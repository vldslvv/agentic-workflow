//! Persistent TODO operations backed by PostgreSQL.

use postgres::{Client, Config, NoTls, Row};
use std::time::Duration;

pub type Result<T> = std::result::Result<T, Box<dyn std::error::Error>>;

pub const DEFAULT_DATABASE_URL: &str = "postgres://todolist:todolist@127.0.0.1:5432/todolist";

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Status {
    New,
    Completed,
    Deleted,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Task {
    pub id: i32,
    pub description: String,
    pub status: Status,
}

/// A live PostgreSQL connection. Each mutation is committed before returning.
pub struct Store {
    client: Client,
}

impl Store {
    pub fn from_env() -> Result<Self> {
        let url = match std::env::var("DATABASE_URL") {
            Ok(url) => url,
            Err(std::env::VarError::NotPresent) => DEFAULT_DATABASE_URL.to_owned(),
            Err(error) => return Err(format!("invalid DATABASE_URL: {error}").into()),
        };
        Self::open(&url)
    }

    /// Connect and initialize a fresh database, safely on repeated invocations.
    pub fn open(url: &str) -> Result<Self> {
        let mut config: Config = url
            .parse()
            .map_err(|error| format!("invalid database connection configuration: {error}"))?;
        config.connect_timeout(Duration::from_secs(3));
        let mut client = config
            .connect(NoTls)
            .map_err(|error| format!("database connection failed: {error}"))?;
        let mut transaction = client.transaction()?;
        // Serialize first-time schema creation across concurrent CLI processes.
        transaction.batch_execute(
            "SELECT pg_advisory_xact_lock(8390272251);
             DO $$ BEGIN
                 CREATE TYPE public.task_status AS ENUM ('New', 'Completed', 'Deleted');
             EXCEPTION WHEN duplicate_object THEN NULL;
             END $$;
             CREATE TABLE IF NOT EXISTS public.tasks (
                 id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                 description text NOT NULL,
                 added timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
                 \"update\" timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
                 status public.task_status NOT NULL DEFAULT 'New'
             );",
        )?;
        transaction.commit()?;
        Ok(Self { client })
    }

    pub fn add(&mut self, description: &str) -> Result<Task> {
        let description = description.trim();
        if description.is_empty() {
            return Err("task description must not be blank".into());
        }
        let row = self.client.query_one(
            "INSERT INTO public.tasks (description) VALUES ($1)
             RETURNING id, description, status::text",
            &[&description],
        )?;
        Self::task(row)
    }

    pub fn list(&mut self) -> Result<Vec<Task>> {
        self.client
            .query(
                "SELECT id, description, status::text FROM public.tasks
                 WHERE status <> 'Deleted' ORDER BY id",
                &[],
            )?
            .into_iter()
            .map(Self::task)
            .collect()
    }

    pub fn complete(&mut self, id: i32) -> Result<()> {
        self.set_status(id, "Completed")
    }

    pub fn delete(&mut self, id: i32) -> Result<()> {
        self.set_status(id, "Deleted")
    }

    fn set_status(&mut self, id: i32, status: &str) -> Result<()> {
        let count = self.client.execute(
            "UPDATE public.tasks SET
                 \"update\" = CASE WHEN status::text = $2 THEN \"update\"
                               ELSE CURRENT_TIMESTAMP END,
                 status = $2::text::public.task_status
             WHERE id = $1 AND status <> 'Deleted'",
            &[&id, &status],
        )?;
        if count == 0 {
            return Err(format!("task {id} not found").into());
        }
        Ok(())
    }

    fn task(row: Row) -> Result<Task> {
        let status = match row.get::<_, &str>(2) {
            "New" => Status::New,
            "Completed" => Status::Completed,
            "Deleted" => Status::Deleted,
            other => return Err(format!("unknown task status: {other}").into()),
        };
        Ok(Task {
            id: row.get(0),
            description: row.get(1),
            status,
        })
    }
}
