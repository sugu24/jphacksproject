from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import loginOrSignupView, loginView, signupView, profileView, setProfileView, setReadBookView, recordBookView, setBookView, bookRankingView, impressionsView, questionRoomsView, booksImpressionsView, questionsView, qAndARoomView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('loginOrSignup/', loginOrSignupView, name='loginOrSignup'),
    path('login/', loginView, name='login'),
    path('signup/', signupView, name='signup'),
    path('profile/<int:pk>', profileView, name='profile'),
    path('profile/', profileView, name='profile'),
    path('setProfile/<int:pk>', setProfileView, name='setProfile'),
    path('setReadBook/', setReadBookView, name='setReadBook'),
    path('recordBook/<int:isbn>', recordBookView, name='recordBook'),
    path('setBook/<str:ibsn>/', setBookView, name='setBook'),
    path('bookRanking/', bookRankingView, name="bookRanking"),
    path('impressions/<int:isbn>', impressionsView, name="impressions"),
    path('questionRooms/', questionRoomsView, name="questionRoom"),
    path('booksImpressions/', booksImpressionsView, name="booksImpressions"),
    path('questions/<str:room>', questionsView, name="questions"),
    path('qAndARoom/<int:pk>', qAndARoomView, name="qAndARoom"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)