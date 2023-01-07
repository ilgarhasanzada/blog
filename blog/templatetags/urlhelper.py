from django.template import Library
from urllib import parse

register = Library()

@register.simple_tag
def edit_querystring(request, **kwargs):
    splitted = parse.urlsplit(request.get_full_path())
    querystring = dict(parse.parse_qsl(splitted.query))
    querystring.update(kwargs)
    new_querystring = parse.urlencode(querystring)
    return '?' + new_querystring
