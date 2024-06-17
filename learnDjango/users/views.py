from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from .forms import LoginUserForm

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "users/login.html"

    # def get_success_url(self):
    #     return reverse_lazy("home")
    # Вместо этого используем константу в settings.py для перенаправленния на главную страницу LOGIN_REDIRECT_URL = "/"

# def login_users(request):
#     if request.method == "POST":   # Если метод передачи формы "Передача данных на сервер"
#         form = LoginUserForm(request.POST)   # Формируем обьект формы уже с заполненными данными - request.Post
#         if form.is_valid():   # Проверям корректность введеных данных
#             cd = form.cleaned_data   # Данные передаваемые в форме
#             user = authenticate(request, username=cd["username"], password=cd["password"])
#             if user and user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('home'))
#     else:
#         form = LoginUserForm()
#
#     return render(request, "users/login.html", {"form": form})


# def logout_users(request):
#     logout(request)
#     return HttpResponseRedirect(reverse('users:login'))