from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Permission(models.Model):
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=128)
    app = models.CharField(max_length=128)

    class Meta:
        db_table = 'permission'
        verbose_name = ('permission')
        verbose_name_plural = ('permissions')
        ordering = ('app',)

    class Admin:
        list_display = ('id', 'name', 'code', 'app')

    def __str__(self):
        return self.name + ' - ' + self.app