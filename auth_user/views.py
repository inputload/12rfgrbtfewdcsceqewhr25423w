from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
# import pyshorteners
from .models import Url

User = get_user_model()


class RegisterView(View):
    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        user = User.objects.create_user(
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        login(request, user)
        return redirect('/')


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        user = authenticate(
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user:
            login(request, user)
            return redirect('/')
        return redirect('/login')


class IndexView(View):
    def get(self, request):
        return render(request, "index.html")

    def post(self, request):
        long_url = request.POST.get('url')
        # type_tiny = pyshorteners.Shortener()
        # short_url = type_tiny.tinyurl.short(long_url)

        url = Url.objects.create(
            long_url=long_url
        )
        short_url = f"http://{request.get_host()}/{url.short_code}"

        return render(request, "index.html", context={'url': short_url})


def logout_view(request):
    logout(request)
    return redirect('/')


def redirecter(request, short_code):
    url = Url.objects.filter(short_code=short_code)
    if url:
        return redirect(url.first().long_url)
    return HttpResponse("Url not found")
