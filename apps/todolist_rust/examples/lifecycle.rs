//! Run only against a fresh disposable database selected by DATABASE_URL.
use todolist_rust::{Status, TodoStore};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut store = TodoStore::project()?;
    assert!(store.list()?.is_empty());
    let a = store.create("A")?;
    let b = store.create("B")?;
    assert_eq!(store.list()?, vec![a.clone(), b.clone()]);
    let completed = store.complete(a.id)?;
    assert_eq!(completed.status, Status::Completed);
    assert_eq!(store.complete(a.id)?, completed);
    store.delete(b.id)?;
    assert_eq!(TodoStore::project()?.list()?, vec![completed.clone()]);
    store.delete(completed.id)?;
    assert!(TodoStore::project()?.list()?.is_empty());
    println!("PASS: PostgreSQL lifecycle, including fresh connection and soft deletion");
    Ok(())
}
