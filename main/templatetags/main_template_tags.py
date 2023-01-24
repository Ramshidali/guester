from django.template import Library

register = Library()


@register.filter
def replace_underscore_upper(value):
    value = value.replace("_", " ").capitalize()
    return value

@register.filter
def to_fixed_two(value):
    return "{:10.2f}".format(value)

@register.filter
def split(value, seperator):
    if value:
        values = value.split(seperator)
        return list(filter(None, values))

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.copy()
    for key in kwargs:
        query[key] = kwargs[key]
    return query.urlencode()

