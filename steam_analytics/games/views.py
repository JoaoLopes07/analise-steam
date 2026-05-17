from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q

from .models import Game


def home(request):
    return render(request, "games/index.html")


def build_query(tags, operator="AND"):

    query = Q()

    if operator == "AND":

        first = True

        for tag in tags:

            condition = Q(
                tags__name__icontains=tag
            )

            if first:
                query = condition
                first = False
            else:
                query &= condition

    elif operator == "OR":

        for tag in tags:

            query |= Q(
                tags__name__icontains=tag
            )

    return query


def list_games(request):

    games = Game.objects.all()

    filter_tags = request.GET.get(
        "filter_tags",
        ""
    ).strip()

    include_groups = []

    exclude_groups = []

    # ==========================================
    # PARSER DOS FILTROS
    # ==========================================

    if filter_tags:

        groups = [
            group.strip()
            for group in filter_tags.split(";")
            if group.strip()
        ]

        for group in groups:

            parts = group.split(" ", 1)

            if len(parts) != 2:
                continue

            command = parts[0].strip().upper()

            tags_raw = parts[1]

            tags = [
                tag.strip()
                for tag in tags_raw.split(",")
                if tag.strip()
            ]

            # ======================================
            # INCLUDE_AND
            # ======================================

            if command == "INCLUDE_AND":

                include_groups.append(
                    build_query(tags, "AND")
                )

            # ======================================
            # INCLUDE_OR
            # ======================================

            elif command == "INCLUDE_OR":

                include_groups.append(
                    build_query(tags, "OR")
                )

            # ======================================
            # EXCLUDE_AND
            # ======================================

            elif command == "EXCLUDE_AND":

                exclude_groups.append(
                    build_query(tags, "AND")
                )

            # ======================================
            # EXCLUDE_OR
            # ======================================

            elif command == "EXCLUDE_OR":

                exclude_groups.append(
                    build_query(tags, "OR")
                )

    # ==========================================
    # APLICA INCLUDES
    # ==========================================

    if include_groups:

        include_query = Q()

        first = True

        for q in include_groups:

            if first:
                include_query = q
                first = False
            else:
                include_query |= q

        games = games.filter(include_query)

    # ==========================================
    # APLICA EXCLUDES
    # ==========================================

    for q in exclude_groups:

        games = games.exclude(q)

    games = games.distinct()

    # ==========================================
    # ORDENAÇÃO
    # ==========================================

    sort = request.GET.get(
        "sort",
        "revenue"
    )

    if sort == "reviews":

        games = games.order_by(
            "-review_count"
        )

    elif sort == "price":

        games = games.order_by(
            "-price"
        )

    elif sort == "release":

        games = games.order_by(
            "-release_date"
        )

    else:

        games = games.order_by(
            "-revenue_1year"
        )

    # ==========================================
    # PAGINAÇÃO
    # ==========================================

    try:

        page = int(
            request.GET.get("page", 1)
        )

    except:

        page = 1

    per_page = 20

    total = games.count()

    start = (page - 1) * per_page

    end = start + per_page

    games = games[start:end]

    # ==========================================
    # SERIALIZAÇÃO
    # ==========================================

    data = []

    for game in games:

        tags = list(
            game.tags.all().values_list(
                "name",
                flat=True
            )
        )

        data.append({

            "appid": game.appid,

            "name": game.name,

            "price": game.price,

            "release_date": game.release_date,

            "review_count": game.review_count,

            "revenue_1year":
                game.revenue_1year,

            "tags": tags,
        })

    return JsonResponse({

        "results": data,

        "page": page,

        "per_page": per_page,

        "total": total,

        "total_pages":
            (total + per_page - 1)
            // per_page,
    })