from django.urls import path, include
from .views import *
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('', home, name= "home" ), 
    path('celulares/', celulares, name= "celulares" ), 
    path('televisores/', televisores, name= "televisores" ), 
    path('about/', about, name= "about" ), 
    path('computadoras/', ComputadoraList.as_view(), name="computadoras" ),
    path('celulares_form/', celularesForm, name="celulares_form" ),
    path('TVformulario/', TvFormulario, name="TVformulario" ),

    path('buscar_celular/', buscarCelular, name="buscar_celular" ),
    path('buscar2/', buscar2, name="buscar2" ),

    path('login/', login_request, name="login" ),
    path('logout/', LogoutView.as_view(template_name= "aplicacion/logout.html"), name="logout" ),
    path('registro/', register, name="registro" ),
    path('editar_perfil/', editarPerfil, name="editar_perfil" ),
    path('agregar_avatar/', agregarAvatar, name="agregar_avatar" ),

    path('update_televisor/<id_televisor>/', updateTelevisor, name= "update_televisor" ), 
    path('delete_televisor/<id_televisor>/', deleteTelevisor, name= "delete_televisor" ), 
    path('create_televisor/', createTelevisor, name= "create_televisor" ), 

    path('update_pc/<int:pk>/', UpdatePCView.as_view(), name= "update_pc" ), 
    path('delete_pc/<int:pk>/', DeleteTelevisor.as_view(), name= "delete_pc" ), 
    path('create_pc/', PCCreate.as_view(), name= "create_pc" ), 

]