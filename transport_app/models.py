from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Orders(models.Model):

    TYPE_OF_TRANSPORT = [
        ('lightweight', 'lightweight'),
        ('halfweight', 'halfweight'),
        ('heavyweight', 'heavyweight')
    ]

    UKRAINE_CITIES = [
        ('Ivano-Frankivsk', 'Ivano-Frankivsk'),
        ('Kiyv', 'Kiyv'),
        ('Lviv', 'Lviv'),
        ('Odessa', 'Odessa'),
        ('Chernivtsi', 'Chernivtsi'),
        ('Kherson', 'Kherson'),
        ('Zaporizhzhia', 'Zaporizhzhia'),
        ('Poltava', 'Poltava')
    ]

    id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)
    shipping_address = models.CharField(max_length=200)
    shipping_city = models.CharField(
        max_length=200,
        choices=UKRAINE_CITIES,
        default=UKRAINE_CITIES[0][0]
    )
    delivery_address = models.CharField(max_length=200)
    delivery_city = models.CharField(
        max_length=200,
        choices=UKRAINE_CITIES,
        default=UKRAINE_CITIES[0][0]
    )
    transport_type = models.CharField(
        max_length=200,
        choices=TYPE_OF_TRANSPORT,
        default=TYPE_OF_TRANSPORT[0][0]
    )
    datetime = models.DateField(auto_now_add=False)
    is_completed = models.BooleanField(default=False)
    get_taxed = models.BooleanField(default=False)
    add_info = models.TextField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)


class CompanyTaxes(models.Model):

    id = models.ForeignKey(Orders, primary_key=True, unique=True, on_delete=models.CASCADE)
    profit = models.FloatField(null=False, blank=False)
    tax_on_profit = models.FloatField(null=False, blank=False)
    vat = models.FloatField(null=False, blank=False)
    create_date = models.DateField(null=False, auto_now=True)


class Workers(models.Model):

    worker_id = models.BigIntegerField(primary_key=True, unique=True)
    worker_position = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200, null=False, blank=False)
    email = models.EmailField(null=True, blank=True)
    percent_from_order = models.FloatField(null=False, blank=False)
    salary_per_month = models.FloatField(null=False, blank=False)


class SalaryTax(models.Model):

    ordrer_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
    worker_id = models.ForeignKey(Workers, on_delete=models.CASCADE)
    salary_per_order = models.FloatField(null=False, blank=False)
    tax_on_profit = models.FloatField(null=False, blank=False)
    military_tax = models.FloatField(null=False, blank=False)
    euv = models.FloatField(null=False, blank=False)
    date_added = models.DateField(auto_now=True)


class SummaryTaxes(models.Model):

    MONTHS = (
        (1, 'January'),
        (2, 'February'),
        (3, 'March'),
        (4, 'April'),
        (5, 'May'),
        (6, 'June'),
        (7, 'July'),
        (8, 'August'),
        (9, 'September'),
        (10, 'October'),
        (11, 'November'),
        (12, 'December')
    )

    day = models.IntegerField(default=1, null=False)
    month = models.IntegerField(
        default=MONTHS[0][0],
        choices=MONTHS
    )
    year = models.IntegerField(null=False, default=timezone.now().year)
    taxes_on_profit = models.FloatField(null=True, blank=True)
    taxes_of_workers = models.FloatField(null=True, blank=True)
    summary_vat = models.FloatField(null=True, blank=True)
    euv_of_workers = models.FloatField(null=True, blank=True)
