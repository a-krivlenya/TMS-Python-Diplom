from django.contrib.auth.models import User
from django.db import models

gender_choice = {
    "M": "Man",
    "W": "Woman",
}


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField()

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.description


class Item(models.Model):
    category = models.ForeignKey(Category, related_name="items", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    image = models.ImageField(upload_to="item_images", blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(User, related_name="items", blank=True)
    gender = models.CharField(max_length=10, choices=gender_choice)
    comments = models.ManyToManyField(Comment)

    def __str__(self):
        return self.name


class Purchase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)
    telegram = models.CharField(max_length=255)
    price = models.FloatField()
