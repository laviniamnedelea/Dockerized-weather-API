from django.db import models

class Tari(models.Model):
    nume_tara = models.CharField(max_length=50, unique=True)
    latitudine = models.FloatField()
    longitudine = models.FloatField()
    class Meta:
        db_table = 'Tari'

class Orase(models.Model):
    # id tara
    tara = models.ForeignKey('Tari', on_delete=models.CASCADE)
    nume_oras = models.CharField(max_length=50)
    latitudine = models.FloatField()
    longitudine = models.FloatField()
    class Meta:
        # name for table
        db_table = 'Orase'
        # unique constraints
        unique_together = ('tara','nume_oras')

class Temperaturi(models.Model):
    valoare = models.FloatField()
    # id oras
    oras = models.ForeignKey('Orase', on_delete=models.CASCADE)
    # auto-generated timestamp
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'Temperaturi'
        # unique constraint
        unique_together=('oras','timestamp')
