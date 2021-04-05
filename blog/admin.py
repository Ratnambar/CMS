from django.contrib import admin
from blog.models import Post
from blog.models import Category,ContactUs


# Register your models here.
admin.site.register((Post)),
admin.site.register(Category),
admin.site.register(ContactUs)

