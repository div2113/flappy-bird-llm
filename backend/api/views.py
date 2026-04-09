from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Player, HighScore, GameSession
from .serializers import (PlayerSerializer,
                           HighScoreSerializer,
                           GameSessionSerializer)


# ── AUTH ─────────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([AllowAny])   # no token needed to register
def register_player(request):
    """Register a new player with username + password."""
    username = request.data.get('username', '').strip()
    password = request.data.get('password', '').strip()

    if not username or not password:
        return Response(
            {'error': 'Username and password required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already taken'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Create Django auth user
    user = User.objects.create_user(
        username=username,
        password=password
    )

    # Create linked Player profile
    player = Player.objects.create(username=username)

    # Generate JWT tokens immediately
    refresh = RefreshToken.for_user(user)

    return Response({
        'message':       'Player registered!',
        'player_id':     player.id,
        'username':      username,
        'access_token':  str(refresh.access_token),
        'refresh_token': str(refresh),
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])   # no token needed to login
def login_player(request):
    """Login and get JWT tokens."""
    username = request.data.get('username', '').strip()
    password = request.data.get('password', '').strip()

    user = authenticate(username=username, password=password)

    if not user:
        return Response(
            {'error': 'Invalid username or password'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # Get linked player profile
    try:
        player = Player.objects.get(username=username)
    except Player.DoesNotExist:
        return Response(
            {'error': 'Player profile not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    refresh = RefreshToken.for_user(user)

    return Response({
        'message':       'Login successful!',
        'player_id':     player.id,
        'username':      username,
        'access_token':  str(refresh.access_token),
        'refresh_token': str(refresh),
    })


# ── HIGH SCORE ───────────────────────────────────────────

@api_view(['POST'])
@permission_classes([IsAuthenticated])   # token required
def save_score(request):
    player_id = request.data.get('player_id')
    score     = request.data.get('score')

    if not player_id or score is None:
        return Response(
            {'error': 'player_id and score required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        player = Player.objects.get(id=player_id)
    except Player.DoesNotExist:
        return Response(
            {'error': 'Player not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    hs = HighScore.objects.create(player=player, score=score)
    return Response(
        HighScoreSerializer(hs).data,
        status=status.HTTP_201_CREATED
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_best_score(request, player_id):
    best = HighScore.objects.filter(
        player_id=player_id
    ).order_by('-score').first()

    if not best:
        return Response({'best_score': 0})
    return Response({'best_score': best.score})


# ── GAME SESSION ─────────────────────────────────────────

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_session(request):
    serializer = GameSessionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_sessions(request, player_id):
    sessions = GameSession.objects.filter(
        player_id=player_id
    ).order_by('-played_at')[:10]
    return Response(
        GameSessionSerializer(sessions, many=True).data
    )