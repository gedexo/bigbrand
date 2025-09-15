from django import forms
from .models import Contact, CareerEnquiry, ServiceEnquiry


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'subject', 'message']

    
class CareerEnquiryForm(forms.ModelForm):
    class Meta:
        model = CareerEnquiry
        fields = ['career', 'name', 'email', 'phone', 'resume', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'resume': forms.ClearableFileInput(attrs={
                'class': 'form-control',  
                'accept': '.pdf,.doc,.docx'
            }),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if not resume:
            raise forms.ValidationError("This field is required.")
        if resume.size > 5*1024*1024:
            raise forms.ValidationError("File size must be under 5MB.")
        return resume


class ServiceEnquiryForm(forms.ModelForm):
    class Meta:
        model = ServiceEnquiry
        fields = ['service', 'name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }