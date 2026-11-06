use todolist::Store;
fn main() {
    let expected=std::path::PathBuf::from(std::env::args().nth(1).unwrap());
    assert_eq!(Store::default_path(), expected.join("tasks.json"));
    let path=std::path::PathBuf::from(std::env::args().nth(2).unwrap());
    let mut store=Store::open(&path).unwrap();
    let task=store.add("existing").unwrap();
    let before=std::fs::read(&path).unwrap();
    assert!(store.add(" \n\t").is_err());
    assert_eq!(std::fs::read(&path).unwrap(), before);
    assert!(store.complete(task.id+1).is_err());
    assert_eq!(std::fs::read(&path).unwrap(), before);
    assert!(store.delete(task.id+1).is_err());
    assert_eq!(std::fs::read(&path).unwrap(), before);
    store.complete(task.id).unwrap();
    let completed=std::fs::read(&path).unwrap();
    store.complete(task.id).unwrap();
    assert_eq!(std::fs::read(&path).unwrap(), completed);
    std::fs::remove_file(path).unwrap();
    println!("B1 B3 B4: rejected operations preserve exact bytes; completion idempotent. B5: default path is app root from unrelated working directory.");
}
