from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField

User = get_user_model()


class Bet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário da Aposta", related_name="bets")
    numbers = ArrayField(models.IntegerField(), verbose_name="Números da Aposta")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data da Aposta")

    def __str__(self):
        return f"{self.user.first_name} - {self.pk}"

    class Meta:
        verbose_name = 'Aposta'
        verbose_name_plural = 'Apostas'
        ordering = ['-created_at']
