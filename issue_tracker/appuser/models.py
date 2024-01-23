from django.contrib.auth.models import AbstractUser
from django.db import models


class AppUser(AbstractUser):
    phone = models.CharField(max_length=100, verbose_name="Phone", blank=True)
    photo = models.ImageField(upload_to="users/photos", verbose_name="Photo", blank=True)
    department = models.CharField(max_length=100, verbose_name='Department', blank=True)
    job_title = models.CharField(max_length=100, verbose_name='Job Title', blank=True)
    team = models.ForeignKey('appuser.Team', on_delete=models.PROTECT, verbose_name='Team', null=True)


class Team(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    team_lead = models.OneToOneField('appuser.AppUser', on_delete=models.PROTECT, verbose_name='Teamlead')