"""Public business API checks; isolated temporary persistence per case."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / 'apps/todolist'))
from todolist import TaskStore

class BusinessContract(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'tasks.json'
        self.store = TaskStore(self.path)

    def test_persisted_lifecycle(self):
        self.assertEqual(self.store.list_tasks(), [])
        first = self.store.create_task('  Buy milk  ')
        second = self.store.create_task('Read book')
        self.assertEqual(first, {'id': 1, 'title': 'Buy milk', 'completed': False})
        self.assertEqual(second['id'], 2)
        self.assertTrue(self.path.is_file())
        self.store = TaskStore(self.path)
        self.assertEqual(self.store.list_tasks(), [first, second])
        self.store.complete_task(first['id'])
        self.store.complete_task(first['id'])
        self.store.delete_task(second['id'])
        self.assertEqual(TaskStore(self.path).list_tasks(), [dict(first, completed=True)])
        self.store.delete_task(first['id'])
        self.assertEqual(TaskStore(self.path).list_tasks(), [])

    def test_rejected_operations_preserve_data(self):
        self.store.create_task('Keep me')
        before = self.path.read_bytes()
        for operation in (lambda: self.store.create_task(' \t'),
                          lambda: self.store.delete_task(999),
                          lambda: self.store.complete_task(999)):
            with self.subTest(operation=operation):
                with self.assertRaises(ValueError):
                    operation()
                self.assertEqual(self.path.read_bytes(), before)

    def test_corrupt_storage_is_not_overwritten(self):
        for raw in ('{broken', '{}', '[{"id": 1}]'):
            with self.subTest(raw=raw):
                self.path.write_text(raw)
                with self.assertRaises(ValueError):
                    TaskStore(self.path).create_task('Must not erase')
                self.assertEqual(self.path.read_text(), raw)

if __name__ == '__main__':
    unittest.main()
