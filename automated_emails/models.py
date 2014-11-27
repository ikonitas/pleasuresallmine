from django.db import models

class AutomatedEmail(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    is_active = models.BooleanField(default=True, blank=True)
    
    content.help_text = "<p class='help' style='color:red;'>Please do not edit anything what is in '{{ }}' or '{% %}'</p>"


    def __unicode__(self):
        return self.title


