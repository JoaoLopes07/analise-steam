from django.contrib import admin
from .models import Game, Tag, Ranking


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "review_count", "revenue_1year")
    search_fields = ("name",)
    list_filter = ("price",)
    ordering = ("-revenue_1year",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "game")
    search_fields = ("name",)


@admin.register(Ranking)
class RankingAdmin(admin.ModelAdmin):
    list_display = ("game", "tag", "type", "position")
    list_filter = ("type", "tag")