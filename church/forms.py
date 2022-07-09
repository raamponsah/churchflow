from django import forms

from church.models import ChurchSettings, Church


class ChurchSetupForm(forms.ModelForm):
    class Meta:
        model = Church
        fields = "__all__"

        widgets = {
            'user': forms.HiddenInput(),
            'church_name': forms.TextInput(attrs={'class': 'form-control'}),
            'short_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),

        }