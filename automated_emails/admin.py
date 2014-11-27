from django.contrib import admin
from automated_emails.models import AutomatedEmail
from django.forms import Textarea
from django.db import models

class AutomatedEmailAdmin(admin.ModelAdmin):
    list_display = ('title','is_active',)

    formfield_overrides = {
            models.TextField: {'widget':Textarea(attrs={'rows':40,'cols':120})},
            }

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('title',) + self.readonly_fields
        return self.readonly_fields

admin.site.register(AutomatedEmail, AutomatedEmailAdmin)

