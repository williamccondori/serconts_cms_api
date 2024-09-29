from django.contrib import admin
from .models import Publication, Category, Tag, Comment


class ModelBaseAdmin(admin.ModelAdmin):
    exclude = ('created_by', 'updated_by')

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Si es un objeto nuevo, se asigna el usuario como creador
            obj.created_by = request.user
        obj.updated_by = request.user  # Asigna siempre al usuario actual como actualizador
        super().save_model(request, obj, form, change)


@admin.register(Publication)
class PublicationAdmin(ModelBaseAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(ModelBaseAdmin):
    pass


@admin.register(Tag)
class TagAdmin(ModelBaseAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(ModelBaseAdmin):
    pass
