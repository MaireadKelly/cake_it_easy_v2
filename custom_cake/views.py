from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomCakeForm
from .models import CustomCake

@login_required
def create_custom_cake(request):
    if request.method == 'POST':
        form = CustomCakeForm(request.POST, request.FILES)
        if form.is_valid():
            custom_cake = form.save(commit=False)
            custom_cake.user = request.user
            custom_cake.save()
            return redirect('custom_cake_list')
    else:
        form = CustomCakeForm()
    return render(request, 'custom_cake/custom_cake_form.html', {'form': form})


@login_required
def custom_cake_list(request):
    cakes = CustomCake.objects.filter(user=request.user)
    return render(request, 'custom_cake/custom_cake_list.html', {'cakes': cakes})
