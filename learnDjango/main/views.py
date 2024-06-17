from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify

from .models import Article, Category, Platform, TagPost

menu = ["О сайте", "Добавить статью", "Обратная связь", "Войти"]

menu_dict = [{"title": "О сайте", "url_name": "about"},
             {"title": "Добавить статью", "url_name": "addpage"},
             {"title": "Обратная связь", "url_name": "contact"},
             {"title": "Войти", "url_name": "login"}]

articles = [
    {"id": 1, "title": '''Кевин Файги советовал Хью Джекману не возвращаться к роли Росомахи — из-за концовки «Логана»''',
     "text": '''Самому же актёру хотелось показать новые стороны героя.
     <img src="https://leonardo.osnova.io/62fe1c64-ebcf-5f29-83b2-9113d3709966/-/preview/800x/-/format/webp" alt="">
      Свежий выпуск журнала Empire посвятили фильму «Дэдпул и Росомаха», и для него журналисты <a href="https://www.empireonline.com/movies/news/deadpool-wolverine-hugh-jackman-sides-we-havent-seen-before-exclusive/">пообщались</a> с авторами картины. Среди них оказался бессменный куратор киновселенной Marvel Кевин Файги. Продюсер рассказал, что заметно волновался из-за возвращения Хью Джекмана к роли Росомахи и даже советовал актёру не делать этого. По мнению Файги, у его персонажа в «Логане» оказался «величайший финал в истории», и в Marvel не хотели его «обнулять». В концовке картины Росомаха погибает, спасая X-23 и других детей-мутантов. Файги подтвердил, что в новом фильме покажут немного другую версию Росомахи, а не точно того же персонажа из прошлых фильмов про Людей Икс. В 2023-м режиссёр Шон Леви также говорил, что события «Логана» будут каноном для «Дэдпула и Росомахи». Самому же Джекману хотелось изучить новые стороны Росомахи, поэтому он недолго думал над предложением Райана Рейнольдса об участии в «Дэдпуле и Росомахе». К примеру, Джекман остался в восторге, что ему удастся надеть жёлтый костюм героя.''',
     "is_publising": True},
    {"id": 2, "title": "Статья 2", "text": "Немного текста для каждой статьи 2", "is_publising": True},
    {"id": 3, "title": "Статья 3", "text": "Немного текста для каждой статьи 3", "is_publising": True},
]

category = [{'id': '1', 'name': 'Игры'},
            {'id': '2', 'name': 'Музыка'},
            {'id': '3', 'name': 'Кино'},
]



class SimpleClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b


def main(request):
    # string = render_to_string("main/main.html")
    # return HttpResponse(string)

    # post = Article.objects.filter(is_publising=True)
    post = Article.publising.all().select_related("cat", "platform")
    # select_related("key1", "key2") - жадная загрузка связанных данных по внешнему ключу key, который имеет тип ForeignKey
    # prefetch_related("key1", "key2") - жадная загрузка связанных данных по внешнему ключу key, который имеет тип ManyToManyField
    # нужно для оптимизаций, убираем повторяющиеся запросы к БД

    data = {"title": "Главная страница сайта",
            'main_title': '',
            "menu": menu,
            "menu_dict": menu_dict,
            "float": 49.5,
            "list": [1, 2, True, "abc"],
            "class": SimpleClass(15, 20),
            "set": {1, 2, 5, 4, 5, 2, 9},
            "dict": {"key1": "value1",
                     "key2": "value2",},
            "slug": slugify("main page"),
            "articles": post,
            "cat_selected": 0,
            }

    return render(request, "main/main.html", context=data)


def show_post(request, post_slug):
    post = get_object_or_404(Article, slug=post_slug)    # Получить обьект или сгенерировать исключение 404

    data = {
        'title': post.title,
        'post': post,
        "menu_dict": menu_dict,
        "cat_selected": 1,
    }

    return render(request, "main/post.html", data)


def show_platform(request, platform_slug):
    platform = get_object_or_404(Platform, slug=platform_slug)   # Получаем из модели по флагу запись

    posts = Article.publising.filter(platform_id=platform.pk).select_related("platform")   # Отбираем статьи по платформам используя собственный менеджер

    data = {
        'main_title': f'Новости {platform.name}',
        "menu_dict": menu_dict,
        "articles": posts,
        # "platform_selected": platform.pk,
    }
    return render(request, "main/main.html", context=data)


def show_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)

    posts = Article.objects.filter(cat_id=category.pk).select_related("cat", "platform")

    data = {
        'main_title': f'Рубрика: {category.name}',
        "menu_dict": menu_dict,
        "articles": posts,
        # "cat_selected": category.pk,
    }
    return render(request, "main/main.html", context=data)


def addpage(request):
    return HttpResponse(f'Добавить статью')


def contact(request):
    return HttpResponse(f'Контактные данные')


def login(request):
    return HttpResponse(f'Авторизация')


@login_required
def about(request):
    return render(request, "main/about.html", {"title": "Об авторе", 'menu_dict': menu_dict,})


# def category(request, cat_id):
#     return HttpResponse(f'<h1>Статьи по категориям</h1><p>id: {cat_id}</p>')
#
#
# def category_by_slug(request, cat_slug):
#     return HttpResponse(f'<h1>Статьи по категориям</h1><p>slug: {cat_slug}</p>')
#
#
# def archive(request, year):
#     if year > 2023:
#         return redirect('cats', 'music', permanent=True)   # permanent=True - url постоянно перемещен по другому адресу
#         # raise Http404()
#
#     return HttpResponse(f'<h1>Архив по годам</h1><p>{year}</p>')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена!</h1>')

def show_tags(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)

    posts = tag.tags.filter(is_publising=Article.Status.published).prefetch_related("tags")   # Из с помощью менеджера tags который определен в
    # модели Article, tags = models.ManyToManyField('TagPost', blank=True, related_name="tags") мы получаем все связанные с этим тегом посты

    data = {
        "title": f"Тег: {tag.tag}",
        "menu": menu,
        "articles": posts,
    }

    return render(request, "main/main.html", context=data)


def test_tab(request):

    posts = Article.objects.all()
    count = len(posts)

    data = {
        "posts": posts,
        "count": count,
    }

    return render(request, "main/test_tab.html", context=data)