# -*- coding: utf-8 -*-
import unittest

from django import test

from .. import models


class TestCommentForm(test.TestCase):

    def test_author_is_required(self):
        self.fail('test_author_is_required FAULT')

    def test_email_is_required(self):
        self.fail('test_email_is_required FAULT')

    def test_email_pattern(self):
        self.fail('test_email_pattern FAULT')

    def test_content_is_required(self):
        self.fail('test_content_is_required FAULT')
