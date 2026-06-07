from django.contrib import admin
from .models import Profile, Rating

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'location', 'created_at']

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['reviewer', 'reviewed', 'stars', 'auction', 'created_at']
    list_filter = ['stars']
    search_fields = ['reviewer__username', 'reviewed__username']
    readonly_fields = ['created_at']
