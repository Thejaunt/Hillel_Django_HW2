from django import forms
from django.core.exceptions import ValidationError


class TriangleForm(forms.Form):
    cath1 = forms.DecimalField(
        max_value=10000, required=True, widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    cath2 = forms.DecimalField(
        max_value=10000, required=True, widget=forms.NumberInput(attrs={"class": "form-control"})
    )

    def clean_cath1(self):
        cath1 = self.cleaned_data.get("cath1")
        if cath1 <= 0:
            raise ValidationError("Catheters must be greater than 0")
        return cath1

    def clean_cath2(self):
        cath2 = self.cleaned_data.get("cath2")
        if cath2 <= 0:
            raise ValidationError("Catheters must be greater than 0")
        return cath2
