from django import template

register = template.Library()

@register.simple_tag(name="my_connection")
def connection_db(table,column):
    return "Read DB..."

@register.filter(name='my_name')
def name(value, surname):
    return "Andres Cruz Yoris "+surname+" "+value