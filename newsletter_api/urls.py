from django.urls import path

from newsletter_api import views

app_name = 'newsletter_api'
urlpatterns = [
    path('', views.email_view, name='send_mail')
]