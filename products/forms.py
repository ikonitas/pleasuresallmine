from django import forms

from products.models import Product

class ProductForm(forms.ModelForm):
    total_price = forms.CharField(max_length=100,
            widget=forms.TextInput(attrs={'readonly': 'readonly',
                                          'class': 'total_price',}))

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['total_price'].required = False
        if self.instance.price:
            self.fields['total_price'].initial = self.instance.total_price()


    class Meta:
        model = Product
