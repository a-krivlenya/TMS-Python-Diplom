from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import LoginForm

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
    path("category/<int:category_id>", views.category, name="category"),
    path("signup/", views.signup, name="signup"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="core/login.html",
            authentication_form=LoginForm,
            extra_context={
                "show_login": True,
                "show_tab": False,
                "asdad21213": True,
                "zxcasdawd": "target-element",
            },
        ),
        name="login",
    ),
    path("logout/", views.log_out, name="logout"),
    path("all_staff/", views.all_staff, name="all_staff"),
]
