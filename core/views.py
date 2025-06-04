# Create your views here.
import random

from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from item.models import Category, Item

from .forms import SignupForm

User = get_user_model()


def all_staff(request):
    items = Item.objects.filter(is_sold=False)
    categories = Category.objects.all()

    gender = ""
    if "gender" not in request.session:
        gender = "ALL"
    else:
        gender = request.session["gender"]

    if gender != "ALL":
        items = items.filter(gender=gender)

    return render(
        request,
        "core/index.html",
        {
            "categories": categories,
            "items": sorted(items, key=lambda x: random.random()),
            "name_category": "All stuff",
            "gender": gender,
            "show_login": True,
            "ajiogfjdhspgojdsapg": "xjcvxzklczxkc",
        },
    )


def index(request):
    items = Item.objects.filter(is_sold=False)
    categories = Category.objects.all()

    gender = ""
    if "gender" not in request.session:
        gender = "ALL"
    else:
        gender = request.session["gender"]

    if gender != "ALL":
        items = items.filter(gender=gender)

    return render(
        request,
        "core/index.html",
        {
            "categories": categories,
            "items": sorted(items, key=lambda x: random.random()),
            "name_category": "All stuff",
            "gender": gender,
            "show_login": True,
        },
    )


def category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    items = Item.objects.filter(category=category)
    categories = Category.objects.all()

    gender = ""
    if "gender" not in request.session:
        gender = "ALL"
    else:
        gender = request.session["gender"]

    if gender != "ALL":
        items = items.filter(gender=gender)

    return render(
        request,
        "core/index.html",
        {
            "categories": categories,
            "items": sorted(items, key=lambda x: random.random()),
            "name_category": category.name,
            "gender": gender,
            "query": category,
            "asdad21213": True,
        },
    )


def log_out(request):
    logout(request)
    return redirect("/")


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            if User.objects.filter(email=email).exists():
                form.add_error(
                    "email",
                    "email already exists, choose another email or u can auth from google",
                )
            else:
                user = form.save()

                user.backend = "django.contrib.auth.backends.ModelBackend"
                login(request, user)
                return redirect("/")
    else:
        form = SignupForm()

    return render(
        request,
        "core/signup.html",
        {
            "form": form,
            "show_login": True,
            "show_tab": False,
            "asdad21213": True,
            "zxcasdawd": "target-element",
        },
    )
