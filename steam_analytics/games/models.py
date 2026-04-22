from django.db import models

class Game(models.Model):
    appid = models.IntegerField(primary_key=True)
    name = models.CharField("Nome", max_length=255)
    price = models.FloatField("Preço", null=True)
    release_date = models.DateField("Data de lançamento", null=True)
    review_count = models.IntegerField("Avaliações", null=True)
    revenue_1year = models.FloatField("Receita (1 ano)", null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Jogo"
        verbose_name_plural = "Jogos"

class Tag(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name="Jogo")
    name = models.CharField("Tag", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

class Ranking(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name="Jogo")
    tag = models.CharField("Tag", max_length=100)
    type = models.CharField("Tipo", max_length=50)
    position = models.IntegerField("Posição")

    def __str__(self):
        return f"{self.game.name} - {self.tag} ({self.position})"

    class Meta:
        verbose_name = "Ranking"
        verbose_name_plural = "Rankings"