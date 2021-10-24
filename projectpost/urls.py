from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import loginOrSignupView, loginView, signupView, profileView, setProfileView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('loginOrSignup/', loginOrSignupView, name='loginOrSignup'),
    path('login/', loginView, name='login'),
    path('signup/', signupView, name='signup'),
    #path('profile/<int:pk>', profileView, name='profile'),
    path('profile/<int:pk>', profileView, name='profile'),
    path('profile/', profileView, name='profile'),
    path('setProfile/<int:pk>', setProfileView, name='setProfile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)