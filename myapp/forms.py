from django import forms
from myapp.models import Order, Product

CHOICES = [(1, 'Yes'), (0, 'No')]
# Part-1 included order, Interest Form
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client', 'product','num_unit']
        widgets = {'client': forms.RadioSelect(), }
        labels = {'num_unit': u'Quantity', 'client': u'ClientName'}
#Client = forms.ChoiceField(label='Client Name', widget=forms.RadioSelect)
#form = OrderForm()
#form.fields['num_unit'].label = 'Quantity'


class InterestForm(forms.Form):
    interested = forms.ChoiceField(label='interested', widget=forms.RadioSelect, choices=CHOICES)
    quantity = forms.IntegerField(label='quantity', initial=1)
    comments = forms.CharField(widget=forms.Textarea, label='Additional Comments', required=False)