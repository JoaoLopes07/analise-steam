from django.db import models


class Game(models.Model):

    appid = models.IntegerField(primary_key=True)

    name = models.CharField(max_length=255)

    price = models.FloatField(null=True)

    release_date = models.DateField(null=True)

    review_count = models.IntegerField(null=True)

    revenue_1year = models.FloatField(null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):

    game = models.ForeignKey(
        Game,
        related_name="tags",
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Ranking(models.Model):

    game = models.ForeignKey(
        Game,
        related_name="rankings",
        on_delete=models.CASCADE
    )

    tag = models.CharField(max_length=100)

    type = models.CharField(max_length=50)

    position = models.IntegerField()

    def __str__(self):
        return f"{self.game.name} - {self.tag}"