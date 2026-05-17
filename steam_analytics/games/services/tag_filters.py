from django.db.models import Q


def apply_tag_filters(games, filter_string):

    groups = filter_string.split(";")

    for group in groups:

        group = group.strip()

        if not group:
            continue

        try:

            command, tags_raw = group.split(" ", 1)

        except ValueError:

            continue

        tags = [

            tag.strip()

            for tag in tags_raw.split(",")

            if tag.strip()
        ]

        if command == "INCLUDE_AND":

            for tag in tags:

                games = games.filter(
                    tags__name__icontains=tag
                )

        elif command == "INCLUDE_OR":

            query = Q()

            for tag in tags:

                query |= Q(
                    tags__name__icontains=tag
                )

            games = games.filter(query)

        elif command == "EXCLUDE_OR":

            query = Q()

            for tag in tags:

                query |= Q(
                    tags__name__icontains=tag
                )

            games = games.exclude(query)

        elif command == "EXCLUDE_AND":

            for tag in tags:

                games = games.exclude(
                    tags__name__icontains=tag
                )

    return games.distinct()