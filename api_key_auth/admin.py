from django.contrib import admin, messages
from .models import APIKey, Request

class APIKeyAdmin(admin.ModelAdmin):
    """
    Admin view for APIKey model.
    """
    list_display = ('id', 'name', 'email', 'created_at', 'modified_at')
    fieldsets = (
        ('Required', {'fields': ('name')}),
        ('Extra', {'fields': ('email',)}),
    )
    search_fields = ('name',)
    readonly_fields = ('created_at', 'modified_at')

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Only if new obj
            messages.add_message(request, messages.WARNING, (f'Your generated APIKey for {obj.name} is {obj.key}. You will not be able to view this again.'))
        super().save_model(request, obj, form, change)


class RequestAdmin(admin.ModelAdmin):
    """
    Admin view for Request model.
    """
    list_display = ('id', 'api_key', 'created_at')
    readonly_fields = ('api_key', 'created_at')

    def has_add_permission(self, request, obj=None):
        return False

admin.site.register(APIKey, APIKeyAdmin)
admin.site.register(Request, RequestAdmin)
