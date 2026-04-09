from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Auth — no token needed
    path('auth/register/', views.register_player),
    path('auth/login/',    views.login_player),
    path('auth/refresh/',  TokenRefreshView.as_view()),

    # Protected — token required
    path('score/save/',                 views.save_score),
    path('score/best/<int:player_id>/', views.get_best_score),
    path('session/save/',               views.save_session),
    path('session/<int:player_id>/',    views.get_sessions),
]