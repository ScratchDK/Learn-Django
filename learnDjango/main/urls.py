from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.main, name='home'),
    path('about/', views.about, name='about'),
    path('addpage/', views.addpage, name='addpage'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.show_post, name='post'),
    path('platform/<slug:platform_slug>', views.show_platform, name='platform'),
    path('category/<slug:category_slug>', views.show_category, name='category'),
    path('tag/<slug:tag_slug>', views.show_tags, name='tag'),
    path('test_tab', views.test_tab),
    # path('cats/<int:cat_id>/', views.category, name='cats_id'),
    # path('cats/<slug:cat_slug>/', views.category_by_slug, name='cats'),
    # re_path(r'^archive/(?P<year>[0-9]{4})/', views.archive, name='archive'),
]
