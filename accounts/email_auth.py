from django.contrib.auth.models import User

class EmailBackend(object):
    """
    Authenticate against email and password
    """
    def authenticate(self, username=None, password=None):
        try:
            username = username.lower()
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            user = None

        if user is not None and user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
