from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('send/', views.send_message, name='send_message'),
    path('new/', views.new_chat, name='new_chat'),
    path('history/', views.get_history, name='get_history'),
    path('sessions/', views.get_sessions, name='get_sessions'),
    path('session/<uuid:session_id>/', views.chat_view, name='chat_session'),
    path('session/<uuid:session_id>/delete/', views.delete_session, name='delete_session'),
]
