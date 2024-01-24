from django.urls import path
from . import views

app_name='comments'
urlpatterns = [
    path('add', views.add, name='add'),
    path('contact', views.contact, name='contact'),
    path('', views.index, name='index'),
    path('update/<int:pk>', views.update, name='update'),
    path('delete/<int:pk>', views.delete, name='delete')
]