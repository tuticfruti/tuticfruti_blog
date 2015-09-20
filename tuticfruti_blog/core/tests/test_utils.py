# -*- coding: utf-8 -*-

import unittest
from unittest import mock

from tuticfruti_blog.core.utils import MockQueryset
from tuticfruti_blog.posts import models


class MockQuerySetTest(unittest.TestCase):
    def setUp(self):
        self.items = [
            mock.Mock(spec=models.Post, title='Post title 1'),
            mock.Mock(spec=models.Post, title='Post title 2')
        ]
        self.queryset = MockQueryset(items=self.items)

    def test___init__(self):
        queryset = MockQueryset(model=models.Post)
        self.assertEqual(queryset.model, models.Post)

        queryset = MockQueryset(items=self.items)
        self.assertEqual(queryset.model, self.items[0].__class__)

    def test___len__(self):
        self.assertEqual(len(self.items), 2)

    def test___getitem__(self):
        self.assertEqual(self.queryset[0].title, self.items[0].title)
        self.assertEqual(self.queryset[1].title, self.items[1].title)

    def test___setitem__(self):
        self.queryset[0].title = 'New title'
        self.assertEqual(self.queryset[0].title, 'New title')

    def test___delitem__(self):
        del self.queryset[0]
        self.assertEqual(len(self.queryset), 1)

    def test___iter__(self):
        for key, item in enumerate(self.queryset):
            self.assertEqual(item, self.items[key])

    def test__reversed__(self):
        reversed(self.queryset)
        for key, item in enumerate(self.queryset):
            self.assertEqual(item, self.queryset[-key])

    def test__contains__(self):
        self.assertTrue(self.items[0] in self.queryset)
        self.assertFalse(mock.Mock(spec=models.Post) in self.queryset)

    def test___str__(self):
        self.assertEqual(str(self.queryset), str(self.items))

    def test___repr__(self):
        self.assertEqual(repr(self.queryset), repr(self.items))
