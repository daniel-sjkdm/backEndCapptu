from django.db import models



class Coin(models.Model):
    book = models.CharField(max_length=10)
    created_at = models.DateTimeField()
    volume = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    last = models.FloatField(null=True, blank=True)
    vwap = models.FloatField(null=True, blank=True)
    ask = models.FloatField(null=True, blank=True)
    bid = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.pk}: {self.book} - {self.created_at}"