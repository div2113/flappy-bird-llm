from django.db import models

class Player(models.Model):
    username    = models.CharField(max_length=50, unique=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class HighScore(models.Model):
    player      = models.ForeignKey(Player, on_delete=models.CASCADE,
                                    related_name='scores')
    score       = models.IntegerField()
    achieved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score']   # highest first

    def __str__(self):
        return f"{self.player.username} → {self.score}"


class GameSession(models.Model):
    player        = models.ForeignKey(Player, on_delete=models.CASCADE,
                                      related_name='sessions')
    score         = models.IntegerField()
    pipes_passed  = models.IntegerField(default=0)
    death_reason  = models.CharField(max_length=50,
                                     choices=[
                                         ('pipe_top',    'Hit top pipe'),
                                         ('pipe_bottom', 'Hit bottom pipe'),
                                         ('ground',      'Hit ground'),
                                     ])
    duration_secs = models.FloatField(default=0)
    played_at     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player.username} | score={self.score} | {self.death_reason}"