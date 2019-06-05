# -*- coding: utf-8 -*-
from django.urls import reverse
from django.db import models
from django.utils.text import slugify
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Task(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)
    description = models.TextField(blank=True, default='')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    do_before = models.DateTimeField()
    finished_on = models.DateTimeField(null=True)
    done = models.BooleanField(default=False)

    user = models.ForeignKey(
        User,
        related_name='tasks',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['do_before']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if(not self.id):
            try:
                last_task = Task.objects.latest('pk')
                next_id = last_task.id + 1
            except Task.DoesNotExist:
                next_id = 1

            self.slug = '{}-{}'.format(
                next_id,
                slugify(self.title, allow_unicode=True)
            )

        super(Task, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('main:task_detail', args=[self.slug])

    def get_update_url(self):
        return reverse('main:task_update', args=[self.slug])

    def get_delete_url(self):
        return reverse('main:task_delete', args=[self.slug])

    def get_do_url(self):
        return reverse('main:task_do', args=[self.slug])

    def get_undo_url(self):
        return reverse('main:task_undo', args=[self.slug])
