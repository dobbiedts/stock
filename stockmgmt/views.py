from django.db.models import query
from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
from django.core.paginator import Paginator

import csv
from .forms import StockCreateForm, StockSearchForm, StockUpdateForm, IssueForm, ReceiveForm, ReorderLevelForm, StockHistorySearchForm, NewUserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.mail import EmailMessage
from django.conf import settings
from io import StringIO, BytesIO
from stockmanagement.settings import EMAIL_HOST_USER as DobbieDts
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm






# Create your views here.

def register_request(request):

    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, 'Registration successful.' )
            return redirect('/list_items')
        messages.error(request, 'Unsuccessful registration. Invalid information.')
        
    else:
        form = NewUserForm()
    context= {
             "register_form" : form,
        }
    return render (request, 'register.html', context)

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"You are now logged in as {username}.")
                return redirect('/list_items')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    form = AuthenticationForm()
    context={
        "login_form":form
        }
    return render(request, 'login.html', context)

def logout_request(request):
    logout(request)
    if logout:
        messages.success(request, 'You have successfully logged out.') 
    return redirect('/login')

def home(request):
    header = 'Welcome : This is the home page'
    form = ' '
    context = {
        "header" : header,
        "form"  : form,
    }
    return redirect('/list_items')

@login_required(login_url='/login')
def list_items(request):
    header = 'List of Items'
    queryset = Stock.objects.all()
    form = StockSearchForm(request.POST or None)
    
    context = {
        "header" : header,
        "queryset" : queryset,
        "form" : form,
    }
    if request.method == 'POST':
        queryset = Stock.objects.filter(category__icontains = form['category'].value(),
                                        item_name__icontains = form['item_name'].value(),
        )

        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type = 'text/csv')
            response['Content-Disposition'] = 'attachment; filename= "List of stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY'])
            instance = queryset
            for stock in instance:
                writer.writerow([stock.category, stock.item_name, stock.quantity])
            return response
        
        context = {
            "form" : form,
            "queryset": queryset,
            "header" : header,        }

    return render(request, "list_items.html", context)

@login_required(login_url='/login')
def add_items(request):
    form =  StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Saved')
        return redirect('/list_items')
    context = {
        "title" : "Add Item",  
        "form" : form,
    }
    return render(request, 'add_items.html', context)

def update_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = StockUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=queryset) 
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated')
            return redirect('/list_items')
    
    context = {
		'form':form
	}
    return render(request, 'add_items.html', context)


def delete_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Successfully deleted')
        return redirect('/list_items')
    return render(request, 'delete_items.html')

def stock_detail(request, pk):
    queryset = Stock.objects.get(id=pk)
    context = {
        "queryset" : queryset,
    }
    return render(request, 'stock_detail.html', context)

def issue_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance = queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.receive_quantity = 0
        instance.quantity -= instance.issue_quantity
        instance.issue_by = str(request.user)
        instance.save()
        messages.success(request, "Issued SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.item_name) + "s now left in Store")
        return redirect('/stock_detail/'+str(instance.id))
		# return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": 'Issue ' + str(queryset.item_name),
        "queryset": queryset,
        "form": form,
        "username": 'Issue By: ' + str(request.user),
    }
    return render(request, "add_items.html", context)

def receive_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.issue_quantity = 0
        instance.quantity += instance.receive_quantity
        instance.receive_by = str(request.user)
        instance.save()
        messages.success(request, "Received Successfully. " + str(instance.quantity) + " of " + str(instance.item_name) + " now in store" )
        return redirect('/stock_detail/'+str(instance.id))
        # return HttpResponseRedirect(instance.get_absolute_url())
    
    context = {
        "title" : 'Receive ' + str(queryset.item_name),
        "queryset"  : queryset,
        "form" : form,
        "username" : 'Received by ' + str(request.user),
    }
    return render(request, "add_items.html", context)

def reorder_level(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReorderLevelForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request,"Reorder level of "+ str(instance.item_name)+ " has been changed to "+ str(instance.reorder_level))
        return redirect('/list_items/')
    context = {
        "title" : 'Reorder level of  ' + str(queryset.item_name),
        "instance"  : queryset,
        "form" : form,
        #"username" : 'Received by ' + str(request.user),
    }
    return render(request, "add_items.html", context)

@login_required(login_url='/login')
def list_history(request):
    header = 'HISTORY OF DATA'
    qset = StockHistory.objects.all()
    form = StockHistorySearchForm(request.POST or None)

    if request.method == 'POST':
        email_to = request.POST.get('email_to', False)
        search = request.POST.get('search', False)

        if email_to:
            stock_report = StringIO()
            writer = csv.writer(stock_report)
            # insert header to csv
            writer.writerow(['CATEGORY', 
                        'ITEM NAME',
                        'QUANTITY', 
                        'ISSUE QUANTITY', 
                        'RECEIVE QUANTITY', 
                        'RECEIVE BY', 
                        'ISSUE BY', 
                        'LAST UPDATED',])
            instance = qset
            for stock in instance:
                    writer.writerow(
                        [stock.category, 
                        stock.item_name, 
                        stock.quantity, 
                        stock.issue_quantity, 
                        stock.receive_quantity, 
                        stock.receive_by, 
                        stock.issue_by, 
                        stock.last_updated])

            subject = 'Stock Report'
            message = 'Stock Report from DobbieDts Systems Information'
            to = request.POST['email_to']     
            recipient_list = [to]

            mail = EmailMessage(subject, message, DobbieDts, to=recipient_list)
            mail.attach('stock_report.csv', stock_report.getvalue(), 'text/csv')
            if mail.send(fail_silently=False) :
                messages.success(request, 'Mail sent successfully')

        elif search:
            category = form['category'].value()
            item = form['item_name'].value()
            start_date = form['start_date'].value()
            end_date = form['end_date'].value()
            today = timezone.now()

            if start_date and end_date :
                qset = StockHistory.objects.filter(
                    item_name__icontains=item,
                    last_updated__range = [start_date, end_date]     
                )
                
            elif start_date:
                qset = StockHistory.objects.filter(
                    item_name__icontains=item,
                    last_updated__range=[start_date, today]  
                )
            else:
                qset = StockHistory.objects.filter(item_name__icontains=item,)
            

            
            #form = StockSearchForm(request.POST or None)
            if form['export_to_CSV'].value() == True:
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="Stock History.csv"'
                writer = csv.writer(response)
                writer.writerow(
                            ['CATEGORY', 
                            'ITEM NAME',
                            'QUANTITY', 
                            'ISSUE QUANTITY', 
                            'RECEIVE QUANTITY', 
                            'RECEIVE BY', 
                            'ISSUE BY', 
                            'LAST UPDATED',])
                instance = qset
                for stock in instance:
                        writer.writerow(
                            [stock.category, 
                            stock.item_name, 
                            stock.quantity, 
                            stock.issue_quantity, 
                            stock.receive_quantity, 
                            stock.receive_by, 
                            stock.issue_by, 
                            stock.last_updated])
                return response
    
    query = qset.order_by('-item_name')
    paginate = Paginator(query, 4)
    page = request.GET.get('page', 1)
    page_obj = paginate.page(page)
    context = {
		"form": form,
		"header": header,
        "page_obj" : page_obj,
        "qset" : qset,
        
	}
    return render(request, "list_history.html", context)





        


