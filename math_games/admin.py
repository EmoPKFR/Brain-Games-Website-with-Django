from django.contrib import admin
from .models import GameLevel, GameScore

@admin.register(GameScore)
class GameScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'highest_score', 'date')
    search_fields = ('user__username', 'level__name')

admin.site.register(GameLevel)