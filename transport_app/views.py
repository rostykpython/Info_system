from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, FormView

from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect

from django.contrib.auth.views import LoginView, login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.db.models import Q

from requests import get
from .models import Orders, SalaryTax, CompanyTaxes, Workers, SummaryTaxes
from .forms import OrderForm


class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')


class RegisterPage(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super(RegisterPage, self).get(request, *args, **kwargs)


class HomePageView(TemplateView):
    template_name = 'home.html'


class OrdersView(LoginRequiredMixin, ListView):
    model = Orders
    template_name = 'orders.html'
    context_object_name = 'orders'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_area = self.request.GET.get('search_area', None)
        context['orders'] = context['orders'].order_by('is_completed')
        if search_area is not None:
            context['orders'] = context['orders'].filter(
                Q(delivery_city__icontains=search_area) |
                Q(delivery_address__icontains=search_area) |
                Q(shipping_city__icontains=search_area) |
                Q(shipping_address__icontains=search_area) |
                Q(name__icontains=search_area)
            )

        if self.request.user.is_staff:
            found_tags = [item.transport_type for item in context['orders']]
            context['filter_tags'] = sorted(set(found_tags))
            filtered_tags = [tag for tag in self.request.GET.keys()]
            if filtered_tags:
                context['orders'] = context['orders'].filter(transport_type__in=filtered_tags)
            return context

        context['orders'] = context['orders'].filter(user=self.request.user).order_by('-create_date')
        found_tags = [item.transport_type for item in context['orders'].order_by('-transport_type')]
        context['filter_tags'] = sorted(set(found_tags))

        filtered_tags = [tag for tag in self.request.GET.keys()]

        if filtered_tags:
            context['orders'] = context['orders'].filter(transport_type__in=filtered_tags)
        return context


class OrderDetail(LoginRequiredMixin, DetailView):
    model = Orders
    template_name = 'order_view.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super(OrderDetail, self).get_context_data(**kwargs)

        is_completed = self.request.GET.get('complete')

        if is_completed is not None:
            context['order'].is_completed = True
            context['order'].save()

        fuel_consumption_per_km = 0.1
        fuel_price = 50

        all_workers = Workers.objects.all()

        delivery_address = context['order'].delivery_address
        delivery_city = context['order'].delivery_city

        shipping_address = context['order'].shipping_address
        shipping_city = context['order'].shipping_city

        respons_distance = get(
            f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={delivery_city}%{delivery_address}&"
            f"destinations={shipping_city}%{shipping_address}&units=metrics&key=AIzaSyBIl7csQ6io8831"
            f"-S7V4ekuJ4aJmIwMivo "
        ).json()

        distance = respons_distance['rows'][0]['elements'][0]['distance']['value'] / 1000.0
        if context['order'].transport_type == 'lightweight':
            estimate_delivery_price = distance * fuel_consumption_per_km * fuel_price * 1.0
            profit = distance * fuel_consumption_per_km * fuel_price * 1.0 * 0.8

            estimate_delivery_price += profit

        elif context['order'].transport_type == 'halfweight':
            estimate_delivery_price = distance * fuel_consumption_per_km * fuel_price * 1.1
            profit = distance * fuel_consumption_per_km * fuel_price * 1.1 * 0.8

            estimate_delivery_price += profit
        else:
            estimate_delivery_price = distance * fuel_consumption_per_km * fuel_price * 1.2
            profit = distance * fuel_consumption_per_km * fuel_price * 1.2 * 0.8

            estimate_delivery_price += profit

        if context['order'].is_completed:
            percents_from_profit = 0

            if not context['order'].get_taxed:

                for worker in all_workers:

                    salary_per_order = (profit * 0.62) * worker.percent_from_order
                    percents_from_profit += salary_per_order
                    salary_tax = SalaryTax.objects.create(
                        ordrer_id=context['order'],
                        worker_id=worker,
                        salary_per_order=round(salary_per_order, 2),
                        tax_on_profit=round(salary_per_order * 0.18, 2),
                        military_tax=round(salary_per_order * 0.015, 2),
                        euv=round(salary_per_order * 0.22, 2)
                    )
                    salary_tax.save()

                company_tax = CompanyTaxes(
                    id=context['order'],
                    profit=round(profit-percents_from_profit, 2),
                    tax_on_profit=round(profit * 0.18, 2),
                    vat=round(profit * 0.2, 2)
                )
                company_tax.save()

                context['order'].get_taxed = True
                context['order'].save()

        context['price'] = round(estimate_delivery_price, 2)
        return context


class OrderCreate(LoginRequiredMixin, CreateView):
    model = Orders
    success_url = reverse_lazy('orders')
    template_name = 'order_create.html'
    form_class = OrderForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(OrderCreate, self).form_valid(form)


class OrderUpdate(LoginRequiredMixin, UpdateView):
    model = Orders
    success_url = reverse_lazy('orders')
    template_name = 'order_create.html'
    form_class = OrderForm


@login_required(redirect_field_name='login')
def delete_view(request, pk):
    obj = get_object_or_404(Orders, id=pk)
    obj.delete()
    return redirect('orders')


class Taxes(LoginRequiredMixin, ListView):

    model = SummaryTaxes
    template_name = 'generate_taxes.html'
    context_object_name = 'taxes'

    def get_context_data(self, **kwargs):
        context = super(Taxes, self).get_context_data(**kwargs)

        for tax in context['taxes']:
            month = tax.month
            context['month'] = SummaryTaxes.MONTHS[month][1]

        return context


class CreateTaxSummary(LoginRequiredMixin, CreateView):

    model = SummaryTaxes
    fields = ['day', 'month', 'year']
    template_name = 'create_tax.html'
    context_object_name = 'tax'
    success_url = reverse_lazy('taxes')


class TaxSummaryDetail(LoginRequiredMixin, DetailView):

    model = SummaryTaxes
    template_name = 'tax_view.html'
    context_object_name = 'tax'

    def get_context_data(self, **kwargs):
        context = super(TaxSummaryDetail, self).get_context_data(**kwargs)
        month = context['tax'].month
        year = context['tax'].year

        context['month'] = SummaryTaxes.MONTHS[month][1]

        summary_of_euv = 0
        summary_of_worker_tax = 0
        summary_of_profit = 0
        summary_of_vat = 0

        all_workers = Workers.objects.all()
        order_taxes_by_company = CompanyTaxes.objects.all().filter(create_date__gte=f'{year}-{month}-01',
                                                                   create_date__lt=f'{year}-{month+1}-01')

        worker_taxes = SalaryTax.objects.all().filter(
            date_added__gte=f'{year}-{month}-01',
            date_added__lt=f'{year}-{month+1}-01'
        )

        for worker in all_workers:
            euv_per_worker = worker.salary_per_month * 0.22
            summary_of_euv += euv_per_worker

        for order_tax in order_taxes_by_company:
            summary_of_profit += order_tax.tax_on_profit
            summary_of_vat += order_tax.vat

        for worker_tax in worker_taxes:
            summary_of_worker_tax += worker_tax.tax_on_profit + worker_tax.military_tax
            summary_of_euv += worker_tax.euv

        context['tax'].taxes_on_profit = summary_of_profit
        context['tax'].taxes_of_workers = summary_of_worker_tax
        context['tax'].summary_vat = summary_of_vat
        context['tax'].euv_of_workers = summary_of_euv
        context['tax'].save()

        return context


@login_required
def delete_tax_summary(request, pk):
    obj = get_object_or_404(SummaryTaxes, id=pk)
    obj.delete()
    return redirect('taxes')
