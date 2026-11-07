use std::{env, process::ExitCode};
use todolist_rust::{Error, Status, TodoStore};

const HELP: &str = "TODO commands:
  add <description>  Add one task; quote descriptions: add \"Buy milk\"
  delete <id>        Delete a task
  complete <id>      Mark a task complete
  list               List tasks: [ ] incomplete, [x] complete
  help               Show this help (also -h, --help, or no arguments)

Storage: PostgreSQL must be alive for every invocation. Configure DATABASE_URL.
IDs are decimal integers from 0 to 2147483647 (stored IDs start at 1). Empty descriptions are allowed: add \"\".";

enum Command {
    Add(String),
    Delete(i32),
    Complete(i32),
    List,
    Help,
}

fn parse(args: Vec<String>) -> Result<Command, &'static str> {
    let id = |value: &str| {
        if value.is_empty() || !value.bytes().all(|byte| byte.is_ascii_digit()) {
            return Err("ID must be an unsigned decimal integer");
        }
        value
            .parse()
            .map_err(|_| "ID is too large for PostgreSQL integer")
    };
    match args.as_slice() {
        [] => Ok(Command::Help),
        [command] if matches!(command.as_str(), "help" | "-h" | "--help") => Ok(Command::Help),
        [command] if command == "list" => Ok(Command::List),
        [command, description] if command == "add" => Ok(Command::Add(description.clone())),
        [command, value] if command == "delete" => Ok(Command::Delete(id(value)?)),
        [command, value] if command == "complete" => Ok(Command::Complete(id(value)?)),
        _ => Err("unknown command or incorrect number of arguments"),
    }
}

fn execute(command: Command, store: &mut TodoStore) -> Result<(), Error> {
    match command {
        Command::Help => println!("{HELP}"),
        Command::Add(description) => println!("Added task {}", store.create(description)?.id),
        Command::Delete(id) => println!("Deleted task {}", store.delete(id)?.id),
        Command::Complete(id) => println!("Completed task {}", store.complete(id)?.id),
        Command::List => {
            let tasks = store.list()?;
            if tasks.is_empty() {
                println!("No tasks.");
            }
            for task in tasks {
                let marker = if task.status == Status::Completed {
                    'x'
                } else {
                    ' '
                };
                println!("{} [{marker}] {}", task.id, task.description);
            }
        }
    }
    Ok(())
}

fn main() -> ExitCode {
    let mut store = match TodoStore::project() {
        Ok(store) => store,
        Err(error) => {
            eprintln!("{error}");
            return ExitCode::from(1);
        }
    };
    let command = env::args_os()
        .skip(1)
        .map(|arg| arg.into_string().map_err(|_| "arguments must be UTF-8"))
        .collect::<Result<Vec<_>, _>>()
        .and_then(parse);
    match command {
        Err(error) => {
            eprintln!("{error}. Run 'todolist_rust help' for usage.");
            ExitCode::from(2)
        }
        Ok(command) => match execute(command, &mut store) {
            Ok(()) => ExitCode::SUCCESS,
            Err(error) => {
                eprintln!("{error}");
                ExitCode::from(1)
            }
        },
    }
}
