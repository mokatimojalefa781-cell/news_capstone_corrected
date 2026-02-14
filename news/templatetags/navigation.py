from django import template

register = template.Library()

@register.filter(name="startswith")
def startswith(value, prefix):
    if value is None:
        return False
    return str(value).startswith(str(prefix))
