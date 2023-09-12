from django.urls import path,include
from . import views
urlpatterns = [
    # adding dashboard URLs
    path('', views.login, name='login'),
    path('dashboard/',views.dashboard, name='Dashboard'),
    path('register/', views.registration, name = 'Registration' ),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('signout/', views.signout, name='signout'),
    path('resetPassword/', views.resetPassword, name = 'resetPassword'),
    path('prediction/', views.prediction, name = 'prediction'),
    
]