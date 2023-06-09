from django import forms
from django.core.exceptions import ValidationError

from .models import LogTriangle, Person


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


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ["first_name", "last_name", "email"]


class LogTriangleForm(forms.ModelForm):
    class Meta:
        model = LogTriangle
        fields = [
            "request",
            "method",
            "path",
            "query",
            "body",
        ]
