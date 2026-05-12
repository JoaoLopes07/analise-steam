from django.shortcuts import render
from django.http import JsonResponse
from .models import Game


def home(request):
    return render(request, "games/index.html")


def list_games(request):
    games = Game.objects.all()

    include_any = request.GET.get("include_any", "").strip().lower()
    exclude_any = request.GET.get("exclude_any", "").strip().lower()

    # INCLUDE TAGS
    if include_any:
        include_tags = [
            tag.strip()
            for tag in include_any.split(",")
            if tag.strip()
        ]

        for tag in include_tags:
            games = games.filter(tag__name__icontains=tag)

    # EXCLUDE TAGS
    if exclude_any:
        exclude_tags = [
            tag.strip()
            for tag in exclude_any.split(",")
            if tag.strip()
        ]

        for tag in exclude_tags:
            games = games.exclude(tag__name__icontains=tag)

    games = games.distinct()

    # ORDENAÇÃO
    sort = request.GET.get("sort", "revenue")

    if sort == "reviews":
        games = games.order_by("-review_count")

    elif sort == "name":
        games = games.order_by("name")

    elif sort == "release":
        games = games.order_by("-release_date")

    else:
        games = games.order_by("-revenue_1year")

    # PAGINAÇÃO
    try:
        page = int(request.GET.get("page", 1))
    except:
        page = 1

    per_page = 20

    start = (page - 1) * per_page
    end = start + per_page

    total = games.count()

    games = games[start:end]

    data = []

    for game in games:
        tags = list(
            game.tag_set.values_list("name", flat=True)
        )

        data.append({
            "appid": game.appid,
            "name": game.name,
            "price": game.price,
            "release_date": game.release_date,
            "revenue_1year": game.revenue_1year,
            "review_count": game.review_count,
            "tags": tags,
        })

    return JsonResponse({
        "results": data,
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": (total + per_page - 1) // per_page
    })