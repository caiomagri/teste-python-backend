from django.contrib import admin
from .models import Bet


class BetAdmin(admin.ModelAdmin):
    pass


admin.site.register(Bet, BetAdmin)
