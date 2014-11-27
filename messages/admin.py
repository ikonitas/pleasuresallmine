from django.contrib import admin
from messages.models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ('message', 'is_active', 'modified_at', 'created_at',)

admin.site.register(Message, MessageAdmin)

