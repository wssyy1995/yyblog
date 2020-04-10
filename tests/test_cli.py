# -*- coding: utf-8 -*-

from yayanblog.models import Admin, Post,Comment
from yayanblog.extensions import db
from tests.base import BaseTestCase


class CLITestCase(BaseTestCase):

    def setUp(self):
        super(CLITestCase, self).setUp()
        db.drop_all()

    def test_initdb_command(self):
        result = self.runner.invoke(args=['initdb'])
        self.assertIn('Initialized database.', result.output)

    def test_initdb_command_with_drop(self):
        result = self.runner.invoke(args=['initdb', '--drop'], input='y\n')
        self.assertIn('This operation will delete the database, do you want to continue?', result.output)
        self.assertIn('Drop tables.', result.output)

    def test_init_command(self):
        result = self.runner.invoke(args=['init', '--username', 'grey', '--password', '123'])
        self.assertIn('Creating the temporary administrator account...', result.output)
        self.assertIn('Done.', result.output)
        self.assertEqual(Admin.query.count(), 1)
        self.assertEqual(Admin.query.first().username, 'grey')

    def test_init_command_with_update(self):
        self.runner.invoke(args=['init', '--username', 'grey', '--password', '123'])
        result = self.runner.invoke(args=['init', '--username', 'new grey', '--password', '123'])
        self.assertIn('The administrator already exists, updating...', result.output)
        self.assertNotIn('Creating the temporary administrator account...', result.output)
        self.assertEqual(Admin.query.count(), 1)
        self.assertEqual(Admin.query.first().username, 'new grey')

    def test_forge_command(self):
        result = self.runner.invoke(args=['forge'])

        self.assertEqual(Admin.query.count(), 1)
        self.assertIn('Generating the administrator...', result.output)

        self.assertEqual(Post.query.count(), 50)
        self.assertIn('Generating 50 posts...', result.output)


        self.assertEqual(Comment.query.count(), 500 + 50 + 50 + 50)
        self.assertIn('Generating 500 comments...', result.output)

    def test_forge_command_with_count(self):
        result = self.runner.invoke(args=['forge','--post', '20', '--comment', '100'])
        self.assertEqual(Admin.query.count(), 1)
        self.assertIn('Generating the administrator...', result.output)

        self.assertEqual(Post.query.count(), 20)
        self.assertIn('Generating 20 posts...', result.output)



        self.assertEqual(Comment.query.count(), 100 + 10 + 10 + 10)
        self.assertIn('Generating 100 comments...', result.output)
