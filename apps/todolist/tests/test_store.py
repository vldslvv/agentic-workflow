"""Public business contracts exercised against real JSON files."""

import json
from pathlib import Path
import tempfile
import unittest

from todolist import TaskStore


class TaskStoreTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.path = Path(directory.name) / "tasks.json"
        self.store = TaskStore(self.path)

    def test_persisted_lifecycle(self):
        self.assertEqual(self.store.list(), [])
        self.assertFalse(self.path.exists())
        first = self.store.create("Buy milk")
        second = self.store.create("Walk the dog")
        self.assertIs(type(first["id"]), int)
        self.assertGreater(first["id"], 0)
        self.assertGreater(second["id"], 0)
        self.assertNotEqual(first["id"], second["id"])
        expected = [
            {"id": first["id"], "title": "Buy milk", "completed": False},
            {"id": second["id"], "title": "Walk the dog", "completed": False},
        ]
        self.assertEqual(TaskStore(self.path).list(), expected)
        self.assertEqual(json.loads(self.path.read_text()), expected)

        completed = self.store.complete(first["id"])
        expected[0]["completed"] = True
        self.assertEqual(completed, expected[0])
        self.assertEqual(TaskStore(self.path).list(), expected)
        self.store.delete(second["id"])
        self.assertEqual(TaskStore(self.path).list(), expected[:1])
        self.store.delete(first["id"])
        self.assertEqual(TaskStore(self.path).list(), [])

    def test_each_operation_reads_current_storage(self):
        other = TaskStore(self.path)
        first = self.store.create("First")
        second = other.create("Second")
        self.assertNotEqual(first["id"], second["id"])
        self.assertEqual([task["title"] for task in self.store.list()], ["First", "Second"])
        other.delete(first["id"])
        self.assertEqual(self.store.list(), [second])

    def test_invalid_input_and_unknown_ids_preserve_storage(self):
        self.store.create("Keep me")
        before = self.path.read_bytes()
        for title in ("", " \n\t", None, 12):
            with self.subTest(title=title), self.assertRaises(ValueError):
                self.store.create(title)
            self.assertEqual(self.path.read_bytes(), before)
        for operation in (self.store.complete, self.store.delete):
            for task_id in (0, -1, True, "1", 1.5, None, 999):
                with self.subTest(operation=operation.__name__, task_id=task_id):
                    with self.assertRaises(ValueError):
                        operation(task_id)
                    self.assertEqual(self.path.read_bytes(), before)

    def test_malformed_storage_is_reported_and_preserved(self):
        valid = {"id": 1, "title": "Keep", "completed": False}
        payloads = [
            "{", "null", "{}", "[3]",
            json.dumps([{"id": 1}]),
            json.dumps([valid, valid]),
        ]
        for field, values in {
            "id": [0, -1, True, "1"],
            "title": [" ", None, 4],
            "completed": [0, "false", None],
        }.items():
            payloads.extend(json.dumps([{**valid, field: value}]) for value in values)
        for payload in payloads:
            self.path.write_text(payload)
            for operation in (
                self.store.list, lambda: self.store.create("New"),
                lambda: self.store.complete(1), lambda: self.store.delete(1),
            ):
                with self.subTest(payload=payload), self.assertRaises(ValueError):
                    operation()
                self.assertEqual(self.path.read_text(), payload)


if __name__ == "__main__":
    unittest.main()
