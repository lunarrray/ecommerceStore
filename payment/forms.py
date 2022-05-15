from django import forms

from orders.models import Order


class OrderForm(forms.ModelForm):

    full_name = forms.CharField(
        label='Customer name', min_length=4, max_length=50, help_text='Required')
    phone = forms.CharField(
        label='Phone number', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={
        'required': 'Sorry, you will need an email'})
    address = forms.CharField(
        label='Address', min_length=4, max_length=50, help_text='Required')

    class Meta:
        model = Order
        fields = ('full_name', 'phone', 'email', 'address')

    def clean_username(self):
        full_name = self.cleaned_data['full_name'].lower()
        return full_name

    def clean_email(self):
        email = self.cleaned_data['email']
        return email

    def clean_address(self):
        address = self.cleaned_data['address']
        return address

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        return phone

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': ''})
        self.fields['phone'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': '0770707070'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['address'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Chyngyz Aitmatov 56'})



