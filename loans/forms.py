from django import forms
from .models import Loan, LoanType

class LoanApplicationForm(forms.ModelForm):
    loan_type = forms.ModelChoiceField(
    queryset=LoanType.objects.all(),
    empty_label="Select a loan type"
    )
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
