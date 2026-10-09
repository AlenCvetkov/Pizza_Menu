from django.contrib import admin
from .models import Topping, Pizza, Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['pizza', 'chef', 'status', 'order_time']

    # 1. Доделување на најавениот корисник како одговорен при креирање
    def save_model(self, request, obj, form, change):
        if not change:
            obj.chef = request.user
        super().save_model(request, obj, form, change)

    # 2. Лекарите ги гледаат само прегледите каде се одговорни или асистенти
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        chef_qs = qs.filter(chef=request.user)
        assistant_qs = qs.filter(assistants=request.user)
        return (chef_qs | assistant_qs).distinct()

    # 3. Избриши може само ако прегледот е незапочнат (status == 'scheduled')
    def has_delete_permission(self, request, obj=None):
        if obj and obj.status != 'scheduled':
            return False
        return super().has_delete_permission(request, obj)

    # 4. Менување е дозволено само за одговорниот или супер-корисник (од барањата на испитот)
    def has_change_permission(self, request, obj=None):
        if obj and not request.user.is_superuser and obj.chef != request.user:
            return False
        return super().has_change_permission(request, obj)


@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if not request.user.is_superuser:
            return False
        return super().has_add_permission(request)


@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if not request.user.is_superuser:
           return False
        return super().has_add_permission(request)