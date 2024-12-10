from django.contrib import admin
from .models import Loan, Payment

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('id', 'borrower', 'loan_type', 'principal_amount', 'interest_rate', 'status')
    list_filter = ('status', 'loan_type', 'start_date')
    search_fields = ('borrower__user__username', 'loan_type__name')

@admin.register(Payment)
class LoanRepaymentAdmin(admin.ModelAdmin):
    list_display = ('loan', 'amount', 'date')