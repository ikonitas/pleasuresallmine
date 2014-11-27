# coding=utf-8

from messages.models import Message


def promotion_messages(request):
    message = Message.objects.order_by('?')[0]
    return {'promotion_message': message}
