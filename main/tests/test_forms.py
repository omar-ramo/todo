from django.test import SimpleTestCase

from ..forms import TaskForm


class TaskFormTest(SimpleTestCase):
    def test_task_form_with_valid_data(self):
        data = {
            'title': 'The first task.',
            'description': 'The only special thing about this task, is ...',
            'do_before': '2022-09-22 19:56:21'
        }
        form = TaskForm(data)
        self.assertTrue(form.is_valid())

    def test_task_form_with_empty_title(self):
        data = {
            'title': '',
            'description': 'The only special thing about this task, is ...',
            'do_before': '2022-09-22 19:56:21'
        }
        form = TaskForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form['title'].errors)

    def test_task_form_with_empty_description(self):
        data = {
            'title': 'The first task.',
            'description': '',
            'do_before': '2022-09-22 19:56:21'
        }
        form = TaskForm(data)
        self.assertTrue(form.is_valid())
        self.assertFalse(form['description'].errors)

    def test_task_form_with_empty_do_before_date(self):
        data = {
            'title': 'The first task.',
            'description': 'The only special thing about this task, is ...',
            'do_before': ''
        }
        form = TaskForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form['do_before'].errors)

    def test_task_form_with_do_before_date_in_the_past(self):
        data = {
            'title': 'The first task.',
            'description': 'The only special thing about this task, is ...',
            'do_before': '2001-12-30 22:18:09'
        }
        form = TaskForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form['do_before'].errors)
