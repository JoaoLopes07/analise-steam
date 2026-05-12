import os
import django
import argparse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'steam_analytics.settings')
django.setup()

from games.models import Game


def query_games(include_all, include_any, exclude_any):
    games = Game.objects.all()

    if include_all:
        for tag in include_all:
            games = games.filter(tag__name=tag)

    if include_any:
        games = games.filter(tag__name__in=include_any)

    if exclude_any:
        games = games.exclude(tag__name__in=exclude_any)

    return games.distinct()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--include-all", type=str, default="")
    parser.add_argument("--include-any", type=str, default="")
    parser.add_argument("--exclude-any", type=str, default="")

    args = parser.parse_args()

    include_all = [t.strip() for t in args.include_all.split(",") if t]
    include_any = [t.strip() for t in args.include_any.split(",") if t]
    exclude_any = [t.strip() for t in args.exclude_any.split(",") if t]

    games = query_games(include_all, include_any, exclude_any)

    for g in games:
        print(g.name)