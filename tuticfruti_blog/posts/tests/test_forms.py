# -*- coding: utf-8 -*-
import unittest

from django import test

from .. import models
from .. import forms


class TestFormBase(test.TestCase):
    @classmethod
    def setUpTestData(cls):
        # Validation errors messages
        cls.REQUIRED_ERROR_MSG = 'This field is required.'
        cls.EMAIL_ERROR_MSG = 'Enter a valid email address.'


class TestCommentForm(TestFormBase):
    def test_author_is_required(self):
        form = forms.CommentForm(models.Comment().__dict__)
        error_msg = form['author'].errors[0]

        self.assertEqual(error_msg, self.REQUIRED_ERROR_MSG)

    def test_email_is_required(self):
        form = forms.CommentForm(models.Comment().__dict__)
        error_msg = form['email'].errors[0]

        self.assertEqual(error_msg, self.REQUIRED_ERROR_MSG)

    def test_malformed_email(self):
        form = forms.CommentForm(
            models.Comment(email='malformed@email').__dict__)
        error_msg = form['email'].errors[0]

        self.assertEqual(error_msg, self.EMAIL_ERROR_MSG)

    def test_content_is_required(self):
        form = forms.CommentForm(models.Comment().__dict__)
        error_msg = form['content'].errors[0]

        self.assertEqual(error_msg, self.REQUIRED_ERROR_MSG)
