from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import redirect


def home(request):
    """Pagina principal de la aplicacion."""
    return render(request, 'home.html')


def signup(request):
    """Pagina de registro de usuario."""
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.save()
            login(request, user)
            return redirect('home')

        return render(request, 'signup.html', {
            'form': form, 'error': 'Error en el formulario'
        })


def signin(request):
    """Pagina de login de usuario."""
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')

        return render(request, 'signin.html', {
            'form': form, 'error': 'Error en los datos de acceso'
        })


def signout(request):
    """Pagina de logout de usuario."""
    logout(request)
    return render(request, 'home.html')
