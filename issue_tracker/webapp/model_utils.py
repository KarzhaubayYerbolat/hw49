from django.db import models


class ReturnTitleStrMixin:
    title = None
    objects = models.Manager()

    def __str__(self):
        return self.title
