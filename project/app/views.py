from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Medicine, User
from .forms import UserForm



# app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserLoginForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'app/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'app/login.html', {'form': form})



@login_required
def home(request):
    medicines = Medicine.objects.all()
    return render(request, 'app/home.html', {'medicines': medicines})

def medicine_detail(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.medicine = medicine
            user.total_price = medicine.price * user.quantity
            user.save()
            return render(request, 'app/bill.html', {'user': user})
    else:
        form = UserForm()
    return render(request, 'app/medicine_detail.html', {'medicine': medicine, 'form': form})

def search(request):
    query = request.GET.get('q')
    medicines = Medicine.objects.filter(name__icontains=query)
    if medicines:
        return render(request, 'app/search_results.html', {'medicines': medicines})
    else:
        return HttpResponse('Medicine not found')

