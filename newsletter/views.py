# newsletter/views.py
from django.contrib import messages
from django.shortcuts import redirect
from .forms import NewsletterSignupForm

def subscribe(request):
    if request.method != "POST":
        return redirect("home")
    form = NewsletterSignupForm(request.POST)
    if form.is_valid():
        sub = form.save(commit=False)
        sub.source = "modal"
        sub.save()
        messages.success(request, "Thanks! You’re subscribed.")
        return redirect("/?nl=1&code=WELCOME10")
    messages.error(request, "Please enter a valid email.")
    return redirect("home")
