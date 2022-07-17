from django import template
from main.models import *


register = template.Library()


@register.inclusion_tag('main/list_categories.html')
def get_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)
    return {"cats": cats, "cat_selected": cat_selected}
