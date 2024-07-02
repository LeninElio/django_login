import uuid
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import JsonResponse
from django.urls import reverse
from oauth2_provider.decorators import protected_resource
from jwcrypto import jwk
from .forms import CustomUserCreationForm


def home(request):
    """Pagina principal de la aplicacion."""
    return render(request, 'home.html')


def signup(request):
    """Página de registro de usuario."""
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': CustomUserCreationForm()
        })

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
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


def load_public_key():
    """Load public key from file and return it as a JWK."""
    with open('/data/public_key.pem', 'rb') as pemfile:
        public_key = jwk.JWK.from_pem(pemfile.read())
        jwk_data = public_key.export(as_dict=True)
        jwk_data['use'] = 'sig'
        jwk_data['kid'] = str(uuid.uuid4())
        return {"keys": [jwk_data]}


@protected_resource()
@login_required
def userinfo(request):
    """Userinfo endpoint."""
    user = request.user
    return JsonResponse({
        'sub': user.username,
        'email': user.email,    
    })


def jwks(request):
    """JSON Web Key Set endpoint."""
    return JsonResponse(load_public_key())


def openid_configuration(request):
    """OpenID Connect configuration endpoint."""
    issuer = request.build_absolute_uri('/')[:-1]
    return JsonResponse({
        "issuer": issuer,
        "authorization_endpoint": issuer + reverse('oauth2_provider:authorize'),
        "token_endpoint": issuer + reverse('oauth2_provider:token'),
        "userinfo_endpoint": issuer + reverse('oauth2_provider:userinfo'),
        "jwks_uri": issuer + reverse('jwks'),
        "response_types_supported": ["code", "token", "id_token"],
        "subject_types_supported": ["public"],
        "id_token_signing_alg_values_supported": ["RS256"],
    })



@protected_resource()
def my_protected_view(request):
    """Protected resource."""
    return JsonResponse({'message': 'This is a protected resource'})
