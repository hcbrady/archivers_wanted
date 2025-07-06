from django import template

register = template.Library()

@register.filter
def without(value_list, item_to_remove):
    """Returns the list without the given item."""
    return [item for item in value_list if item != item_to_remove]
