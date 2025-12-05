from django.contrib import admin
from .models import Category, Dataset, DataPoint

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'description']

@admin.register(DataPoint)
class DataPointAdmin(admin.ModelAdmin):
    list_display = ['id', 'dataset', 'region', 'year', 'value']