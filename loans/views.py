from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import LoanApplicationForm, LoanRepaymentForm
from .models import Loan, Borrower, LoanType, Payment
from django.utils import timezone
from .serializers import PaymentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

def home(request):
    return render(request, 'base.html')


def get_interest_rate(request, loan_type_id):
    try:
        loan_type = LoanType.objects.get(pk=loan_type_id)
        print(f"Requested loan_type_id: {loan_type_id}")
        return JsonResponse({'interest_rate': loan_type.interest_rate})
    
    except LoanType.DoesNotExist:
        return JsonResponse({'error': 'Loan type not found'}, status=404)

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
            try:
                borrower = Borrower.objects.get(user=request.user)
            except Borrower.DoesNotExist:
                # Create a new Borrower instance
                borrower = Borrower.objects.create(user=request.user)
            loan.borrower = borrower
            loan.interest_rate = loan.loan_type.interest_rate
            loan.status = 'Pending'
            loan.save()
            messages.success(request, 'Loan application submitted successfully!')
            return redirect('loan_list')  # Redirect to loan list after applying
        else:
            print("Form errors:", form.errors)
    else:
        form = LoanApplicationForm(initial={'start_date': timezone.now().date()})

    loan_types = LoanType.objects.all()
    return render(request, 'loans/apply_loan.html', {'form': form, 'loan_types': loan_types})

@login_required
def loan_list(request):
    try:
        borrower = Borrower.objects.get(user=request.user)
        loans = Loan.objects.filter(borrower=borrower)
        return render(request, 'loans/loan_list.html', {'loans': loans})
    except Borrower.DoesNotExist:
        messages.warning(request, 'You need to apply for a loan first.')
        return redirect('apply_loan')
    
@login_required
def loan_detail(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)
    return render(request, 'loans/loan_detail.html', {'loan': loan})


@api_view(['GET', 'POST'])
def make_repayment(request, loan_id):
    try:
        loan = get_object_or_404(Loan, id=loan_id)
        
        if request.method == 'POST':
            # For POST requests, get the amount from request.data instead of form
            amount = request.data.get('amount')
            if not amount:
                return Response(
                    {'error': 'Amount is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                amount = float(amount)
            except (TypeError, ValueError):
                return Response(
                    {'error': 'Invalid amount format'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if amount <= loan.remaining_balance():
                # Create payment
                payment = Payment.objects.create(
                    loan=loan,
                    amount=amount
                )
                
                # Update loan
                loan.amount_repaid += amount
                if loan.remaining_balance() <= 0:
                    loan.status = 'Closed'
                loan.save()

               # Serialize and return payment details
                serializer = PaymentSerializer(payment)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {'error': 'Repayment amount exceeds remaining balance'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # GET request
        loan_data = {
            'loan_id': loan.id,
            'remaining_balance': loan.remaining_balance(),
            'status': loan.status,
            'total_amount': loan.amount
        }
        return Response(loan_data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )