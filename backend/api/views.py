from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Player, HighScore, GameSession
from .serializers import (PlayerSerializer,
                           HighScoreSerializer,
                           GameSessionSerializer)


# ── PLAYER ──────────────────────────────────────
@api_view(['POST'])
def register_player(request):
    """Create or get a player by username."""
    username = request.data.get('username', '').strip()
    if not username:
        return Response({'error': 'Username required'},
                        status=status.HTTP_400_BAD_REQUEST)

    player, created = Player.objects.get_or_create(username=username)
    return Response({
        'player': PlayerSerializer(player).data,
        'created': created
    }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


# ── HIGH SCORE ───────────────────────────────────
@api_view(['POST'])
def save_score(request):
    """Save a new high score for a player."""
    player_id = request.data.get('player_id')
    score     = request.data.get('score')

    if not player_id or score is None:
        return Response({'error': 'player_id and score required'},
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        player = Player.objects.get(id=player_id)
    except Player.DoesNotExist:
        return Response({'error': 'Player not found'},
                        status=status.HTTP_404_NOT_FOUND)

    hs = HighScore.objects.create(player=player, score=score)
    return Response(HighScoreSerializer(hs).data,
                    status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_best_score(request, player_id):
    """Get a player's personal best score."""
    best = HighScore.objects.filter(
        player_id=player_id
    ).order_by('-score').first()

    if not best:
        return Response({'best_score': 0})
    return Response({'best_score': best.score})


# ── GAME SESSION ─────────────────────────────────
@api_view(['POST'])
def save_session(request):
    """Save a full game session after death."""
    serializer = GameSessionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)
    return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_sessions(request, player_id):
    """Get all sessions for a player."""
    sessions = GameSession.objects.filter(
        player_id=player_id
    ).order_by('-played_at')[:10]   # last 10 games
    return Response(GameSessionSerializer(sessions, many=True).data)