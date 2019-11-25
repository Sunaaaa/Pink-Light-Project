from django.contrib import admin
from .models import Train, Notification

class TrainAdmin(admin.ModelAdmin):
    list_display = ['train_no', 'slot_no', 'seat_no']

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['content', 'created_at']

# Register your models here.
# admin.site.register(Train, TrainAdmin)
admin.site.register(Notification, NotificationAdmin)