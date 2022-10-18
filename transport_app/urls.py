from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('orders', views.OrdersView.as_view(), name='orders'),

    path('order/<int:pk>/', views.OrderDetail.as_view(), name='order'),
    path('create-order/', views.OrderCreate.as_view(), name='create_order'),
    path('edit-order/<int:pk>/', views.OrderUpdate.as_view(), name='edit_order'),
    path('delete-order/<int:pk>', views.delete_view, name='delete_order'),

    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('register', views.RegisterPage.as_view(), name='register'),

    path('taxes/', views.Taxes.as_view(), name='taxes'),
    path('tax-create/', views.CreateTaxSummary.as_view(), name='create_tax'),
    path('tax-summary/<int:pk>', views.TaxSummaryDetail.as_view(), name='tax'),
    path('tax-summary-delete/<int:pk>', views.delete_tax_summary, name='delete_tax')
]
