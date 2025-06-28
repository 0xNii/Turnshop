from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='homepage'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('updateInfo',views.updateInfo,name='update'),
    path('edit',views.edit,name='edit'),
    path('subscribe',views.subscribe,name='subscribe')
]