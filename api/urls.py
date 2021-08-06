from django.urls import include, path
from rest_framework import routers
from . import views
from . import customAdminViews
from django.views.generic.base import RedirectView


#router = routers.DefaultRouter()
#router.register(r'notes', views.NoteViewSet, basename='notes')

urlpatterns = [
    path('', RedirectView.as_view(url='admin',permanent=True),name='index'),
    path('menu/', views.MenuList.as_view()),
    path('home/', views.HomeConfig.as_view()),
    path('notes/', views.NoteList.as_view()),
    path('note/<slug>', views.NoteRetrieve.as_view()),
    path('banner/<category__slug>', views.BannerRetrieveByCategory.as_view()),
    path('banner/', views.BannerRetrieveNotes.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/home/save', customAdminViews.homeAdd,name="home-save"),
    path('admin/home/del', customAdminViews.homeRemove,name="home-del"),
    path('admin/home/reorder', customAdminViews.homeReorder,name="home-order"),
    path('admin/menu/reorder', customAdminViews.menuReorder,name="menu-order"),
    path('admin/menu/first', customAdminViews.firstOrder),
    path('reorder', customAdminViews.reorder),
    path('depure', customAdminViews.depureBanners),
    path('instagram-data', views.InstagramRetrieveData.as_view()),
]