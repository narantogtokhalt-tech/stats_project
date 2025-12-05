from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse  # ✅ Add this

def home(request):  # ✅ This is your homepage
    return HttpResponse("✅ Django backend is running!")

urlpatterns = [
    path('', home),  # ✅ Add this line for homepage
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
