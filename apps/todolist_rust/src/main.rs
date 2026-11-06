use std::process::ExitCode;
use std::sync::mpsc;
use std::time::Duration;
use todolist::{Result, Store};

const USAGE: &str = "Usage: todolist <command>

Commands:
  add DESCRIPTION  Add a task (quote descriptions containing spaces)
  list             List active tasks
  complete ID      Mark a task completed
  delete ID        Delete a task
  help             Show this help

Use --help or no arguments to show help.";

fn task_id(text: &str) -> Result<i32> {
    match text.parse::<i32>() {
        Ok(id) if id > 0 => Ok(id),
        _ => Err("task ID must be a positive integer".into()),
    }
}

fn display_description(description: &str) -> String {
    description
        .replace('\\', "\\\\")
        .replace('\t', "\\t")
        .replace('\r', "\\r")
        .replace('\n', "\\n")
}

fn run() -> Result<()> {
    // Bound all startup work, including DNS, authentication and schema setup.
    // On timeout main exits, ending any stalled connection worker as well.
    let (sender, receiver) = mpsc::channel();
    std::thread::spawn(move || {
        let result = Store::from_env().map_err(|error| error.to_string());
        let _ = sender.send(result);
    });
    let mut store = receiver
        .recv_timeout(Duration::from_secs(5))
        .map_err(|_| "database connection or initialization timed out")??;
    let arguments: Vec<String> = std::env::args().skip(1).collect();
    let arguments: Vec<&str> = arguments.iter().map(String::as_str).collect();
    match arguments.as_slice() {
        [] | ["help"] | ["--help"] => println!("{USAGE}"),
        ["add", description] => {
            let task = store.add(description)?;
            println!("Added task {}", task.id);
        }
        ["list"] => {
            let tasks = store.list()?;
            println!("id\tstatus\tdescription");
            for task in tasks {
                println!(
                    "{}\t{:?}\t{}",
                    task.id,
                    task.status,
                    display_description(&task.description)
                );
            }
        }
        ["complete", id] => {
            let id = task_id(id)?;
            store.complete(id)?;
            println!("Completed task {id}");
        }
        ["delete", id] => {
            let id = task_id(id)?;
            store.delete(id)?;
            println!("Deleted task {id}");
        }
        _ => return Err(format!("invalid command or arguments\n\n{USAGE}").into()),
    }
    Ok(())
}

fn main() -> ExitCode {
    match run() {
        Ok(()) => ExitCode::SUCCESS,
        Err(error) => {
            eprintln!("Error: {error}");
            ExitCode::FAILURE
        }
    }
}
