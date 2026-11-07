//! TODO business operations backed by PostgreSQL.
use chrono::{DateTime, Utc};
use postgres::{Client, NoTls, Row};
use std::{env, fmt, time::Duration};

pub const DEFAULT_DATABASE_URL: &str = "postgres://todo:todo@127.0.0.1:5432/todo";

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Status {
    Completed,
    New,
    Deleted,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Task {
    pub id: i32,
    pub description: String,
    pub added: DateTime<Utc>,
    pub update: DateTime<Utc>,
    pub status: Status,
}

#[derive(Debug)]
pub enum Error {
    Database(postgres::Error),
    Configuration(env::VarError),
    NotFound(i32),
    InvalidStatus(String),
    IncompatibleSchema,
}

impl fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Database(error) => match error.as_db_error() {
                Some(detail) => write!(f, "database: {}", detail.message()),
                None => write!(f, "database: {error}"),
            },
            Self::Configuration(error) => write!(f, "database configuration: {error}"),
            Self::NotFound(id) => write!(f, "task {id} does not exist"),
            Self::IncompatibleSchema => write!(f, "database: incompatible tasks schema"),
            Self::InvalidStatus(status) => write!(f, "database: unsupported task status {status}"),
        }
    }
}

impl std::error::Error for Error {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Self::Database(error) => Some(error),
            Self::Configuration(error) => Some(error),
            _ => None,
        }
    }
}

impl From<postgres::Error> for Error {
    fn from(error: postgres::Error) -> Self {
        Self::Database(error)
    }
}

fn task(row: Row) -> Result<Task, Error> {
    let status: String = row.try_get("status")?;
    let status = match status.as_str() {
        "New" => Status::New,
        "Completed" => Status::Completed,
        "Deleted" => Status::Deleted,
        _ => return Err(Error::InvalidStatus(status)),
    };
    Ok(Task {
        id: row.try_get("id")?,
        description: row.try_get("description")?,
        added: row.try_get("added")?,
        update: row.try_get("update")?,
        status,
    })
}

/// Owns a live database connection; each mutation commits before returning.
pub struct TodoStore {
    client: Client,
}

impl TodoStore {
    /// DATABASE_URL or the local compose database, independent of working directory.
    pub fn project() -> Result<Self, Error> {
        let url = match env::var("DATABASE_URL") {
            Ok(url) => url,
            Err(env::VarError::NotPresent) => DEFAULT_DATABASE_URL.to_owned(),
            Err(error) => return Err(Error::Configuration(error)),
        };
        Self::connect(&url)
    }

    /// Connect with a five-second connection timeout and initialize a fresh schema.
    pub fn connect(url: &str) -> Result<Self, Error> {
        let mut config: postgres::Config = url.parse()?;
        config.connect_timeout(Duration::from_secs(5));
        let mut client = config.connect(NoTls)?;
        client.simple_query("SELECT 1")?;
        let mut transaction = client.transaction()?;
        transaction.batch_execute(
            "DO $$ BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'task_status'
                               AND typnamespace = current_schema()::regnamespace) THEN
                    CREATE TYPE task_status AS ENUM ('Completed', 'New', 'Deleted');
                END IF;
             END $$;
             CREATE TABLE IF NOT EXISTS tasks (
                id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY CHECK (id > 0),
                description text NOT NULL,
                added timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
                \"update\" timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
                status task_status NOT NULL DEFAULT 'New'
             );",
        )?;
        // CREATE TABLE IF NOT EXISTS alone would silently accept incompatible tables.
        let compatible: bool = transaction
            .query_one(
                "SELECT COALESCE(
                (SELECT count(*) = 5 AND bool_and(attnotnull AND COALESCE(atttypid =
                    CASE attname
                        WHEN 'id' THEN 'integer'::regtype
                        WHEN 'description' THEN 'text'::regtype
                        WHEN 'added' THEN 'timestamptz'::regtype
                        WHEN 'update' THEN 'timestamptz'::regtype
                        WHEN 'status' THEN 'task_status'::regtype
                    END, false))
                 FROM pg_attribute WHERE attrelid = 'tasks'::regclass
                 AND attnum > 0 AND NOT attisdropped)
                AND EXISTS (SELECT 1 FROM pg_constraint c JOIN pg_attribute a
                    ON a.attrelid = c.conrelid AND a.attname = 'id'
                    WHERE c.conrelid = 'tasks'::regclass AND c.contype = 'p'
                    AND c.conkey = ARRAY[a.attnum] AND a.attidentity IN ('a', 'd'))
                AND (SELECT array_agg(enumlabel ORDER BY enumlabel) =
                    ARRAY['Completed', 'Deleted', 'New']::name[]
                    FROM pg_enum WHERE enumtypid = 'task_status'::regtype), false)",
                &[],
            )?
            .get(0);
        if !compatible {
            return Err(Error::IncompatibleSchema);
        }
        transaction.commit()?;
        Ok(Self { client })
    }

    /// Visible tasks in creation order; Deleted rows remain only in the database.
    pub fn list(&mut self) -> Result<Vec<Task>, Error> {
        self.client
            .query("SELECT id, description, added, \"update\", status::text FROM tasks WHERE status <> 'Deleted' ORDER BY id", &[])?
            .into_iter().map(task).collect()
    }

    pub fn create(&mut self, description: impl Into<String>) -> Result<Task, Error> {
        task(self.client.query_one(
            "INSERT INTO tasks (description, added, \"update\", status) VALUES ($1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'New') RETURNING id, description, added, \"update\", status::text",
            &[&description.into()],
        )?)
    }

    /// Already-completed tasks retain all timestamps and succeed unchanged.
    pub fn complete(&mut self, id: i32) -> Result<Task, Error> {
        let mut transaction = self.client.transaction()?;
        let row = transaction.query_opt(
            "SELECT id, description, added, \"update\", status::text FROM tasks WHERE id = $1 AND status <> 'Deleted' FOR UPDATE",
            &[&id],
        )?.ok_or(Error::NotFound(id))?;
        let current = task(row)?;
        let result = if current.status == Status::New {
            task(transaction.query_one(
                "UPDATE tasks SET status = 'Completed', \"update\" = clock_timestamp() WHERE id = $1 RETURNING id, description, added, \"update\", status::text",
                &[&id],
            )?)?
        } else {
            current
        };
        transaction.commit()?;
        Ok(result)
    }

    /// Soft-delete a visible task, retaining its identity and creation timestamp.
    pub fn delete(&mut self, id: i32) -> Result<Task, Error> {
        let row = self.client.query_opt(
            "UPDATE tasks SET status = 'Deleted', \"update\" = clock_timestamp() WHERE id = $1 AND status <> 'Deleted' RETURNING id, description, added, \"update\", status::text",
            &[&id],
        )?.ok_or(Error::NotFound(id))?;
        task(row)
    }
}
