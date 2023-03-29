from django.db import models


class Location(models.Model):
    address = models.CharField('Адрес места', max_length=200, unique=True)
    lat = models.DecimalField('Широта', max_digits=9, decimal_places=6, null=True, blank=True)
    lon = models.DecimalField('Долгота', max_digits=9, decimal_places=6, null=True, blank=True)
    query_date = models.DateTimeField('Дата запроса')

    def __str__(self):
        return f'{self.address} {self.lat} {self.lon}'
