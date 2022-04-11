from django import template
from app.models import *

register = template.Library()

@register.simple_tag()
def get_top_users():
    return Profile.top_users.all()

@register.simple_tag()
def get_top_tags():
    return Tag.top_tags.all()
