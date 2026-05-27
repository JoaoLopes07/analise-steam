import json

from django.test import TestCase


class ListGamesAPITest(TestCase):

    fixtures = ["test_games.json"]

    def test_basic_list_returns_200_with_expected_shape(self):
        response = self.client.get("/api/games/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Type"], "application/json"
        )

        data = json.loads(response.content)

        for key in ("results", "page", "per_page", "total", "total_pages"):
            self.assertIn(key, data, msg=f"Missing key: {key}")

        self.assertEqual(data["total"], 2)

        expected_fields = {
            "appid", "name", "price", "release_date",
            "review_count", "revenue_1year", "tags",
        }
        for item in data["results"]:
            self.assertEqual(set(item.keys()), expected_fields)
            self.assertIsInstance(item["tags"], list)
            for tag in item["tags"]:
                self.assertIsInstance(tag, str)
