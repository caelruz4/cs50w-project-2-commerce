# tuapp/context_processors.py

from django.contrib.auth.models import User
from .models import *

def global_variables(request):
    # Agrega las variables que deseas a este diccionario
    user = request.user if request.user.is_authenticated else None
    categories = Category.objects.all()

    return {
        'user': user,
        'categories': categories,
    }
