import os
import picfinder
import unittest
import tempfile

class picfinderTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, picfinder.app.config['DATABASE'] = tempfile.mkstemp()
        picfinder.app.testing = True
        self.app = picfinder.app.test_client()
        with picfinder.app.app_context():
            picfinder.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(picfinder.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'No entries here so far' in rv.data






if __name__ == '__main__':
    unittest.main()
