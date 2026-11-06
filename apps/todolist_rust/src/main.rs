use std::error::Error;
use std::io::{self, Write};
use std::process::ExitCode;
use todolist_rust::Store;

const HELP: &str = "Usage: todolist_rust COMMAND [ARGUMENT]

Commands:
  add DESCRIPTION  Add a new task (quote descriptions containing spaces)
  list             List active tasks as JSON, ordered by ID
  complete ID      Complete a task and print it as JSON
  delete ID        Delete a task
  help, --help     Show this help

IDs must be positive 32-bit integers. Tasks are stored in PostgreSQL.
Start the database with 'docker compose up -d --wait' from the app directory.
DATABASE_URL overrides postgres://todo:todo@127.0.0.1:5432/todo.
Operational commands require a live database; help works offline.
Errors are printed to stderr with a nonzero exit status.
";

enum Command {
    Add(String),
    List,
    Complete(i32),
    Delete(i32),
    Help,
}

fn parse_command(args: &[String]) -> Result<Command, Box<dyn Error>> {
    let command = match args {
        [command] if command == "help" || command == "--help" => Command::Help,
        [command] if command == "list" => Command::List,
        [command, description] if command == "add" => {
            if description.trim().is_empty() {
                return Err("description must not be blank".into());
            }
            Command::Add(description.clone())
        }
        [command, value] if command == "complete" || command == "delete" => {
            let id = value
                .parse::<i32>()
                .ok()
                .filter(|id| *id > 0)
                .ok_or("ID must be a positive 32-bit integer")?;
            if command == "complete" {
                Command::Complete(id)
            } else {
                Command::Delete(id)
            }
        }
        _ => return Err("invalid command or arguments; run 'todolist_rust help'".into()),
    };
    Ok(command)
}

fn print_json(value: &impl serde::Serialize) -> Result<(), Box<dyn Error>> {
    let mut output = io::stdout().lock();
    serde_json::to_writer(&mut output, value)?;
    writeln!(output)?;
    Ok(())
}

fn run() -> Result<(), Box<dyn Error>> {
    let args = std::env::args_os()
        .skip(1)
        .map(|arg| {
            arg.into_string()
                .map_err(|_| "arguments must be valid UTF-8")
        })
        .collect::<Result<Vec<_>, _>>()?;
    let command = parse_command(&args)?;
    if matches!(command, Command::Help) {
        io::stdout().lock().write_all(HELP.as_bytes())?;
        return Ok(());
    }

    let url = match std::env::var("DATABASE_URL") {
        Ok(url) => url,
        Err(std::env::VarError::NotPresent) => "postgres://todo:todo@127.0.0.1:5432/todo".into(),
        Err(error) => return Err(error.into()),
    };
    let mut store = Store::connect(&url)?;
    match command {
        Command::Add(description) => print_json(&store.add(&description)?)?,
        Command::List => print_json(&store.list()?)?,
        Command::Complete(id) => print_json(&store.complete(id)?)?,
        Command::Delete(id) => store.delete(id)?,
        Command::Help => unreachable!(),
    }
    Ok(())
}

fn main() -> ExitCode {
    match run() {
        Ok(()) => ExitCode::SUCCESS,
        Err(error) => {
            eprintln!("error: {error}");
            ExitCode::FAILURE
        }
    }
}
