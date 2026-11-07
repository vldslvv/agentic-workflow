use chrono::Utc;
use todolist_rust::{Error, Status, TodoStore};

// The process runner provisions a separate real database for this API contract.
#[test]
fn public_api_state_and_connection_lifetime() -> Result<(), Box<dyn std::error::Error>> {
    let url = std::env::var("DATABASE_URL").expect("run tests/cli_e2e.py for an isolated database");
    let mut store = TodoStore::connect(&url)?;
    assert!(store.list()?.is_empty());
    let before = Utc::now();
    let created = store.create("API task")?;
    assert_eq!(created.id, 1);
    assert_eq!(created.description, "API task");
    assert_eq!(created.status, Status::New);
    assert_eq!(created.added, created.update);
    assert!(created.added >= before && created.added <= Utc::now());
    drop(store);
    let mut reconnected = TodoStore::connect(&url)?;
    assert_eq!(reconnected.list()?, vec![created.clone()]);
    let completed = reconnected.complete(created.id)?;
    assert_eq!(completed.status, Status::Completed);
    assert_eq!(completed.added, created.added);
    assert_eq!(reconnected.complete(created.id)?, completed);
    let deleted = reconnected.delete(created.id)?;
    assert_eq!(deleted.status, Status::Deleted);
    assert_eq!(deleted.description, created.description);
    assert_eq!(deleted.added, created.added);
    assert!(reconnected.list()?.is_empty());
    assert!(matches!(
        reconnected.complete(created.id),
        Err(Error::NotFound(1))
    ));
    assert!(matches!(
        reconnected.delete(created.id),
        Err(Error::NotFound(1))
    ));
    assert!(matches!(
        reconnected.complete(i32::MAX),
        Err(Error::NotFound(i32::MAX))
    ));
    assert_eq!(reconnected.create("Next")?.id, 2);
    Ok(())
}
