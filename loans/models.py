from django.db import models
from django.contrib.auth.models import User

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
    interest_rate = models.FloatField()
    duration_months = models.IntegerField()
    start_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')])

    def total_repayment(self):
        return self.principal_amount * (1 + (self.interest_rate / 100))
    
    def __str__(self):
        return f"Loan {self.id} for {self.borrower.user.username}"

class Payment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()

    def __str__(self):
        return f"Payment of {self.amount} for Loan {self.loan.id}"
