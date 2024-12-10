from django.db import models
from django.contrib.auth.models import User
from math import ceil

class LoanType(models.Model):
    name = models.CharField(max_length=50)
    interest_rate = models.FloatField()
    max_duration_months = models.IntegerField()

    def __str__(self):
        return self.name

class Borrower(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.user.username

class Loan(models.Model):
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    loan_type = models.ForeignKey(LoanType, on_delete=models.SET_NULL, null=True)
    principal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    duration_months = models.IntegerField()
    start_date = models.DateField()
    amount_repaid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')])

    
    def monthly_installment(self):
        # Using a simple calculation for installment (not compound interest)
        total = self.total_repayment()
        return ceil(total / self.duration_months)

    def total_repayment(self):
        # Compound interest formula: A = P * (1 + r/n)^(n*t)
        # Here, n=12 (monthly compounding), t=duration_months/12
        rate = self.interest_rate / 100
        total = self.principal_amount * ((1 + rate / 12) ** (self.duration_months))
        return round(total, 2)
    
    def remaining_balance(self):
        """Calculate remaining balance to be repaid."""
        return self.total_repayment() - self.amount_repaid

    
    def __str__(self):
        return f"Loan {self.id} for {self.borrower.user.username}"

class Payment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE,related_name='repayments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"Payment of {self.amount} for Loan {self.loan.id}"
