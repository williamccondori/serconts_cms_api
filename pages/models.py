from django.contrib.auth import get_user_model  # Para obtener el modelo de usuario actual
from django.db import models
from django.utils.translation import gettext_lazy as _  # Para la traducción


class ModelBase(models.Model):
    status = models.BooleanField(default=True, verbose_name=_('Estado'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Fecha de creación'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Fecha de actualización'))
    created_by = models.ForeignKey(get_user_model(), null=True, blank=True, related_name='%(class)s_created_by',
                                   on_delete=models.SET_NULL, verbose_name=_('Creado por'))
    updated_by = models.ForeignKey(get_user_model(), null=True, blank=True, related_name='%(class)s_updated_by',
                                   on_delete=models.SET_NULL, verbose_name=_('Actualizado por'))

    class Meta:
        abstract = True
        verbose_name = _('Modelo Base')
        verbose_name_plural = _('Modelos Base')

    # Sobrescribir save() para actualizar 'updated_by'
    def save(self, *args, **kwargs):
        if not self.pk:  # Si es un objeto nuevo, se llena created_by
            self.created_by = kwargs.pop('user', None)
        self.updated_by = kwargs.pop('user', None)  # Actualiza el campo updated_by
        super().save(*args, **kwargs)


# Create your models here.
class Publication(ModelBase):
    title = models.CharField(max_length=200, verbose_name=_('Título'))
    content = models.TextField(verbose_name=_('Contenido'))
    image = models.ImageField(upload_to='publications', null=True, blank=True, verbose_name=_('Imagen'))
    video = models.FileField(upload_to='publications', null=True, blank=True, verbose_name=_('Video'))
    slug = models.SlugField(max_length=200, unique=True, verbose_name=_('Slug'))
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name=_('Categoría'))
    tags = models.ManyToManyField('Tag', blank=True, verbose_name=_('Etiquetas'))
    comments = models.ManyToManyField('Comment', blank=True, related_name='publications', verbose_name=_('Comentarios'))  # Agregué related_name aquí

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Publicación')
        verbose_name_plural = _('Publicaciones')


class Category(ModelBase):
    name = models.CharField(max_length=200, verbose_name=_('Nombre'))
    slug = models.SlugField(max_length=200, unique=True, verbose_name=_('Slug'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Categoría')
        verbose_name_plural = _('Categorías')


class Tag(ModelBase):
    name = models.CharField(max_length=200, verbose_name=_('Nombre'))
    slug = models.SlugField(max_length=200, unique=True, verbose_name=_('Slug'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Etiqueta')
        verbose_name_plural = _('Etiquetas')


class Comment(ModelBase):
    name = models.CharField(max_length=200, verbose_name=_('Nombre'))
    email = models.EmailField(verbose_name=_('Correo electrónico'))
    content = models.TextField(verbose_name=_('Contenido'))
    publication = models.ForeignKey('Publication', on_delete=models.CASCADE, verbose_name=_('Publicación'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Comentario')
        verbose_name_plural = _('Comentarios')
