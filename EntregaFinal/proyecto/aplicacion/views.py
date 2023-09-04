from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from .models import Celular, TV, PC, Avatar
from .forms import TvForm, RegistroUsuariosForm, UserEditForm, AvatarFormulario
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView

# Create your views here.
def home(request):
    return render(request, "aplicacion/home.html")

def about(request):
    return render(request, "aplicacion/about.html")

@login_required
def celulares(request):
    contexto = {'celulares': Celular.objects.all()}
    return render(request, "aplicacion/celulares.html", contexto)

@login_required
def televisores(request):
    contexto = {'televisores': TV.objects.all}
    return render(request, "aplicacion/televisores.html", contexto)

@login_required
def computadoras(request):
    contexto = {'computadoras': PC.objects.all}
    return render(request, "aplicacion/computadoras.html", contexto)

@login_required
def celularesForm(request):
    if request.method == "POST":
        celulares = Celular(marca=request.POST['marca'],
                          modelo=request.POST['modelo'],
                          precio=request.POST['precio'])
        celulares.save()
        return HttpResponse ("Se grabó con éxito el celular!")
    return render(request,"aplicacion/celularesForm.html")

@login_required
def TvFormulario(request):
    if request.method == "POST":
        miForm= TvForm(request.POST)
        if miForm.is_valid():
            tv_marca = miForm.cleaned_data.get('marca')
            tv_modelo = miForm.cleaned_data.get('modelo')
            tv_pulgadas = miForm.cleaned_data.get('pulgadas')
            tv_precio = miForm.cleaned_data.get('precio')
            televisores = TV(marca=tv_marca,
                             modelo=tv_modelo,
                             pulgadas=tv_pulgadas,
                             precio=tv_precio)
            televisores.save()
            return render(request, "aplicacion/base.html")
    else: 
        miForm = TvForm()

    return render (request, "aplicacion/TVformulario.html", {"form": miForm})


def login_request(request):
    if request.method == "POST":
        miForm= AuthenticationForm(request, data=request.POST)
        if miForm.is_valid():
            usuario = miForm.cleaned_data.get('username')
            password = miForm.cleaned_data.get('password')
            user = authenticate(username=usuario, password=password)
            if user is not None: 
                login(request, user)

                try:
                    avatar = Avatar.objects.get(user=request.user.id).imagen.url
                except:
                    avatar = "media/avatares/default.png"
                finally:
                    request.session["avatar"] = avatar


                return render(request, "aplicacion/base.html", {'mensaje': f'Bienvenido al sitio {usuario}'})
            else:
                 return render(request, "aplicacion/login.html", {'form': miForm, 'mensaje':  'Los datos son inválidos'})
        else: 
            return render(request, "aplicacion/login.html", {'form': miForm, 'mensaje':  'Los datos son inválidos'})
    miForm = AuthenticationForm ()

    return render(request, "aplicacion/login.html", {'form': miForm })

def register(request):
    if request.method == "POST":
        miForm= RegistroUsuariosForm(request.POST)
        if miForm.is_valid():
            usuario = miForm.cleaned_data.get('username')
            miForm.save()
            return render(request, "aplicacion/base.html")
    else:
        miForm = RegistroUsuariosForm ()
    return render(request, "aplicacion/registro.html", {'form': miForm })

@login_required
def editarPerfil(request):
    usuario = request.user
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return render(request, "aplicacion/base.html")
    else:
        form = UserEditForm(instance=usuario)
    return render(request, "aplicacion/editarPerfil.html", {'form': form, 'usuario': usuario.username})


@login_required
def buscarCelular(request):
    return render (request, "aplicacion/buscarCelular.html")

@login_required
def buscar2(request):
    if request.GET['buscar']:
        patron = request.GET['buscar']
        celulares = Celular.objects.filter(marca__icontains=patron)
        contexto = {"celulares": celulares}
        return render(request, "aplicacion/celulares.html", contexto)
    return HttpResponse("No se buscó nada")

@login_required
def updateTelevisor(request, id_televisor):
    televisor = TV.objects.get(id=id_televisor)
    if request.method == "POST":
        miForm = TvForm(request.POST)
        if miForm.is_valid():
            televisor.marca = miForm.cleaned_data.get('marca')
            televisor.modelo = miForm.cleaned_data.get('modelo')
            televisor.pulgadas = miForm.cleaned_data.get('pulgadas')
            televisor.precio = miForm.cleaned_data.get('precio')
            televisor.save()
            return redirect(reverse_lazy('televisores'))
    else: 
        miForm = TvForm(initial={
            'marca': televisor.marca,
            'modelo': televisor.modelo,
            'pulgadas': televisor.pulgadas,
            'precio': televisor.precio,
        })
    return render(request, "aplicacion/TVformulario.html", {'form': miForm})

@login_required
def deleteTelevisor(request, id_televisor):
    televisor = TV.objects.get(id=id_televisor)
    televisor.delete()
    return redirect(reverse_lazy('televisores'))

@login_required
def createTelevisor(request):
    if request.method == "POST":
        miForm = TvForm(request.POST)
        if miForm.is_valid():
            p_marca = miForm.cleaned_data.get('marca')
            p_modelo = miForm.cleaned_data.get('modelo')
            p_pulgadas = miForm.cleaned_data.get('pulgadas')
            p_precio = miForm.cleaned_data.get('precio')
            televisor = TV(marca=p_marca, 
                             modelo=p_modelo,
                             pulgadas=p_pulgadas,
                             precio=p_precio,
                             )
            televisor.save()
            return redirect(reverse_lazy('televisores'))
    else: 
        miForm = TvForm()

    return render(request, "aplicacion/TVformulario.html", {'form': miForm})

#____________________ Class Based View

class ComputadoraList(LoginRequiredMixin, ListView):
    model = PC

class PCCreate(LoginRequiredMixin, CreateView):
    model = PC
    fields = ['marca', 'modelo', 'procesador', 'disco', 'pulgadas', 'precio']
    success_url = reverse_lazy('computadoras')

class UpdatePCView(LoginRequiredMixin, UpdateView):
    model = PC
    fields =  ['marca', 'modelo', 'procesador', 'disco', 'pulgadas', 'precio']
    success_url = reverse_lazy('computadoras')

class DeleteTelevisor(LoginRequiredMixin, DeleteView):
    model = PC
    success_url = reverse_lazy('computadoras')

@login_required
def agregarAvatar(request):
    if request.method == "POST":
        form = AvatarFormulario(request.POST, request.FILES)
        if form.is_valid():
            u = User.objects.get(username=request.user)
            avatar = Avatar(user=u, imagen=form.cleaned_data['imagen'])
            avatar.save() 

            imagen = Avatar.objects.filter(user=request.user.id).first().imagen.url
            request.session["avatar"] = imagen
            return render(request, "aplicacion/base.html")
    else:
        form = AvatarFormulario()
    return render(request, "aplicacion/agregarAvatar.html", {'form': form})