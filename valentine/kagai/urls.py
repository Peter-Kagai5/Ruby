from django.urls import path
from . import views

app_name = 'kagai'

urlpatterns = [
    # Authentication
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Special Proposal
    path('valentine-proposal/', views.valentine_proposal, name='valentine_proposal'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Profile
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('browse/', views.browse_users, name='browse_users'),
    
    # Love Notes
    path('note/send/<str:recipient_username>/', views.send_note, name='send_note'),
    path('note/<int:note_id>/', views.view_note, name='view_note'),
    path('note/favorite/<int:note_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('notes/', views.my_notes, name='my_notes'),
    
    # Connections
    path('connect/<str:recipient_username>/', views.send_connection_request, name='send_connection_request'),
    path('connection/<int:connection_id>/accept/', views.accept_connection, name='accept_connection'),
    path('connection/<int:connection_id>/reject/', views.reject_connection, name='reject_connection'),
    path('connection/<int:connection_id>/remove/', views.remove_connection, name='remove_connection'),
]
