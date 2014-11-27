from django.db import models
from django.contrib.auth.models import User
from accounts.choice_list import SOCIAL_TITLE_CHOICES

class UserProfile(models.Model):
    title = models.CharField(choices=SOCIAL_TITLE_CHOICES, max_length=10)
    date_of_birth = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    user = models.OneToOneField(User, unique=True)
    terms = models.BooleanField()
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s" % self.user.username

    def full_name(self):
        return "%s %s %s" % (self.get_title_display(), self.user.first_name, self.user.last_name)

    def user_email(self):
        return self.user.email

    class Meta:
        verbose_name = 'Customer'


class Address(models.Model):
    company_name = models.CharField(max_length=200, null=True, blank=True)
    line_1 = models.CharField(max_length=255)
    line_2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255)
    county = models.CharField(max_length=100, null=True, blank=True)
    postcode = models.CharField(max_length=10)
    user = models.ForeignKey(User)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s" % self.line_1
