from django.contrib import admin, messages
from .models import Article, Category, Platform


class AuthorFilter(admin.SimpleListFilter):
    title = "За авторством"
    parameter_name = "status"   # Произвольное название переменной которая будет принимать значения фильтраций

    def lookups(self, request, model_admin):
        return [
            ("no_attribution", "Без авторства"),   # Значения фильтров
            ("by", "За авторством"),
        ]

    def queryset(self, request, queryset):   # Получаем значение запроса
        # Если значение = выбранному фильтру, то мы возвращаем из связанной таблицы только те записи которые подходят по фильтраций
        if self.value() == "by":
            return queryset.filter(author__isnull=False)
        elif self.value() == "no_attribution":
            return queryset.filter(author__isnull=True)


# Register your models here.
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    fields = ["title", "text", "slug", "cat", "platform", "is_publising", "tags"]   # Отображаемые для редактирования поля
    #exclude = ["tags", "Is_publising"]   # Поля которые не будут добавлены в форму редктирования
    #readonly_fields = ["slug"]   # Поля доступные только для чтения
    prepopulated_fields = {"slug": ("title", )}   # ОБЯЗАТЕЛЬНО! Поле должно быть доступно для редактирования,
    # дублирует текст из одного поля в другое. С переводом?

    filter_horizontal = ["tags"]

    list_display = ('id', 'title', 'data_create', 'is_publising', "brief_info")
    list_display_links = ('id', )
    ordering = ['-data_create', 'title']
    list_editable = ('title', 'is_publising')   # Редактируемые поля, поле не должно быть в list_display_links
    list_per_page = 25  # Количество элементов на странице в админ панели
    actions = ["set_publising", "set_draft"]
    search_fields = ["title", "cat__name"]   # Обращаться напрямую к cat нельзя так как это внешний ключ, поэтому обращаемся к нужному полю через __
    list_filter = [AuthorFilter, "cat__name", "is_publising"]

    @admin.display(description="Длина статьи", ordering="text")   # Мы не можем делать явную сортировку по данному полю так как его не существует,
    # поэтому нужно делать ее в связке с полем модели
    def brief_info(self, brief: Article):   # brief: - название переменной, Article - зависит от модели
        return f"Статья содержит: {len(brief.text)} символов"

    @admin.action(description="Отметить опубликованные")
    def set_publising(self, request, queryset):
        count = queryset.update(is_publising=Article.Status.published)
        self.message_user(request, f"Опубликовано: {count} записей")

    @admin.action(description="Отметить черновики")
    def set_draft(self, request, queryset):
        count = queryset.update(is_publising=Article.Status.draft)
        self.message_user(request, f"Отменена публикация, {count} записей", messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


# admin.site.register(Article, ArticleAdmin)
# admin.site.register(Category)
# admin.site.register(Platform)