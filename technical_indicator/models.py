from django.db import models
from django.db.models import JSONField


class CompanyWiseChartData(models.Model):
    symbol = models.CharField(max_length=20, null=True, blank=True)
    last_price = JSONField(default=dict, blank=True, null=True)
    value = JSONField(default=dict, blank=True, null=True)
    date_n_time = models.DateTimeField(auto_now=True)


class CompanyWiseResistancesSupports(models.Model):
    symbol = models.CharField(max_length=20, null=True, blank=True)
    first_high_res = models.CharField(max_length=20, null=True, blank=True)
    sec_high_res = models.CharField(max_length=20, null=True, blank=True)
    thr_high_res = models.CharField(max_length=20, null=True, blank=True)
    first_high_res_oi = models.CharField(max_length=20, null=True, blank=True)
    sec_high_res_oi = models.CharField(max_length=20, null=True, blank=True)
    thr_high_res_oi = models.CharField(max_length=20, null=True, blank=True)
    high_chg_res_oi_price = models.CharField(max_length=20, null=True, blank=True)
    first_high_sup = models.CharField(max_length=20, null=True, blank=True)
    sec_high_sup = models.CharField(max_length=20, null=True, blank=True)
    thr_high_sup = models.CharField(max_length=20, null=True, blank=True)
    first_high_sup_oi = models.CharField(max_length=20, null=True, blank=True)
    sec_high_sup_oi = models.CharField(max_length=20, null=True, blank=True)
    thr_high_sup_oi = models.CharField(max_length=20, null=True, blank=True)
    high_chg_sup_oi_price = models.CharField(max_length=20, null=True, blank=True)
    date_n_time = models.DateTimeField(auto_now=True)


class PreData(models.Model):
    company = models.CharField(max_length=50, blank=True, null=True)
    date_time = models.DateTimeField(auto_now=True)
    pre_data = JSONField(default=dict, blank=True, null=True)


class LowMACDStocks(models.Model):
    company = models.CharField(max_length=50, blank=True, null=True)