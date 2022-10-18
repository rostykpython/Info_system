from django.contrib import admin
from .models import Orders, CompanyTaxes, Workers, SalaryTax

admin.site.register(Orders)
admin.site.register(CompanyTaxes)
admin.site.register(Workers)
admin.site.register(SalaryTax)
