from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.template.defaultfilters import slugify
from .utils import make_thumbnail
from django.contrib.auth.models import User, AbstractUser, Permission
from django.db.models import Max

# define new storage for S3 bucket
from storages.backends.s3boto3 import S3Boto3Storage
class PublicStorage(S3Boto3Storage):
    default_acl = "public-read-write"

# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=60,verbose_name='Nombre de la Categoría', unique=True)
    slug = models.SlugField(max_length=100,unique=False, default=None, null=True)
    target = models.CharField(max_length=1,choices=[('M','Menú principal'),('S','Menú secundario')],default='S',verbose_name="Menu")
    visible = models.BooleanField(default=True,verbose_name='Visible')
    top_note = models.ForeignKey('Note',on_delete=models.DO_NOTHING, verbose_name="Nota destacada",blank=True, null=True)
    order = models.BigIntegerField(default=None, null=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        #save slug
        self.slug = slugify(self.name)
        super(Categories, self).save(*args, **kwargs)
    
class Colaborator(AbstractUser):
    class Meta:
        verbose_name = 'Colaborador'
        verbose_name_plural = 'Colaboradores'
    def __str__(self):
        return self.first_name if self.first_name!="" else self.username

class Tag(models.Model):
    name = models.CharField(max_length=250, verbose_name='tags disponibles')

    def __str__(self):
        return self.name
    

class Note(models.Model):
    title = models.CharField(max_length=120,verbose_name='Titulo', unique=True) 
    slug = models.SlugField(max_length=130, unique=False,default=None, null=True) 
    category = models.ForeignKey(Categories,on_delete=models.CASCADE, verbose_name="Categoría")
    resume = models.CharField(max_length=250,verbose_name='Subtitulo',default='')
    header_image = models.ImageField(upload_to='notes/headers', verbose_name='Imagen destacada')
    thumb_image = models.ImageField(upload_to='notes/headers/thumbs', verbose_name='Thumbnail')
    body = RichTextUploadingField(verbose_name='Contenido',default='',extra_plugins=['youtube'],
        external_plugin_resources=[(
            'youtube',
            '/static/ckeditor/ckeditor/plugins/youtube/',
            'plugin.js',
        )],)
    publish_at = models.DateTimeField(auto_now=True,verbose_name='Fecha de creación')  
    colaborator = models.ForeignKey(Colaborator, on_delete=models.CASCADE) 
    show_signed = models.BooleanField(default=False, verbose_name='Firma visible')
    top = models.BooleanField(default=False, verbose_name='Nota destacada en su categoría')
    tags = models.ManyToManyField(Tag, verbose_name="Tags", help_text="seleccione o cree un nuevo tag")
    enable_comments = models.BooleanField(default=True,verbose_name='Comentarios')
    last_notes = models.BooleanField(default=False,verbose_name='Incluir en ultimas noticias')
    main_note = models.BooleanField(default=False,verbose_name='Nota Principal')
    related_notes = models.ManyToManyField('self',verbose_name = 'Notas relacionadas', blank=True, null=True)
    top_order = models.BigIntegerField(default=None, null=True)
    category_order = models.BigIntegerField(default=None, null=True)
    

    class Meta:
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'
        
    def __str__(self):
        return self.title

    @staticmethod
    def removeItem(id,source):
        note = Note.objects.get(pk=id)
        if(source == 'lasts'):
            note.last_notes = False
            note.top_order = None
            reorder = Note.objects.filter(last_notes=True).exclude(pk=id).order_by('top_order')
            order_field = 'top_order'
        else:
            note.top = False
            note.category_order = None
            reorder = Note.objects.filter(category__slug=source).filter(top=True).exclude(pk=id).order_by('category_order')
            order_field = 'category_order'
        note.save()

        order = 1
        for n in reorder:
            setattr(n,order_field,order)
            n.save()
            order+=1
        return True

    def save(self, *args, **kwargs):
        #save slug
        self.slug = slugify(self.title)
        # save for image
        data = make_thumbnail(self.header_image)
        if(self.main_note):
            Note.objects.all().update(main_note=False)
        
        if(self.last_notes and not self.top_order):
            last_order = Note.objects.filter(last_notes=True).aggregate(Max('top_order'))['top_order__max']
            total = len(Note.objects.filter(last_notes=True))
            if(total>=6):
                first = Note.objects.filter(last_notes=True).order_by('top_order')[0]
                Note.removeItem(id=first.id,source='lasts')
                last_order=last_order - 1
            self.last_notes = True
            self.top_order = last_order+1 if last_order else 1
        if(self.top and not self.category_order):
            last_order_cat = Note.objects.filter(category=self.category).filter(top=True).aggregate(Max('category_order'))['category_order__max']
            total = len(Note.objects.filter(category=self.category).filter(top=True))
            if(total>=3):
                first = Note.objects.filter(category=self.category).filter(top=True).order_by('category_order')[0]
                Note.removeItem(id=first.id,source=self.category)
                last_order_cat=last_order_cat - 1
            self.top = True
            self.category_order = last_order_cat+1 if last_order_cat else 1
        if(data):
            self.thumb_image.save(data[0], data[1], save=False)

        # save for thumbnail and icon
        super(Note, self).save(*args, **kwargs)
    

class Banners(models.Model):

    popup_image = models.ImageField(upload_to="banners", verbose_name='imagen', null=True, blank=True)
    popup_link = models.URLField(null=True, blank=True, verbose_name='link')
    leaderboard_image = models.ImageField(upload_to="banners", verbose_name='imagen', null=True, blank=True)
    leaderboard_link = models.URLField(null=True,verbose_name='link', blank=True)
    skyscraper_image = models.ImageField(upload_to="banners", verbose_name='imagen', null=True, blank=True)
    skyscraper_link = models.URLField(null=True, verbose_name='link', blank=True)
    footbuttom_image = models.ImageField(upload_to="banners", verbose_name='imagen', null=True, blank=True)
    footbuttom_link = models.URLField(null=True,verbose_name='link', blank=True)
    prefooter_image = models.ImageField(upload_to="banners", verbose_name='imagen', null=True, blank=True)
    prefooter_link = models.URLField(null=True,verbose_name='link', blank=True)
    category = models.ForeignKey(Categories,on_delete=models.CASCADE,verbose_name="Categoria", blank=True, null=True, unique=True)
    visible = models.BooleanField(default=True, verbose_name='visible')

    def __str__(self):
        if(not self.category):
            return 'Noticia'
        return self.category.name
    
    class Meta:
        verbose_name = "Anuncios"
        verbose_name_plural = "Anuncios"
    
