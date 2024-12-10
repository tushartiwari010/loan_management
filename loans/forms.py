from django import forms
from .models import Loan, LoanType
from django.utils import timezone

class LoanApplicationForm(forms.ModelForm):
    loan_type = forms.ModelChoiceField(
    queryset=LoanType.objects.all(),
    empty_label="Select a loan type"
    )
    interest_rate = forms.FloatField(disabled=True)
    start_date = forms.DateField(
        initial=timezone.now().date(),
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        loan_type_id = self.data.get('loan_type')
        if loan_type_id:
            try:
                loan_type = LoanType.objects.get(pk=int(loan_type_id))
                self.fields['interest_rate'].initial = loan_type.interest_rate
            except (ValueError, LoanType.DoesNotExist):
                self.fields['interest_rate'].initial = None
            
    class Meta:
        model = Loan
        fields = ['loan_type', 'principal_amount', 'interest_rate', 'duration_months', 'start_date']

    def clean(self):
        cleaned_data = super().clean()
        principal_amount = cleaned_data.get('principal_amount')
        duration = cleaned_data.get('duration_months')

        if principal_amount <= 0:
            self.add_error('principal_amount', 'Principal amount must be greater than zero.')
        if duration <= 0:
            self.add_error('duration_months', 'Duration must be greater than zero.')
        loan_type = cleaned_data.get('loan_type')
        if loan_type:
            cleaned_data['interest_rate'] = loan_type.interest_rate
        return cleaned_data


class LoanRepaymentForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label="Repayment Amount")