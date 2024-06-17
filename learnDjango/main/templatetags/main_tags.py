from django import template
import main.views as views
from django.db.models import Count

from main.models import Platform, Category, TagPost


register = template.Library()    # Декоратор для собственных тегов


@register.simple_tag()
def get_category():
    return views.category


@register.inclusion_tag('main/list_categories.html')
def show_category_list_categories(cat_selected_list_categories=0):
    categories_list_categories = Category.objects.annotate(total=Count("cat")).filter(total__gt=0)
    platform_list_categories = Platform.objects.annotate(total=Count("posts")).filter(total__gt=0)
    # С помощью annotate создаем доп вычислительное поле total, Count("posts") подсчитываем сколько всего статей в категорий или на платформе
    # filter(total__gt=0) получаем только те категорий или платформы где статей больше 0
    return {'categories_list_categories': categories_list_categories,
            'platform_list_categories': platform_list_categories,
            'cat_selected_list_categories': cat_selected_list_categories}


@register.inclusion_tag('main/list_categories.html')
def show_platform_list_categories(platform_selected_list_categories=0):   # platform_selected_personal - Зачем?
                                                            # Возможно для определения стилей при уже выбранной платформе,
                                                            # но в данный момент не работает
    platform_list_categories = Platform.objects.annotate(total=Count("posts")).filter(total__gt=0)
    return {'platform_list_categories': platform_list_categories, 'platform_selected_list_categories': platform_selected_list_categories}


@register.inclusion_tag('main/tags.html')
def show_all_tags():
    return {'tags': TagPost.objects.annotate(total=Count("tags")).filter(total__gt=0)}