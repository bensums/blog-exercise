from django.http import HttpResponse

from google.appengine.api import users

def appengine_users(request):
    """
    Populate context with login url if not logged in or with logout url and
    user nickname if logged in.
    """

    user = users.get_current_user()
    if user:
        return {
            'user_nickname': user.nickname(),
            'logout_url': users.create_logout_url(request.build_absolute_uri())
        }
    else:
        return {
            'login_url': users.create_login_url(request.build_absolute_uri())
        }
