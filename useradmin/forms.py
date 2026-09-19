from core.models import Product, Vendor
from django import forms
# from bootstrap_datepicker_plus import DatePickerInput



class AddProductForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Product Title", "class":"form-control"}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Product Description", "class":"form-control"}))
    price = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': "Sale Price", "class":"form-control", "step": "any"}))
    old_price = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': "Old Price", "class":"form-control", "step": "any"}))
    type = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Type of product e.g organic cream", "class":"form-control"}))
    stock_count = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': "How many are in stock?", "class":"form-control"}))
    life = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': "How long would this product live?", "class":"form-control"}))
    mfd = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'placeholder': "e.g: 22-11-02", "class":"form-control"}))
    tags = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': "Tags", "class":"form-control"}))
    image = forms.ImageField(widget=forms.FileInput(attrs={"class":"form-control"}))

    class Meta:
        model = Product
        fields = [
            'title',
            'image',
            'description',
            'price',
            'old_price',
            'specifications',
            'type',
            'stock_count',
            'life',
            'mfd',
            'tags',
            'digital',

            'category',
        ]

        widgets = {
        # 'mdf': DateTimePickerInput
    }

class VendorForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Store Name", "class": "form-control"}))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={"placeholder": "Store Description", "class": "form-control"}))
    address = forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder": "Address", "class": "form-control"}))
    contact = forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder": "Contact Phone", "class": "form-control"}))
    chat_resp_time = forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder": "Chat Response Time", "class": "form-control"}))
    shipping_on_time = forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder": "Shipping On Time %", "class": "form-control"}))
    authentic_rating = forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder": "Authentic Rating %", "class": "form-control"}))
    days_return = forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder": "Days Return Policy", "class": "form-control"}))
    warranty_period = forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder": "Warranty Period", "class": "form-control"}))
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={"class":"form-control"}))
    cover_image = forms.ImageField(required=False, widget=forms.FileInput(attrs={"class":"form-control"}))

    class Meta:
        model = Vendor
        fields = [
            "title", "image", "cover_image", "description", 
            "address", "contact", "chat_resp_time", "shipping_on_time", 
            "authentic_rating", "days_return", "warranty_period"
        ]