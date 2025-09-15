from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
            messages.success(request, 'Custom cake created successfully!')
            return redirect('custom_cake_list')
        else:
            messages.error(request, 'Error creating custom cake. Please correct the errors below.')
    else:
        form = CustomCakeForm()
    return render(request, 'custom_cake/custom_cake_form.html', {'form': form})


@login_required
def custom_cake_list(request):
    cakes = CustomCake.objects.filter(user=request.user)
    return render(request, 'custom_cake/custom_cake_list.html', {'cakes': cakes})


@login_required
def update_custom_cake(request, pk):
    cake = get_object_or_404(CustomCake, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CustomCakeForm(request.POST, request.FILES, instance=cake)
        if form.is_valid():
            form.save()
            messages.success(request, 'Custom cake updated successfully!')
            return redirect('custom_cake_list')
        else:
            messages.error(request, 'Error updating custom cake. Please correct the errors below.')
    else:
        form = CustomCakeForm(instance=cake)
    return render(request, 'custom_cake/custom_cake_edit.html', {'form': form, 'cake': cake})


@login_required
def delete_custom_cake(request, pk):
    cake = get_object_or_404(CustomCake, pk=pk, user=request.user)
    if request.method == 'POST':
        cake.delete()
        messages.success(request, 'Custom cake deleted successfully.')
        return redirect('custom_cake_list')
    return render(request, 'custom_cake/custom_cake_confirm_delete.html', {'cake': cake})