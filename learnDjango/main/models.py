from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


class PublishedManager(models.Manager):   # Собственный менеджер вместо objects, опять же переусложнение
    def get_queryset(self):
        return super().get_queryset().filter(is_publising=Article.Status.published)


# -> str: ожидаемый результат который хотим получить на выходе
def translit(s: str) -> str:   # Перебираем строку s которую передаем в эту функцию
    # Или как вариант - from pytils.translit import slugify
    alph = {"а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e", "ж": "j", "з": "z", "и": "i",
            "й": "i", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t",
            "у": "u", "ф": "f", "х": "h", "ц": "c", "ч": "ch", "ш": "sh", "щ": "sh", "ь": "", "ы": "y", "ъ": "",
            "э": "r", "ю": "y", "я": "i"
    }
    return ''.join(map(lambda x: alph[x] if alph.get(x, False) else x, s.lower()))
    # верхняя lambda функция примерно соотвествует:
    # alph = {
    #     "а": "a", "б": "b", "в": "v", "г": "g",
    #     "д": "d", "е": "e", "ё": "e", "ж": "j",
    #     "з": "z", "и": "i", "й": "i", "к": "k",
    #     "л": "l", "м": "m", "н": "n", "о": "o",
    #     "п": "p", "р": "r", "с": "s", "т": "t",
    #     "у": "u", "ф": "f", "х": "h", "ц": "c",
    #     "ч": "ch", "ш": "sh", "щ": "sh",
    #     "ь": "", "ы": "y", "ъ": "",
    #     "э": "r", "ю": "y", "я": "i"
    # }
    #
    # string = "просто слово для перевода"
    #
    # strinh_eng = ""
    #
    # for i in string:
    #     if i in alph:
    #         el = alph.get(i)
    #         strinh_eng += el

    # map использует дочернюю функцию на любом обьекте к которому применим цикл for
    # double = lambda x: x*2
    # Эквивалентна:
    #
    # def double(x):
    # 		return x * 2


class Article(models.Model):
    class Status(models.IntegerChoices):   # Выбор вместо True, False, но зачем так усложнять?
        draft = 0, 'Черновик'
        published = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    text = models.TextField(blank=True)   # blank= позволяет не заполнять ячейку
    data_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    data_update = models.DateTimeField(auto_now=True)
    is_publising = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.published, verbose_name="Статус")

    author = models.OneToOneField("Author", on_delete=models.SET_NULL, null=True, blank=True, related_name="article")
    # Мы указываем связанную модель в "" как строку поскольку класс определяется ниже, если выше то просто пишем клосс связанной модели
    # related_name="article" менеджер по которому мы можем связывать таблицы

    tags = models.ManyToManyField('TagPost', blank=True, related_name="tags")

    platform = models.ForeignKey('Platform', on_delete=models.PROTECT, null=True, related_name='posts', verbose_name="Платформа")   # Связь многие к одному к таблице (Platform)
    # related_name='posts' без него выбор бы был через article_set
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name="cat", verbose_name="Категория")  # Связь многие к одному к таблице (Category)

    objects = models.Manager()
    publising = PublishedManager()

    def __str__(self):       # Прописываем отображение вывода, вместо objects, строку
        return self.title

    class Meta:        # Прописываем сортировку на уровне модели
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['-data_create']   # Сортировка от раньше к позже?
        indexes = [models.Index(fields=['-data_create'])]   # Индексация от раньше к позже?

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    # Данный метод нужен в том случае если поле не редактируемое, но обязательно для заполнения
    # Используем метод save() модели для автоматического генерированния слагов
    # def save(self, *args, **kwargs):   # Зачем мы передаем сюда параметры?
    #     self.slug = slugify(translit(self.title))   # Slugify метод который помогает сформировать slug. Использует только англ слова?
    #     super().save(*args, **kwargs)   # Ищет первый попавщийся метод?   Нужно для вызова метода из базового класса?


class Platform(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT)  # Связь многие к одному к таблице (Category)

    def __str__(self):
        return self.name

    class Meta:        # Прописываем сортировку на уровне модели
        verbose_name = "Платформа"
        verbose_name_plural = "Платформы"

    # Получаем путь из urls и передаем в него выбранный в данный момент слаг
    def get_absolute_url(self):
        return reverse('platform', kwargs={'platform_slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:  # Прописываем сортировку на уровне модели
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})


class TagPost(models.Model):
    tag = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)

    def __str__(self):
        return self.name