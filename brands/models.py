from django.db import models

from main.models import BaseModel
from main.variables import phone_regex


class Brand(BaseModel):
    name = models.CharField(max_length=128 )
    image = models.ImageField(upload_to="Brand/", blank=True, null=True)
    logo = models.ImageField(upload_to="Brand/", blank=True, null=True)

    class Meta:
        db_table = 'brand'
        verbose_name = ('brand')
        verbose_name_plural = ('brands')
        ordering = ('auto_id', )

    def __str__(self):
        return str(self.name)