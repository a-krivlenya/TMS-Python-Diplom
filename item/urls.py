from django.urls import path

from . import views

app_name = "item"

urlpatterns = [
    path("<int:pk>", views.detail, name="detail"),
    path("", views.items, name="items"),
    path("<int:pk>/add", views.add, name="add"),
    path("<int:pk>/remove", views.remove, name="remove"),
    path("<int:pk>/remove_detail", views.remove_detail, name="remove_detail"),
    path("basket/", views.basket, name="basket"),
    path("gender/<str:gender>", views.gender_f, name="gender"),
    path("<str:gender>/<int:pk>", views.gender_detail_f, name="gender_detail"),
    path("delete", views.delete, name="delete"),
    path("purchase", views.purchase, name="purchase"),
    path("<int:pk>/purchase_delete", views.purchase_delete, name="purchase_delete"),
    path(
        "<int:pk>/purchase_delete_admin",
        views.purchase_delete_admin,
        name="purchase_delete_admin",
    ),
    path("all_purchases", views.all_purchases, name="all_purchases"),
    path("new_category", views.new_category, name="new_category"),
    path("new_item", views.new_item, name="new_item"),
    path("<int:pk>/remove_category", views.remove_category, name="remove_category"),
    path("<int:pk>/remove_item", views.remove_item, name="remove_item"),
    path("<int:pk>/edit_item", views.edit_item, name="edit_item"),
    path("<int:pk>/edit_category", views.edit_category, name="edit_category"),
    path("<int:pk>/new_comment", views.new_comment, name="new_comment"),
    path(
        "<int:pk_comment>/<int:pk_item>/delete_comment",
        views.delete_comment,
        name="delete_comment",
    ),
    path(
        "<int:pk_comment>/<int:pk_item>/edit_comment",
        views.edit_comment,
        name="edit_comment",
    ),
    path("all_comments", views.all_comments, name="all_comments"),
    path("gender_index/<str:gender>", views.gender_index, name="gender_index"),
    path("gender_detail/<str:gender>/<int:pk>", views.gender_detail, name="gender_detail"),
]
