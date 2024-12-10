from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Home page
    path("", views.home, name="home"),  # This renders the home.html template

    # Loan-related URLs
    path("loans/", views.loan_list, name="loan_list"),  # List of all loans
    path("loans/<int:loan_id>/", views.loan_detail, name="loan_detail"),  # Detail of a specific loan
    path("loans/apply/", views.apply_loan, name="apply_loan"),  # Apply for a loan
    path('api/get-interest-rate/<int:loan_type_id>/', views.get_interest_rate, name='get_interest_rate'),
    path('loan/<int:loan_id>/repayment/', views.Payment, name='make_repayment'),
    
    # Authentication URLs
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="registration/logged_out.html"), name="logout"),
    path("register/", views.register, name="register"),  # User registration
]
