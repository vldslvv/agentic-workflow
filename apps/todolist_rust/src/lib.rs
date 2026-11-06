use chrono::{DateTime, Utc};
use postgres::{Client, Config, NoTls, Row};
use serde::{Deserialize, Serialize};
use std::error::Error;
use std::time::Duration;

type Result<T> = std::result::Result<T, Box<dyn Error>>;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum Status {
    New,
    Completed,
    Deleted,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Task {
    pub id: i32,
    pub description: String,
    pub added: DateTime<Utc>,
    pub update: DateTime<Utc>,
    pub status: Status,
}

/// A live PostgreSQL store. Each successful mutation is committed before return.
pub struct Store {
    client: Client,
}

impl Store {
    /// Connect and initialize the schema. The local Docker database uses no TLS.
    pub fn connect(url: &str) -> Result<Self> {
        let mut config: Config = url.parse()?;
        config.connect_timeout(Duration::from_secs(5));
        let mut client = config.connect(NoTls)?;
        let mut setup = client.transaction()?;
        // Serialize first-time initialization across concurrent CLI processes.
        setup.batch_execute(
            "SELECT pg_advisory_xact_lock(873103017);
             DO $$ BEGIN
               CREATE TYPE public.task_status AS ENUM ('New', 'Completed', 'Deleted');
             EXCEPTION WHEN duplicate_object THEN NULL;
             END $$;
             CREATE TABLE IF NOT EXISTS public.tasks (
               id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY CHECK (id > 0),
               description TEXT NOT NULL CHECK (length(btrim(description)) > 0),
               added TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
               \"update\" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
               status public.task_status NOT NULL DEFAULT 'New'
             );",
        )?;
        setup.commit()?;
        Ok(Self { client })
    }

    pub fn add(&mut self, description: &str) -> Result<Task> {
        if description.trim().is_empty() {
            return Err("description must not be blank".into());
        }
        let row = self.client.query_one(
            "INSERT INTO public.tasks (description) VALUES ($1)
             RETURNING id, description, added, \"update\", status::text",
            &[&description],
        )?;
        task_from_row(row)
    }

    pub fn list(&mut self) -> Result<Vec<Task>> {
        self.client
            .query(
                "SELECT id, description, added, \"update\", status::text
                 FROM public.tasks WHERE status <> 'Deleted' ORDER BY id",
                &[],
            )?
            .into_iter()
            .map(task_from_row)
            .collect()
    }

    pub fn complete(&mut self, id: i32) -> Result<Task> {
        self.change_status(id, "Completed")
    }

    pub fn delete(&mut self, id: i32) -> Result<()> {
        self.change_status(id, "Deleted").map(|_| ())
    }

    fn change_status(&mut self, id: i32, status: &str) -> Result<Task> {
        let row = self.client.query_opt(
            "UPDATE public.tasks
             SET status = $2::text::public.task_status,
                 \"update\" = CASE WHEN status = $2::text::public.task_status
                                   THEN \"update\" ELSE clock_timestamp() END
             WHERE id = $1 AND status <> 'Deleted'
             RETURNING id, description, added, \"update\", status::text",
            &[&id, &status],
        )?;
        task_from_row(row.ok_or_else(|| format!("task {id} not found"))?)
    }
}

fn task_from_row(row: Row) -> Result<Task> {
    let status = match row.try_get::<_, &str>("status")? {
        "New" => Status::New,
        "Completed" => Status::Completed,
        "Deleted" => Status::Deleted,
        _ => return Err("unknown task status in database".into()),
    };
    Ok(Task {
        id: row.try_get("id")?,
        description: row.try_get("description")?,
        added: row.try_get("added")?,
        update: row.try_get("update")?,
        status,
    })
}
