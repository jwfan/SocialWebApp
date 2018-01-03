from django.template import Variable, Library, Node, TemplateSyntaxError
from django.template.loader import render_to_string

from grumblr.models import *

register = Library()
def is_following(user, object):
    """
    Returns true if the given user is following the object

    ::

        {% if request.user|is_following:another_user %}
            You are already following {{ another_user }}
        {% endif %}
    """
    return user.profile.follower.filter(username=object).exists()

register.filter(is_following)