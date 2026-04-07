from django.urls import path
from . import views

urlpatterns = [
    path('player/register/',views.register_player),
    path('score/save/', views.save_score),
    path('score/best/<int:player_id>/',views.get_best_score),
    path('session/save/',  views.save_session),
    path('session/<int:player_id>/', views.get_sessions),
]