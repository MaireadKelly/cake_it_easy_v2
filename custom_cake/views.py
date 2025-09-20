from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from .models import CustomCake
from .forms import CustomCakeForm  # uses your existing ModelForm

def _can_access(user, cake: CustomCake) -> bool:
    return user.is_staff or (cake.user_id == getattr(user, "id", None))

@login_required
def custom_cake_list(request):
    """
    List the current user's custom cakes.
    Staff sees all for convenience.
    """
    if request.user.is_staff:
        cakes = CustomCake.objects.all().order_by('-id')
    else:
        cakes = CustomCake.objects.filter(user=request.user).order_by('-id')
    return render(request, 'custom_cake/custom_cake_list.html', {'cakes': cakes})

@login_required
def custom_cake_create(request):
    """Create a new custom cake tied to the logged-in user."""
    if request.method == 'POST':
        form = CustomCakeForm(request.POST, request.FILES)
        if form.is_valid():
            cake = form.save(commit=False)
            cake.user = request.user
            cake.save()
            messages.success(request, 'Custom cake created.')
            return redirect('custom_cake_detail', pk=cake.pk)
    else:
        form = CustomCakeForm()
    return render(request, 'custom_cake/custom_cake_form.html', {'form': form, 'mode': 'create'})

@login_required
def custom_cake_detail(request, pk: int):
    cake = get_object_or_404(CustomCake, pk=pk)
    if not _can_access(request.user, cake):
        raise PermissionDenied
    return render(request, 'custom_cake/custom_cake_detail.html', {'cake': cake})

@login_required
def custom_cake_edit(request, pk: int):
    cake = get_object_or_404(CustomCake, pk=pk)
    if not _can_access(request.user, cake):
        raise PermissionDenied
    if request.method == 'POST':
        form = CustomCakeForm(request.POST, request.FILES, instance=cake)
        if form.is_valid():
            form.save()
            messages.success(request, 'Custom cake updated.')
            return redirect('custom_cake_detail', pk=cake.pk)
    else:
        form = CustomCakeForm(instance=cake)
    return render(request, 'custom_cake/custom_cake_form.html', {'form': form, 'mode': 'edit', 'cake': cake})

@login_required
def custom_cake_delete(request, pk: int):
    cake = get_object_or_404(CustomCake, pk=pk)
    if not _can_access(request.user, cake):
        raise PermissionDenied
    if request.method == 'POST':
        cake.delete()
        messages.info(request, 'Custom cake deleted.')
        return redirect('custom_cake_list')
    return render(request, 'custom_cake/custtom_cake_confirm_delete.html', {'cake': cake})
