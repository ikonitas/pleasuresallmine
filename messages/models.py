from django.db import models


class Message(models.Model):
    message = models.TextField()
    is_active = models.NullBooleanField(default=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __unicode__(self):
        return self.message
