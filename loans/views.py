from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import LoanApplicationForm
from .models import Loan, Borrower, LoanType, Payment

def home(request):
    return render(request, 'base.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to the home page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def apply_loan(request):
    if request.method == 'POST':
        form = LoanApplicationForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            borrower = Borrower.objects.get(user=request.user)  # Assuming Borrower is linked to User
            loan.borrower = borrower
            loan.interest_rate = loan.loan_type.interest_rate
            loan.status = 'Pending'
            loan.save()
            messages.success(request, 'Loan application submitted successfully!')
            return redirect('loan_list')  # Redirect to loan list after applying
    else:
        form = LoanApplicationForm()

    loan_types = LoanType.objects.all()
    return render(request, 'loans/apply_loan.html', {'form': form, 'loan_types': loan_types})

@login_required
def loan_list(request):
    try:
        borrower = Borrower.objects.get(user=request.user)
    except Borrower.DoesNotExist:
        # If no Borrower exists for the user, redirect to registration or an error page
        return redirect('register')
    loans = Loan.objects.filter(borrower=borrower)  # Loans specific to the logged-in user
    return render(request, 'loans/loan_list.html', {'loans': loans})
@login_required
def loan_detail(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)
    return render(request, 'loans/loan_detail.html', {'loan': loan})
