from django.contrib import admin
from technical_indicator.models import CompanyWiseResistancesSupports, CompanyWiseChartData, PreData

# Register your models here.

admin.site.register(CompanyWiseResistancesSupports)
admin.site.register(CompanyWiseChartData)
admin.site.register(PreData)
