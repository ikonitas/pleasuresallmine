# coding=utf-8

from core.views import home

class StaffMember(object):
    def process_request(self, request):
        if not request.user.is_active and not request.user.is_staff:
            return home(request)

    def process_response(self, request, response):
        return response

