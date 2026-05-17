def serialize_game(game):

    return {

        "appid": game.appid,

        "name": game.name,

        "price": game.price,

        "release_date": game.release_date,

        "review_count": game.review_count,

        "revenue_1year": game.revenue_1year,

        "tags": [

            tag.name

            for tag in game.tags.all()
        ]
    }