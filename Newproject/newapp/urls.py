from django.urls import path , include
from . import views

urlpatterns = [

    path('AddUser/', views.Adduser , name='Adduser'),
    path('getalluser/', views.getalluser, name='getalluser'),
    path('Login/', views.Login , name='Login'),

    #Crud for client

    path('addclient/', views.addclient, name='addclient'),
    path('getallclients/', views.getallclients , name='getallclients'),
    path('getclients/<int:id>', views.getclients , name='getclients'),
    path('updateclient/<int:id>', views.updateclient, name='updateclient'),
    path('deleteclient/<int:id>', views.deleteclient, name='deleteclient'),
    path('client/<int:id>/projects', views.CreateProject, name='deleteclient'),

    path('getprojects/', views.getprojects, name='getprojects')

]