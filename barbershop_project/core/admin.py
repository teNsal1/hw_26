from django.contrib import admin
from .models import Master, Service, Order, Review

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'experience', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'phone')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'is_popular')
    list_filter = ('is_popular',)
    search_fields = ('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'phone', 'status', 'appointment_date', 'master')
    list_filter = ('status', 'master')
    search_fields = ('client_name', 'phone')
    date_hierarchy = 'appointment_date'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'master', 'rating', 'created_at', 'is_published')
    list_filter = ('rating', 'is_published', 'master')
    search_fields = ('client_name', 'text')
    date_hierarchy = 'created_at'