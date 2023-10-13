from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:pk>/detail', views.detailitem, name='detail'),
    path('create/', views.createitem, name='create'),
    path('<int:pk>/update/', views.updateitem, name='update'),
    path('<int:pk>/delete/', views.deleteitem, name='delete'),
    path('profile/', views.profile, name='profile'),
    path('<int:item_pk>/newchat/', views.newchat, name='newchat'),
    path('inbox/', views.inbox, name='inbox'),
    path('<int:pk>/detailchat/', views.detailchat, name='detailchat'),
]