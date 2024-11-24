from django.db import models

# Create your models here.
class ExchangeRate(models.Model):
    cur_unit = models.CharField(max_length=150)
    search_date = models.DateField()
    cur_nm = models.TextField()
    deal_bas_r = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)