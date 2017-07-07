from django.contrib import admin
from .hem_app.models import Category, ProductAssignment, Product

admin.site.register(Category)
admin.site.register(ProductAssignment)
admin.site.register(Product)