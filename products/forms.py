from django import forms
from .models import Product

class ProductForm(forms.Form):
    name = forms.CharField()

class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
        ]
    def clean_name(self):
        data = self.cleaned_data.get('name')
        if len(data) < 4:
            raise forms.ValidationError("This is not long enough!")
        return data
        
class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'price', 'inventory', )