from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import CustomCakeForm
from .models import CustomCake
from .utils import get_or_create_deposit_product


def _can_access(user, cake: CustomCake) -> bool:
    """Staff can access everything; users can access their own items."""
    return user.is_staff or (cake.user_id == getattr(user, "id", None))


@login_required
def custom_cake_list(request):
    """
    List the current user's custom cakes (staff see all).
    """
    if request.user.is_staff:
        cakes = CustomCake.objects.all().order_by("-created_on", "-id")
    else:
        cakes = CustomCake.objects.filter(user=request.user).order_by(
            "-created_on", "-id"
        )
    return render(
        request, "custom_cake/custom_cake_list.html", {"cakes": cakes}
    )


@login_required
def custom_cake_create(request):
    """
    Create a new custom cake tied to the logged-in user.
    Tests expect an error message 'Error creating custom cake' on invalid POST.
    """
    if request.method == "POST":
        form = CustomCakeForm(request.POST, request.FILES)
        if form.is_valid():
            cake = form.save(commit=False)
            cake.user = request.user
            cake.save()
            messages.success(request, "Custom cake created successfully.")
            return redirect("custom_cake_detail", pk=cake.pk)
        else:
            # matches test expectation

            messages.error(request, "Error creating custom cake")
    else:
        form = CustomCakeForm()
    return render(
        request,
        "custom_cake/custom_cake_form.html",
        {"form": form, "mode": "create"},
    )


@login_required
def custom_cake_detail(request, pk: int):
    cake = get_object_or_404(CustomCake, pk=pk)
    if not _can_access(request.user, cake):
        raise PermissionDenied
    deposit_product = get_or_create_deposit_product()
    return render(
        request,
        "custom_cake/custom_cake_detail.html",
        {"cake": cake, "deposit_product": deposit_product},
    )


@login_required
def custom_cake_edit(request, pk: int):
    """
    Update an existing custom cake.
    Tests verify that a valid POST changes the name.
    """
    cake = get_object_or_404(CustomCake, pk=pk)
    if not _can_access(request.user, cake):
        raise PermissionDenied
    if request.method == "POST":
        form = CustomCakeForm(request.POST, request.FILES, instance=cake)
        if form.is_valid():
            cake = form.save()
            messages.success(request, "Custom cake updated successfully.")
            return redirect("custom_cake_detail", pk=cake.pk)
        else:
            messages.error(request, "Error updating custom cake")
    else:
        form = CustomCakeForm(instance=cake)
    return render(
        request,
        "custom_cake/custom_cake_edit.html",
        {"form": form, "mode": "edit", "cake": cake},
    )


@login_required
def custom_cake_delete(request, pk: int):
    cake = get_object_or_404(CustomCake, pk=pk)
    if not _can_access(request.user, cake):
        raise PermissionDenied
    if request.method == "POST":
        cake.delete()
        # match test expectation text:

        messages.success(request, "Custom cake deleted successfully.")
        return redirect("custom_cake_list")
    return render(
        request, "custom_cake/custom_cake_confirm_delete.html", {"cake": cake}
    )

def design_your_own(request):
    """
    Gatekeeper for the 'Design Your Own' nav link.
    If user is not authenticated, show message and redirect to login with ?next=
    so they return to the custom cake form after logging in.
    """
    create_url = reverse("custom_cake_create")

    if request.user.is_authenticated:
        return redirect(create_url)

    messages.info(request, "Please sign in to design a custom cake.")
    login_url = reverse("account_login")
    return redirect(f"{login_url}?next={create_url}")
