from rest_framework import serializers
from .models import Player, HighScore, GameSession

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Player
        fields = ['id', 'username', 'created_at']

class HighScoreSerializer(serializers.ModelSerializer):
    player_name = serializers.CharField(source='player.username',
                                        read_only=True)
    class Meta:
        model  = HighScore
        fields = ['id', 'player_name', 'score', 'achieved_at']

class GameSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model  = GameSession
        fields = ['id', 'player', 'score', 'pipes_passed',
                  'death_reason', 'duration_secs', 'played_at']