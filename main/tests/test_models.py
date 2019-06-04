from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from ..models import Task


class TaskTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1_credentials = {
            'username': 'user1',
            'email': 'user1@domain.com',
            'password': 'APQMwn0$'
        }
        cls.user1 = User.objects.create_user(**user1_credentials)

    def test_save_method_works_correctly(self):
        task1_data = {
            'title': 'Another task',
            'description': 'Nothing new here.',
            'do_before': timezone.now() + timedelta(days=3),
            'user': TaskTest.user1
        }
        task1 = Task.objects.create(**task1_data)
        self.assertEqual(task1.slug, '1-another-task')

        task2_data = {
            'title': 'Another task number 2',
            'do_before': timezone.now() + timedelta(days=3),
            'user': TaskTest.user1
        }
        task2 = Task.objects.create(**task2_data)
        self.assertEqual(task2.slug, '2-another-task-number-2')

    def test_str_method_returns_the_task_title(self):
        task_data = {
            'title': 'Another task',
            'description': 'Nothing new here.',
            'do_before': timezone.now() + timedelta(days=3),
            'user': TaskTest.user1
        }
        task = Task.objects.create(**task_data)
        self.assertEqual(str(task), task_data['title'])

    def test_get_absolute_url_returns_the_correct_url(self):
        task_data = {
            'title': 'A task',
            'description': 'Nothing new here.',
            'do_before': timezone.now() + timedelta(days=3),
            'user': TaskTest.user1
        }
        task = Task.objects.create(**task_data)

        expected_url = '/1-a-task/detail/'

        self.assertEqual(task.get_absolute_url(), expected_url)

    def test_get_update_url_returns_the_correct_url(self):
        task_data = {
            'title': 'A task',
            'description': 'Nothing new here.',
            'do_before': timezone.now() + timedelta(days=3),
            'user': TaskTest.user1
        }
        task = Task.objects.create(**task_data)

        expected_url = '/1-a-task/update/'

        self.assertEqual(task.get_update_url(), expected_url)

    def test_get_delete_url_returns_the_correct_url(self):
        task_data = {
            'title': 'A task',
            'description': 'Nothing new here.',
            'do_before': timezone.now() + timedelta(days=3),
            'user': TaskTest.user1
        }
        task = Task.objects.create(**task_data)

        expected_url = '/1-a-task/delete/'

        self.assertEqual(task.get_delete_url(), expected_url)

    def test_get_undo_url_returns_the_correct_url(self):
        task_data = {
            'title': 'A task',
            'description': 'Nothing new here.',
            'do_before': timezone.now() + timedelta(days=3),
            'user': TaskTest.user1
        }
        task = Task.objects.create(**task_data)

        expected_url = '/1-a-task/undo/'

        self.assertEqual(task.get_undo_url(), expected_url)

    def test_get_do_url_returns_the_correct_url(self):
        task_data = {
            'title': 'A task',
            'description': 'Nothing new here.',
            'do_before': timezone.now() + timedelta(days=3),
            'user': TaskTest.user1
        }
        task = Task.objects.create(**task_data)

        expected_url = '/1-a-task/do/'

        self.assertEqual(task.get_do_url(), expected_url)
