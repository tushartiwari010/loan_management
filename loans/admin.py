from django.contrib import admin
from .models import LoanType, Borrower, Loan, Payment

admin.site.register(LoanType)
admin.site.register(Borrower)
admin.site.register(Loan)
admin.site.register(Payment)

