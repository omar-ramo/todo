from datetime import timedelta
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from ..forms import TaskForm
from ..models import Task
from ..views import (
    task_list, task_detail, task_create, task_update, task_delete
)
User = get_user_model()


class TaskListTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1_credentials = {
            'username': 'user1',
            'email': 'user1@domain.com',
            'password': 'APQMwn0$'
        }
        cls.user1 = User.objects.create_user(**cls.user1_credentials)

        cls.user2_credentials = {
            'username': 'user2',
            'email': 'user1@domain.com',
            'password': 'APQMw2Zn0$'
        }
        cls.user2 = User.objects.create_user(**cls.user2_credentials)

        Task.objects.create(
            title='Read for 20 mins.(user1)',
            do_before=timezone.now() + timedelta(days=3),
            user=cls.user1
        )
        Task.objects.create(
            title='Watch A tv show.(user1)',
            do_before=timezone.now() + timedelta(days=1),
            user=cls.user1
        )
        Task.objects.create(
            title='Watch a crashcourse.(user1)',
            do_before=timezone.now() - timedelta(days=1),
            finished_on=timezone.now() - timedelta(days=2),
            done=True,
            user=cls.user1
        )
        cls.user1_undone_tasks = Task.objects.filter(
            user=cls.user1, done=False
        )

    def test_task_list_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.resolver_match.func, task_list)

    def test_task_list_url_pattern_naming_works_correctly(self):
        response = self.client.get(reverse('main:task_list'))
        self.assertEqual(response.resolver_match.func, task_list)

    def test_task_list_redirect_unlogged_in_user(self):
        """Unlogged in user will be redirected to login page"""
        response = self.client.get(reverse('main:task_list'))
        expected_url = f'{reverse("account_login")}'
        expected_url += f'?next={reverse("main:task_list")}'
        self.assertRedirects(response, expected_url)

    def test_task_list_uses_correct_template(self):
        self.client.login(
            email=TaskListTest.user1_credentials['email'],
            password=TaskListTest.user1_credentials['password']
        )
        response = self.client.get(reverse('main:task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/task_list.html')

    def test_logged_in_user_will_see_only_his_tasks(self):
        """Ensure a user can't see another user's tasks"""
        self.client.login(
            email=TaskListTest.user1_credentials['email'],
            password=TaskListTest.user1_credentials['password']
        )
        response = self.client.get(reverse('main:task_list'))
        self.assertQuerysetEqual(
            response.context['tasks'],
            TaskListTest.user1_undone_tasks,
            transform=lambda x: x
        )

    def test_logged_in_user_will_see_add_task_link(self):
        """Ensure a user will see a 'Add Task' link"""
        self.client.login(
            email=TaskListTest.user1_credentials['email'],
            password=TaskListTest.user1_credentials['password']
        )
        response = self.client.get(reverse('main:task_list'))
        link = reverse('main:task_create')
        html_link = f'<a href="{link}">Add Task</a>'
        self.assertInHTML(html_link, response.content.decode('utf-8'))

    def test_logged_in_user_will_see_management_links_for_each_task(self):
        """Ensures page will contain done, update and delete links for
           each task
        """
        self.client.login(
            email=TaskListTest.user1_credentials['email'],
            password=TaskListTest.user1_credentials['password']
        )
        response = self.client.get(reverse('main:task_list'))

        links = []

        for task in TaskListTest.user1_undone_tasks:
            links.append(f'href="{task.get_absolute_url()}"')
            links.append(f'href="{task.get_do_url()}"')
            links.append(f'href="{task.get_update_url()}"')
            links.append(f'href="{task.get_delete_url()}"')

        for link in links:
            self.assertContains(response, link)


class TaskDetailTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1_credentials = {
            'username': 'user1',
            'email': 'user1@domain.com',
            'password': 'APQMwn0$'
        }
        cls.user1 = User.objects.create_user(**cls.user1_credentials)

        cls.user2_credentials = {
            'username': 'user2',
            'email': 'user1@domain.com',
            'password': 'APQMw2Zn0$'
        }
        cls.user2 = User.objects.create_user(**cls.user2_credentials)

        Task.objects.create(
            title='Read for 20 mins.(user1)',
            do_before=timezone.now() + timedelta(days=3),
            user=cls.user1
        )
        cls.first_task = Task.objects.latest('pk')
        Task.objects.create(
            title='Do nothing at all for a while.(user1)',
            do_before=timezone.now() - timedelta(days=1),
            finished_on=timezone.now() - timedelta(days=2),
            done=True,
            user=cls.user1
        )
        cls.second_task = Task.objects.latest('pk')
        cls.user1_tasks = Task.objects.filter(user=cls.user1)

    def test_task_detail_exists_at_desired_location(self):
        response = self.client.get(
            TaskDetailTest.first_task.get_absolute_url()
        )
        self.assertEqual(response.resolver_match.func, task_detail)

    def test_task_detail_url_pattern_naming_works_correctly(self):
        response = self.client.get(
            reverse('main:task_detail', args=[TaskDetailTest.first_task.slug])
        )
        self.assertEqual(response.resolver_match.func, task_detail)

    def test_task_detail_redirect_unlogged_in_user(self):
        """Unlogged in user will be redirected to login page"""
        response = self.client.get(
            TaskDetailTest.first_task.get_absolute_url()
        )
        expected_url = f'{reverse("account_login")}'
        expected_url += f'?next={TaskDetailTest.first_task.get_absolute_url()}'
        self.assertRedirects(response, expected_url)

    def test_task_detail_uses_correct_template(self):
        self.client.login(
            email=TaskDetailTest.user1_credentials['email'],
            password=TaskDetailTest.user1_credentials['password']
        )
        response = self.client.get(
            TaskDetailTest.first_task.get_absolute_url()
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/task_detail.html')

    def test_logged_in_user_will_see_only_his_tasks(self):
        """Ensure a user can't see another user's task"""
        self.client.login(
            email=TaskDetailTest.user2_credentials['email'],
            password=TaskDetailTest.user2_credentials['password']
        )
        response = self.client.get(
            TaskDetailTest.first_task.get_absolute_url()
        )
        self.assertEqual(response.status_code, 404)

    def test_logged_in_user_will_see_management_links_for_undone_task(self):
        """Ensures page will contain done, update and delete links"""
        self.client.login(
            email=TaskDetailTest.user1_credentials['email'],
            password=TaskDetailTest.user1_credentials['password']
        )
        response = self.client.get(
            TaskDetailTest.first_task.get_absolute_url()
        )

        links = [
            f'href="{TaskDetailTest.first_task.get_do_url()}"',
            f'href="{TaskDetailTest.first_task.get_update_url()}"',
            f'href="{TaskDetailTest.first_task.get_delete_url()}"'
        ]

        for link in links:
            self.assertContains(response, link)

    def test_logged_in_user_will_see_management_links_for_done_task(self):
        """Ensures detail page will contain undone, update and delete links"""
        self.client.login(
            email=TaskDetailTest.user1_credentials['email'],
            password=TaskDetailTest.user1_credentials['password']
        )
        response = self.client.get(
            TaskDetailTest.second_task.get_absolute_url()
        )

        links = [
            f'href="{TaskDetailTest.second_task.get_undo_url()}"',
            f'href="{TaskDetailTest.second_task.get_update_url()}"',
            f'href="{TaskDetailTest.second_task.get_delete_url()}"'
        ]

        for link in links:
            self.assertContains(response, link)


class TaskCreateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1_credentials = {
            'username': 'user1',
            'email': 'user1@domain.com',
            'password': 'APQMwn0$'
        }
        cls.user1 = User.objects.create_user(**cls.user1_credentials)

    def test_task_create_exists_at_desired_location(self):
        response = self.client.get('/add/')
        self.assertEqual(response.resolver_match.func, task_create)

    def test_task_create_url_pattern_naming_works_correctly(self):
        response = self.client.get(reverse('main:task_create'))
        self.assertEqual(response.resolver_match.func, task_create)

    def test_task_create_redirect_unlogged_in_user(self):
        """Unlogged in user will be redirected to login page"""
        response = self.client.get(reverse('main:task_create'))
        expected_url = f'{reverse("account_login")}'
        expected_url += f'?next={reverse("main:task_create")}'
        self.assertRedirects(response, expected_url)

    def test_task_create_uses_correct_template(self):
        self.client.login(
            email=TaskCreateTest.user1_credentials['email'],
            password=TaskCreateTest.user1_credentials['password']
        )
        response = self.client.get(reverse('main:task_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/task_create.html')

    def test_task_create_contains_task_add_form(self):
        self.client.login(
            email=TaskCreateTest.user1_credentials['email'],
            password=TaskCreateTest.user1_credentials['password']
        )
        expected_form_html = f'<form action="{reverse("main:task_create")}"'
        expected_form_html += ' method="post">'

        response = self.client.get(reverse('main:task_create'))

        self.assertIsInstance(response.context['form'], TaskForm)
        self.assertContains(response, expected_form_html)
        self.assertContains(response, '>Create</button>')

    def test_task_create_creates_a_task(self):
        self.client.login(
            email=TaskCreateTest.user1_credentials['email'],
            password=TaskCreateTest.user1_credentials['password']
        )
        task_data = {
            'title': 'Do the task',
            'do_before': '2029-02-23 22:45:01'
        }

        response = self.client.post(
            reverse('main:task_create'),
            data=task_data
        )

        self.assertEqual(Task.objects.count(), 1)

        created_task = Task.objects.first()

        self.assertRedirects(response, created_task.get_absolute_url())
        self.assertEqual(created_task.title, task_data['title'])


class TaskUpdateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1_credentials = {
            'username': 'user1',
            'email': 'user1@domain.com',
            'password': 'APQMwn0$'
        }
        cls.user1 = User.objects.create_user(**cls.user1_credentials)
        task_data = {
            'title': 'Do the task',
            'do_before': '2029-02-23 22:45:01',
            'user': cls.user1
        }
        cls.task = Task.objects.create(**task_data)

    def test_task_update_exists_at_desired_location(self):
        response = self.client.get('/do-the-task/update/')
        self.assertEqual(response.resolver_match.func, task_update)

    def test_task_update_url_pattern_naming_works_correctly(self):
        response = self.client.get(
            reverse('main:task_update', args=[TaskUpdateTest.task.slug])
        )
        self.assertEqual(response.resolver_match.func, task_update)

    def test_task_update_redirect_unlogged_in_user(self):
        """Unlogged in user will be redirected to login page"""
        response = self.client.get(TaskUpdateTest.task.get_update_url())
        expected_url = f'{reverse("account_login")}'
        expected_url += f'?next={TaskUpdateTest.task.get_update_url()}'
        self.assertRedirects(response, expected_url)

    def test_task_update_uses_correct_template(self):
        self.client.login(
            email=TaskUpdateTest.user1_credentials['email'],
            password=TaskUpdateTest.user1_credentials['password']
        )
        response = self.client.get(TaskUpdateTest.task.get_update_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/task_update.html')

    def test_task_update_contains_task_update_form(self):
        self.client.login(
            email=TaskUpdateTest.user1_credentials['email'],
            password=TaskUpdateTest.user1_credentials['password']
        )
        expected_form_html = '<form action="'
        expected_form_html += f'{TaskUpdateTest.task.get_update_url()}"'
        expected_form_html += ' method="post">'

        response = self.client.get(TaskUpdateTest.task.get_update_url())

        self.assertIsInstance(response.context['form'], TaskForm)
        self.assertIsInstance(response.context['form'].instance, Task)
        self.assertContains(response, expected_form_html)
        self.assertContains(response, '>Update</button>')

    def test_task_update_updates_a_task(self):
        self.client.login(
            email=TaskUpdateTest.user1_credentials['email'],
            password=TaskUpdateTest.user1_credentials['password']
        )
        task_new_data = {
            'title': 'Make sure to do the task',
            'do_before': '2027-11-23 22:45:01'
        }

        response = self.client.post(
            TaskUpdateTest.task.get_update_url(),
            data=task_new_data
        )

        self.assertEqual(Task.objects.count(), 1)

        updated_task = Task.objects.first()

        self.assertRedirects(response, updated_task.get_absolute_url())
        self.assertEqual(updated_task.title, task_new_data['title'])


class TaskDeleteTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1_credentials = {
            'username': 'user1',
            'email': 'user1@domain.com',
            'password': 'APQMwn0$'
        }
        cls.user1 = User.objects.create_user(**cls.user1_credentials)
        task_data = {
            'title': 'Do the task',
            'do_before': '2029-02-23 22:45:01',
            'user': cls.user1
        }
        cls.task = Task.objects.create(**task_data)

    def test_task_delete_exists_at_desired_location(self):
        response = self.client.get('/do-the-task/delete/')
        self.assertEqual(response.resolver_match.func, task_delete)

    def test_task_delete_url_pattern_naming_works_correctly(self):
        response = self.client.get(
            reverse('main:task_delete', args=[TaskDeleteTest.task.slug])
        )
        self.assertEqual(response.resolver_match.func, task_delete)

    def test_task_delete_redirect_unlogged_in_user(self):
        """Unlogged in user will be redirected to login page"""
        response = self.client.get(TaskDeleteTest.task.get_delete_url())
        expected_url = f'{reverse("account_login")}'
        expected_url += f'?next={TaskDeleteTest.task.get_delete_url()}'
        self.assertRedirects(response, expected_url)

    def test_task_delete_status_code(self):
        self.client.login(
            email=TaskDeleteTest.user1_credentials['email'],
            password=TaskDeleteTest.user1_credentials['password']
        )
        response = self.client.get(TaskDeleteTest.task.get_delete_url())
        self.assertEqual(response.status_code, 302)

    def test_task_delete_deletes_a_task(self):
        self.client.login(
            email=TaskDeleteTest.user1_credentials['email'],
            password=TaskDeleteTest.user1_credentials['password']
        )

        response = self.client.get(
            TaskDeleteTest.task.get_delete_url(),
        )

        self.assertEqual(Task.objects.count(), 0)

        self.assertRedirects(response, reverse('main:task_list'))
