from django import forms
from django.forms import ModelForm, fields
from .models import Stock, StockHistory
from functools import partial
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        
    # def save(self, commit=True):
    #     user = super(NewUserForm, self).save(commit=False)
    #     user.email = self.cleaned_data['email']
    #     if commit:
    #         user.save()
        
    #     return user


class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity', 'issue_by']

    #def clean_category(self):
        #category = self.cleaned_data.get('category')
        #if not category:
            #raise forms.ValidationError('This field is required')
        
        #for instance in Stock.objects.all():
            #if instance.category == category:
                #raise forms.ValidationError(category + ' is already created')

        #return category

    #def clean_item_name(self):
        #item_name = self.cleaned_data.get('item_data')
        #if not item_name:
            #raise forms.ValidationError('This field is required')
        #return item_name
    
    def clean_issue_by(self):
        issue_by = self.cleaned_data.get('issue_by')
        if not issue_by:
            raise forms.ValidationError('This field is required')
        return issue_by
 
class DateInput(forms.DateInput):
    input_type = 'date'

class StockHistorySearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required=False)
    start_date = forms.DateTimeField(required=False, widget = DateInput())
    end_date = forms.DateTimeField(required=False, widget = DateInput)
    class Meta:
        model = StockHistory
        fields = ['category', 'item_name', 'start_date', 'end_date']
       

class StockSearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required = False)
    class Meta:
        model = Stock
        fields = ['category', 'item_name']


class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity', 'issue_by']

class IssueForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['issue_quantity', 'issue_to']


class ReceiveForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['receive_quantity', 'receive_by']

class ReorderLevelForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['reorder_level']