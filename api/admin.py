from django.contrib.admin import AdminSite, ModelAdmin, HORIZONTAL
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.html import format_html
from tags_input import admin as tags_input_admin
from PIL import Image
from django.urls import path
from django.contrib.auth.models import Group
from django.template.response import TemplateResponse
from admin_views.admin import AdminViews
from django import forms
from .models import *

class MyAdminSite(AdminSite):
    site_header = 'GONEWS'
    site_title = 'Gonews - Administrativo'
    site_url = 'https://gonews-front.herokuapp.com/'


    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('home/', self.admin_view(self.my_view),name="home"),
            path('menu/', self.admin_view(self.menu_view),name="menu"),
        ]
        return urls + my_urls

    def my_view(self, request):
        main = Note.objects.filter(main_note=True)[0:1]
        last = Note.objects.filter(last_notes=True).order_by('-top_order')
        listado = [
            {
                'name':'Nota Destacada',
                'slug':'main',
                'note_set':main,
                'candidates':Note.objects.filter(main_note=False)
            },
            {
                'name':'Ultimas noticias',
                'slug':'lasts',
                'note_set':last,
                'candidates':Note.objects.filter(last_notes=False).order_by('-publish_at')
            },
        ]

        for category in Categories.objects.all():
            listado.append({
                'name':category.name,
                'slug':category.slug,
                'note_set':category.note_set.filter(top=True).order_by('-category_order'),
                'candidates':category.note_set.filter(top=False).order_by('-publish_at')
            })


        context = dict(
           # Include common variables for rendering the admin template.
           self.each_context(request),

           # Anything else you want in the context...
           headers = ['noticia','categoria','orden','eliminar'],
           categories  = listado
        )

        return TemplateResponse(request, "admin/home_list_changes.html", context)

    def menu_view(self, request):
        
        main = Categories.objects.filter(target='M').order_by('order')
        second = Categories.objects.filter(target='S').order_by('order')
        listado = [
            {
                'name':'Menu Principal',
                'slug':'M',
                'note_set':main
            },
            {
                'name':'Menu Secundario',
                'slug':'S',
                'note_set':second
            },
        ]

        context = dict(
           # Include common variables for rendering the admin template.
           self.each_context(request),

           # Anything else you want in the context...
           headers = ['Nombre de la Categoría','Visibilidad','Orden de visibilidad'],
           categories  = listado
        )

        return TemplateResponse(request, "admin/menu_list_changes.html", context)


admin_site = MyAdminSite(name='gonews')
# Register your models here.

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Nombre Completo")

    class Meta:
        model = User
        fields = ("username", "first_name", "email", )

class ColaboratorAdmin(ModelAdmin):
    list_display = ('username','email')
    search_fields = ('username','username')
    form = RegisterForm
    list_per_page = 10
    preserve_filters=True
    def save_model(self, request, obj, form, change):
        obj.is_staff = True
        super().save_model(request, obj, form, change)
        my_group = Group.objects.get(name='Colaborador') 
        my_group.user_set.add(obj)
        my_group.save()

class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        #rint(self.fields)
        #if self.instance.note:
        self.fields['top_note'].queryset = Note.objects.filter(category__id=self.instance.id)
    
    
class CategoryAdmin(ModelAdmin):
    class Media:
        js = ('admin/js/autosave.js',)

    form = CategoryForm
    
    def delete_button(self, obj):
        return format_html('<a class="btn" href="/admin/api/categories/{}/delete/"><img src="/static/admin/img/trash.png"></a>', obj.id)
    
    def get_changelist_form(self, request, **kwargs):
        return CategoryForm
    
    def formfield_for_dbfield(self, *args, **kwargs):
        formfield = super().formfield_for_dbfield(*args, **kwargs)

        formfield.widget.can_delete_related = False
        formfield.widget.can_change_related = False
        formfield.widget.can_add_related = False

        return formfield

    exclude = ('visible','slug')
    list_display = ('name','visible', 'target','top_note','delete_button')

    search_fields = ('name',)
    list_editable = ('visible','top_note','target')
    list_per_page = 10
    preserve_filters=True
    radio_fields = {"target": HORIZONTAL}
    fields = (
        'name',
        'target',
        'top_note'
    )

    

class NoteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        #if self.instance.note:
        #self.fields['top_note'].queryset = Note.objects.filter(category__id=self.instance.id)
    resume = forms.CharField(
        widget = forms.Textarea()
    )
    
    
    class Meta:
        model = Note
        exclude = ('publish_at','thumb_image','slug')
        

class NoteAdmin(tags_input_admin.TagsInputAdmin):
    
    def eliminar(self, obj):
        return format_html('<a class="btn" href="/admin/api/note/{}/delete/"><img src="/static/admin/img/trash.png"></a>', obj.id) 
    
    def noticia(self, obj):
        return obj.title

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or obj.colaborator == request.user if obj else False
    
    def has_delete_permission(self,request,obj=None):
        return request.user.is_superuser or obj.colaborator == request.user if obj else False

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "colaborator":
            if(not request.user.is_superuser):
                kwargs["queryset"] = Colaborator.objects.filter(pk=request.user.id)
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_dbfield(self, *args, **kwargs):
        formfield = super().formfield_for_dbfield(*args, **kwargs)

        formfield.widget.can_delete_related = False
        formfield.widget.can_change_related = False
        formfield.widget.can_add_related = False

        return formfield
            

    # def has_add_permission(self,request):
    #     return False
    
    # exclude = ('slug',)
    search_fields = ('title',)
    list_per_page = 10
    list_display = ('noticia','category','publish_at','eliminar')
    raw_id_fields = ('tags','related_notes')
    form = NoteForm
    preserve_filters=True
    fieldsets = (
            (
                None,
                {
                    'fields' : (
                        'title',
                        'category',
                        'resume',
                        'header_image',
                        'body',
                        ('colaborator','show_signed','top'),
                        ('main_note','last_notes'),
                        'tags',
                        
                    )
                }
            ),
            (
                None,
                {
                    'fields': (
                        'related_notes',
                        'enable_comments'
                    )
                }
            )
        )

class BannerForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Categories.objects.all(), empty_label='Noticias', required=False)

class BannersAdmin(ModelAdmin):
    
    form = BannerForm
    def display_name(self,object):
        if (not object.category):
            return 'Noticia'

        return object.category
    
    banners = {'popup_link':'PopUp','leaderboard_link':'Leaderboard','skyscraper_link':'Skyscraper','footbuttom_link':'pie de boton','prefooter_link':'social area'}
    def banners_list(self,object):
        listado = ""
        for (key,name) in self.banners.items():
            if(getattr(object,key)):
                listado += name+", "
        return listado
            
    list_display = ('display_name','banners_list','visible')
    list_display_links = ('banners_list','display_name')
    list_editable = ('visible',)
    fieldsets = (
        (None,{'fields':('category',)}),
        (
            'Anuncios:  (Pop up)',
            {
                'fields': (
                    'popup_image',
                    'popup_link'
                )
            }
        ),
        (
            'Anuncios: \n (Leaderboard)',
            {
                'fields': (
                    'leaderboard_image',
                    'leaderboard_link'
                )
            }
        ),
        (
            'Anuncios: \n (Skyscraper)',
            {
                'fields': (
                    'skyscraper_image',
                    'skyscraper_link'
                )
            }
        ),
        (
            'Anuncios: \n (boton de pie)',
            {
                'fields': (
                    'footbuttom_image',
                    'footbuttom_link'
                )
            }
        ),
        (
            'Anuncios: \n (pre-footer) \n solo visible en HOME',
            {
                'fields': (
                    'prefooter_image',
                    'prefooter_link'
                )
            }
        )
    )



admin_site.register(Categories,CategoryAdmin)
admin_site.register(Colaborator,ColaboratorAdmin)
admin_site.register(Note,NoteAdmin)
admin_site.register(Banners,BannersAdmin)
# admin_site.register(Group)
# admin_site.register(Tag)

# 306x225
# 1440x813
