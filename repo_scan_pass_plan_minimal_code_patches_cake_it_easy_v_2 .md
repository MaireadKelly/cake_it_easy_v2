# 🚀 Quick Start — Bag + Checkout + Webhooks (copy/paste order)
**Use this list as your checklist.** Full code for each file is in the section **“✅ Copy‑paste Code Pack — Bag, Checkout, Stripe (incl. Webhooks)”** **below** (already included in this canvas).

### Files — apply in this order (REPLACE/CREATE as indicated)
1) **bag**
   - `bag/context_processors.py` — REPLACE
   - `bag/views.py` — REPLACE
   - `bag/urls.py` — REPLACE/CREATE
   - `bag/templates/bag/bag.html` — REPLACE/CREATE
2) **checkout**
   - `checkout/models.py` — REPLACE
   - `checkout/forms.py` — REPLACE/CREATE
   - `checkout/views.py` — REPLACE
   - `checkout/templates/checkout/checkout.html` — REPLACE
   - `checkout/templates/checkout/checkout_success.html` — REPLACE/CREATE
   - `checkout/webhooks.py` — CREATE
   - `checkout/urls.py` — REPLACE
3) **project urls**
   - `cake_it_easy_v2/urls.py` — ensure it includes:
     ```py
     path('bag/', include('bag.urls')),
     path('checkout/', include('checkout.urls')),
     ```
4) **Env Vars (local .env & Heroku Config Vars)**
   ```
   STRIPE_PUBLIC_KEY=pk_test_...
   STRIPE_SECRET_KEY=sk_test_...
   STRIPE_CURRENCY=eur
   STRIPE_WEBHOOK_SECRET=whsec_...
   ```

### Commands
- **Local:**
  ```bash
  python manage.py makemigrations checkout
  python manage.py migrate
  python manage.py runserver
  ```
- **Heroku (Dashboard → More → Run console):**
  ```
  python manage.py migrate
  python manage.py collectstatic --noinput
  ```

### Stripe Webhook (test mode)
1. Stripe → Developers → Webhooks → **Add endpoint**: `https://<your-app>.herokuapp.com/checkout/wh/`
2. Events: `payment_intent.succeeded` (optionally `payment_intent.payment_failed`)
3. Copy **signing secret** → set `STRIPE_WEBHOOK_SECRET` in Heroku Config Vars

---
# Repo scan summary (uploaded zips)

**Files received & opened:**

- `cake_it_easy_clean.zip` → extracted as `/repo_new_fix`
- `cake_it_easy_old_clean.zip` → extracted as `/repo_old_fix`

**Quick findings (v2.0 **``**):**

- ✅ Apps present: `home/`, `products/`, `custom_cake/`, `bag/`, `checkout/`
- ✅ Project package: `cake_it_easy_v2/` with `settings.py`, `urls.py`
- ✅ Templates & static exist
- ⚠️ Several files look **truncated** (contain literal `...`) and/or cut mid‑line:
  - `checkout/models.py` (address fields cut; trailing `...`)
  - `checkout/views.py` (right after `STRIPE_ENABLED = ...` and near create PaymentIntent / save order)
  - `bag/views.py` (inside `add_to_bag`)
  - Some templates like `templates/base.html` cut mid‑tag
- ✅ `settings.py` includes Stripe envs (`STRIPE_PUBLIC_KEY`, `STRIPE_SECRET_KEY`, `STRIPE_ENABLED`)
- ✅ `urls.py` wires `home`, `products`, `custom_cake`, `bag`, `checkout`

**Quick findings (old **``**):**

- ✅ `bag/` app present with variant-aware add flow
- ❌ No `checkout/` app here
- ✅ Templates set includes `bag/bag.html`, `products/*`, etc.
- ⚠️ Some old files also appear truncated

**Conclusion:** I can see your intended structure and most pieces, but a few **critical files are truncated**. I’ve prepared minimal, rubric-aligned replacements below so you can drop them in 1:1 and get back to a runnable baseline.

---

# Minimal code patches (copy‑paste)

> **Goal:** restore a clean, PASS‑oriented MVP (PaymentIntent + Order saving + basic Bag). These patches keep your naming and URLs.

## 1) `checkout/models.py`

```python
from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Order(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    full_name = models.CharField(max_length=80)
    email = models.EmailField()
    phone_number = models.CharField(max_length=32, blank=True)
    country = models.CharField(max_length=40, blank=True)
    postcode = models.CharField(max_length=20, blank=True)
    town_or_city = models.CharField(max_length=40, blank=True)
    street_address1 = models.CharField(max_length=80, blank=True)
    street_address2 = models.CharField(max_length=80, blank=True)

    order_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stripe_pid = models.CharField(max_length=254, blank=True)
    original_bag = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"

class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    lineitem_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order {self.order_id})"
```

> **After paste:** run `makemigrations checkout && migrate`.

## 2) `checkout/forms.py`

```python
from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'full_name','email','phone_number','country','postcode',
            'town_or_city','street_address1','street_address2'
        )
```

## 3) `checkout/views.py`

```python
import json
from decimal import Decimal

import stripe
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render

from products.models import Product
from .forms import OrderForm
from .models import Order, OrderLineItem

STRIPE_ENABLED = bool(getattr(settings, "STRIPE_PUBLIC_KEY", "") and getattr(settings, "STRIPE_SECRET_KEY", ""))
if STRIPE_ENABLED:
    stripe.api_key = settings.STRIPE_SECRET_KEY

def _calc_bag_items_and_total(request):
    bag = request.session.get('bag', {})
    items, total = [], Decimal('0.00')
    for pid, qty in bag.items():
        product = get_object_or_404(Product, pk=int(pid))
        line_total = product.price * qty
        items.append({'product': product, 'quantity': qty, 'line_total': line_total})
        total += line_total
    return items, total

def checkout(request):
    items, total = _calc_bag_items_and_total(request)
    if not items:
        messages.info(request, "Your bag is empty.")
        return redirect('product_list')

    client_secret = ''
    if STRIPE_ENABLED:
        intent = stripe.PaymentIntent.create(
            amount=int(total * 100),  # cents
            currency=getattr(settings, 'STRIPE_CURRENCY', 'eur'),
            metadata={'integration_check': 'accept_a_payment'},
        )
        client_secret = intent.client_secret
    else:
        messages.warning(request, "Stripe is not configured. Running in no-payment demo mode.")

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            pid = request.POST.get('client_secret', '').split('_secret')[0] if STRIPE_ENABLED else ''
            order = form.save(commit=False)
            order.user = request.user if request.user.is_authenticated else None
            order.order_total = total
            order.stripe_pid = pid
            order.original_bag = json.dumps(request.session.get('bag', {}))
            order.save()
            for i in items:
                OrderLineItem.objects.create(order=order, product=i['product'], quantity=i['quantity'])
            request.session['bag'] = {}
            try:
                send_mail(
                    subject=f"Cake It Easy — Order #{order.id} confirmed",
                    message=f"Thanks for your order! Total: €{order.order_total}",
                    from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
                    recipient_list=[order.email],
                    fail_silently=True,
                )
            except Exception:
                pass
            return redirect('checkout_success', order_id=order.id)
    else:
        form = OrderForm()

    return render(request, 'checkout/checkout.html', {
        'form': form,
        'items': items,
        'total': total,
        'stripe_public_key': getattr(settings, "STRIPE_PUBLIC_KEY", ""),
        'client_secret': client_secret,
    })

def checkout_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'checkout/checkout_success.html', {'order': order})
```

## 4) `checkout/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('success/<int:order_id>/', views.checkout_success, name='checkout_success'),
]
```

## 5) `templates/checkout/checkout.html`

```html
{% extends 'base.html' %}
{% block content %}
<h1>Checkout</h1>
<ul>
  {% for i in items %}
    <li>{{ i.product.name }} × {{ i.quantity }} — €{{ i.line_total }}</li>
  {% endfor %}
</ul>
<p><strong>Total: €{{ total }}</strong></p>
<form id="checkout-form" method="POST">
  {% csrf_token %}
  {{ form.as_p }}
  <input type="hidden" name="client_secret" id="client_secret" value="{{ client_secret }}">
  <button type="submit" id="pay-btn">Pay</button>
</form>
{% if stripe_public_key %}
<script src="https://js.stripe.com/v3/"></script>
<script>
  const stripe = Stripe("{{ stripe_public_key }}");
  const form = document.getElementById('checkout-form');
  form.addEventListener('submit', async (e) => {
    // Minimal demo — rely on server-side PaymentIntent confirmation after redirect
  });
</script>
{% endif %}
{% endblock %}
```

## 6) `templates/checkout/checkout_success.html`

```html
{% extends 'base.html' %}
{% block content %}
  <h1>Thanks!</h1>
  <p>Your order number is <strong>#{{ order.id }}</strong>.</p>
{% endblock %}
```

## 7) `bag/views.py` (minimal, server-side add)

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product

def view_bag(request):
    return render(request, 'bag/bag.html')

def add_to_bag(request, product_id):
    if request.method != 'POST':
        return redirect('product_detail', product_id=product_id)
    product = get_object_or_404(Product, pk=product_id)
    try:
        qty = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        qty = 1
    qty = max(1, qty)

    bag = request.session.get('bag', {})
    pid = str(product_id)
    bag[pid] = bag.get(pid, 0) + qty
    request.session['bag'] = bag

    messages.success(request, f"Added {qty} × {product.name} to your bag.")
    return redirect('checkout')
```

## 8) `bag/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_bag, name='view_bag'),
    path('add/<int:product_id>/', views.add_to_bag, name='add_to_bag'),
]
```

## 9) `templates/bag/bag.html` (very simple)

```html
{% extends 'base.html' %}
{% block content %}
<h1>Your Bag</h1>
<p>For the PASS demo flow we add items and proceed straight to checkout.</p>
{% endblock %}
```

---

# PASS‑focused plan (short)

**Blockers discovered:** truncated checkout and bag files; base template partially cut; Stripe keys optional but flow should not crash if missing.

**Plan (fastest credible route to PASS):**

1. **Restore files** above (paste patches). Ensure base template is complete enough to render; if needed, use a barebones `base.html` with `{% block content %}{% endblock %}` while keeping your includes.
2. `python manage.py makemigrations checkout && migrate`.
3. Seed 2–3 products (fixture or admin) to demo bag/checkout.
4. **Stripe**: add test keys to `.env` locally; on deploy, set in env vars. If absent, app still completes order without charging (with a visible message) — this satisfies 1.1/1.2 for demo but add a real test run with keys before submission.
5. **RBAC fix**: hide product CRUD buttons for non‑staff; gate views with `@staff_member_required` and template `{% if request.user.is_staff %}`.
6. **Broken links**: verify logo/home/footer URLs; use `{% url %}` reverse names only.
7. **SEO minimums**: add `<meta name="description">`, `robots.txt`, `sitemap.xml` routing, custom `404.html` with DEBUG=False on deploy.
8. **Docs & Proof**: screenshots of Stripe dashboard (test payment), success page, email console output, ERD (dbdiagram.io), and a link checklist. Minimal manual tests list.

---

# What I still need (when you’re back)

- Re‑upload any **files you want me to keep exactly** if they differ from these patches.
- Confirm deploy target (Heroku?) so I can list the exact env vars + `collectstatic` steps.

I’ve kept all code ready to drop into your current structure with your naming. When you return, we’ll slot these in, run, and tick off the PASS checklist items quickly.



---

## 🔧 Patch Application Instructions (clear, file-by-file)

> Unless stated otherwise, **REPLACE the entire file** with the snippet provided. Create files/dirs that don’t exist. Keep the same paths and names.

### 0) Safety net first

- Make a branch: `git checkout -b fix/pass-mvp`
- Commit your current state: `git add -A && git commit -m "chore: snapshot before PASS MVP patches"`

### 1) `checkout/models.py` → **REPLACE FILE**

- Path: `checkout/models.py`
- Replace the full file with the **Order**/**OrderLineItem** model code from the “Minimal code patches” section.
- Then run:
  ```bash
  python manage.py makemigrations checkout
  python manage.py migrate
  ```

### 2) `checkout/forms.py` → **REPLACE FILE** (or **CREATE** if missing)

- Path: `checkout/forms.py`
- Paste the `OrderForm` code exactly as given.

### 3) `checkout/views.py` → **REPLACE FILE**

- Path: `checkout/views.py`
- The current file is truncated. Replace it with the full snippet (PaymentIntent setup, `_calc_bag_items_and_total`, `checkout`, `checkout_success`).

### 4) `checkout/urls.py` → **REPLACE FILE** (or **CREATE**)

- Path: `checkout/urls.py`
- Paste the snippet with two routes: `''` and `success/<int:order_id>/`.

### 5) Project URL wiring → **EDIT **``

Add these lines if they’re not already present:

```python
from django.urls import include, path

urlpatterns = [
    # ... existing patterns ...
    path('bag/', include('bag.urls')),
    path('checkout/', include('checkout.urls')),
]
```

> Keep existing patterns for `home`, `products`, `custom_cake`.

### 6) Checkout templates → **REPLACE/CREATE FILES**

- Path: `templates/checkout/checkout.html` → **REPLACE** with provided snippet
- Path: `templates/checkout/checkout_success.html` → **REPLACE** with provided snippet

### 7) `bag/views.py` → **REPLACE FILE**

- Path: `bag/views.py`
- Replace with the minimal server-side add/view implementation.

### 8) `bag/urls.py` → **REPLACE FILE** (or **CREATE**)

- Path: `bag/urls.py`
- Paste the two routes: `''` and `add/<int:product_id>/`.

### 9) Bag template → **REPLACE/CREATE FILE**

- Path: `templates/bag/bag.html`
- Paste the minimal template from the snippet.

### 10) `base.html` fallback (only if your current base is broken)

If `templates/base.html` is truncated and causing render errors, use this **temporary minimal** base and iterate later:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Cake It Easy</title>
  <meta name="description" content="Custom cakes and accessories – order online.">
  {% load static %}
  <link rel="stylesheet" href="{% static 'css/base.css' %}">
</head>
<body>
  <nav>
    <a href="/">Home</a>
    <a href="/products/">Products</a>
    <a href="/bag/">Bag</a>
    <a href="/checkout/">Checkout</a>
  </nav>

  {% if messages %}
    <ul class="msgs">{% for m in messages %}<li>{{ m }}</li>{% endfor %}</ul>
  {% endif %}

  <main>
    {% block content %}{% endblock %}
  </main>
</body>
</html>
```

### 11) `settings.py` sanity

No breaking changes required. For Stripe, add these to your **env** (not committed):

```
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_CURRENCY=eur
```

> The code handles missing keys by showing a warning and proceeding without charge for demo—use real test keys for at least one screenshot.

### 12) Quick run & smoke test

```bash
python manage.py collectstatic --noinput  # if you have static configured
python manage.py runserver
```

- Create 2–3 products (admin)
- Add one to bag → go to `/checkout/` → complete order → see success page
- With Stripe test keys set, verify a **PaymentIntent** in Stripe Dashboard

### 13) RBAC lock (minimal)

- In templates, wrap Product CRUD buttons with `{% if request.user.is_staff %}...{% endif %}`
- In views handling add/edit/delete products, add `from django.contrib.admin.views.decorators import staff_member_required` and decorate: `@staff_member_required`

### 14) Evidence to capture (for README/pass)

- Success page screenshot + Stripe dashboard payment
- Console/email output screenshot
- W3C validator pass for Home/Products/Detail/Checkout
- ERD image (Category ↔ Product ↔ Order ↔ LineItem)

---

## ✅ Acceptance checks (what to verify before pushing)

- Checkout flow works locally, creates **Order + LineItems**
- Messages shown on success/failure
- Non‑staff cannot see or access product CRUD
- No broken links in navbar/footer/logo
- Minimal SEO files present (meta description, robots.txt, sitemap route, 404 page)

## 📦 Commit sequence (recommended)

```bash
git add -A
git commit -m "feat(checkout): restore models, views, urls, templates (PaymentIntent MVP)"

git commit -m "feat(bag): minimal add/view flow + urls + template"

git commit -m "fix(base): temporary minimal base layout with messages + nav"

git commit -m "chore: urls wiring + settings stripe env usage"
```

---

## When you’re back

We’ll run through the demo script, take the screenshots, and I’ll mark the PASS checklist ✅/⏳/❌ accordingly.



---

## Heroku Python runtime fix — replace `runtime.txt` with `.python-version`
> Heroku now prefers **`.python-version`** (major.minor only) and deprecates `runtime.txt`.

### What to do
1) **Delete** `runtime.txt` from the repo (if present).
2) **Create** a file named `.python-version` at the repo root with this exact content:
   ```
   3.12
   ```
   > Do **not** add quotes or `python-` prefix; don’t pin a patch (Heroku will use latest 3.12.x).

### PowerShell commands (from repo root)
```powershell
# Remove runtime.txt if it exists and is tracked
if (Test-Path .untime.txt) {
  git rm runtime.txt
}

# Create .python-version with major.minor only
Set-Content -Path .\.python-version -Value "3.12"

# Commit and push (adjust branch if needed)
git add .python-version
git commit -m "chore(heroku): switch to .python-version (3.12)"
```

If you deploy from GitHub → **push to main**, then in Heroku **Deploy → Deploy Branch** (or wait for auto). If you deploy via Heroku git remote, push `main` there.

After build:
- **Overview → More → Restart all dynos**
- **More → View logs** to confirm the warning is gone and Python 3.12.x is selected

### Troubleshooting
- Build fails with “No default language could be detected” → ensure `requirements.txt` is at the **repo root**.
- Still seeing the old warning → confirm there is **no** `runtime.txt` left in the repo and the new slug was deployed (rebuild from Deploy tab).
- If you previously committed a `runtime.txt` in another branch, ensure it’s removed on `main` too before deploying.



---

## Day‑3 Kickoff (PASS‑focused)
**Goal:** ship a credible demo path (products visible, smooth Add→Bag→Checkout, Stripe test proof, README evidence). Keep to minimum—no extras.

### 1) Seed demo products (fastest path)
- Option A (Admin): Heroku → More → Run console → `python manage.py createsuperuser` → add 6 items.
- Option B (Fixture):
  1. Create `products/fixtures/products.json` with 4–6 items (use the example below, then tweak names/prices).
  2. Local: `python manage.py loaddata products/fixtures/products.json`
  3. Commit & push → Deploy → Restart dynos.

**Example (start small, edit later):**
```json
[
  {"model":"products.category","pk":1,"fields":{"name":"cakes","friendly_name":"Cakes"}},
  {"model":"products.product","pk":1,"fields":{"category":1,"sku":"CK-001","name":"Vanilla Celebration","description":"Classic vanilla sponge.","price":"24.99","is_custom":false,"is_accessory":false,"is_offer":false}},
  {"model":"products.product","pk":2,"fields":{"category":1,"sku":"CK-002","name":"Chocolate Fudge","description":"Rich chocolate cake.","price":"29.99","is_custom":false,"is_accessory":false,"is_offer":true}},
  {"model":"products.product","pk":3,"fields":{"category":1,"sku":"CK-003","name":"Red Velvet","description":"Cream cheese frosting.","price":"27.50","is_custom":false,"is_accessory":false,"is_offer":false}}
]
```

### 2) Home hero cleanup & tiny CSS
- Replace any `{# … #}` Django comments that are *rendering* with HTML comments `<!-- … -->` in `home/templates/home/index.html`.
- Minimal spacing fix in `static/css/base.css` (keep very small):
```css
main { padding-bottom: 2rem; }
.container { max-width: 1140px; }
```

### 3) Stripe test proof (screenshots for README)
- Heroku → Settings → Config Vars: set `STRIPE_PUBLIC_KEY` & `STRIPE_SECRET_KEY` (test keys).
- Live flow: Add item → Bag → Checkout → pay with `4242 4242 4242 4242`, any future date, CVC any 3.
- Take screenshots: Checkout form, Success page, Stripe Dashboard PaymentIntent.

### 4) README essentials (evidence‑first)
Create/extend sections:
- **Project summary** (1–2 lines), **Live site link**, **Repo link**
- **Features:** Products list/detail, Add to Bag, Checkout (PaymentIntent or Demo fallback), Admin‑only CRUD
- **How to run locally:** Python/venv, `pip install -r requirements.txt`, `.env` keys, `python manage.py migrate && runserver`
- **Env vars:** `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `DATABASE_URL`, `CLOUDINARY_URL`, `STRIPE_PUBLIC_KEY`, `STRIPE_SECRET_KEY`
- **Testing the checkout:** Stripe test card details
- **Screenshots gallery:** home, list, detail, bag, checkout, success, Stripe dashboard, RBAC (staff vs non‑staff)
- **Credits & Acknowledgements**

### 5) RBAC proof (2 screenshots)
- Non‑staff user: no Add/Edit/Delete buttons; direct URL blocked.
- Staff user: buttons visible; can add/edit/delete.

### 6) Quick link sweep (5 min)
- Navbar/logo/footer use `{% url '...' %}` only.
- 404 present (simple template) and `robots.txt` served from `static/robots.txt`.

### Acceptance checks (before calling it “ready”)
- Live site renders home, products list/detail.
- Add → Bag → Checkout works; demo fallback if Stripe misconfigured.
- One Stripe test payment captured.
- Admin‑only CRUD enforced; non‑staff blocked.
- README has evidence screenshots and local run instructions.

---

## Backup & Export (so nothing gets lost)
**Code:**
- `git push origin main` after each block of changes.
- Optionally tag a stable point: `git tag -a v0.1-pass-mvp -m "PASS MVP" && git push origin v0.1-pass-mvp`.

**Chat & Canvas (ChatGPT):**
- Settings → **Data controls** → **Export** → confirm. You’ll receive a ZIP containing chats, canvases, and files.
- For a single conversation: open the chat → **⋯** (top‑right) → **Share/Export** or print to PDF (Ctrl/Cmd+P → Save as PDF).

**Heroku runtime reminder:**
- Use `.python-version` with `3.12` at repo root (we added instructions above). Delete any `runtime.txt` left in branches.



---

# ✅ Copy‑paste Code Pack — Bag, Checkout, Stripe (incl. Webhooks)
> Scope: minimal, PASS‑oriented files only. Each block says **REPLACE** or **CREATE** and the exact **path**. After pasting, run the commands at the end.

## Env vars required (local `.env` & Heroku Config Vars)
```
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_CURRENCY=eur
# Stripe → Developers → Webhooks → Click endpoint → Reveal signing secret
STRIPE_WEBHOOK_SECRET=whsec_...
```

---

## 1) `bag/context_processors.py` — **REPLACE/CREATE**
```python
from decimal import Decimal

def bag_totals(request):
    bag = request.session.get('bag', {})
    count = 0
    for _, qty in bag.items():
        try:
            count += int(qty)
        except Exception:
            pass
    # Header shows count; precise totals calculated in checkout
    return {"bag_count": count, "bag_total": Decimal("0.00")}
```

## 2) `bag/views.py` — **REPLACE**
```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product


def view_bag(request):
    # Minimal page with checkout button; items are shown on checkout page
    return render(request, 'bag/bag.html')


def add_to_bag(request, product_id):
    if request.method != 'POST':
        return redirect('product_detail', product_id=product_id)
    product = get_object_or_404(Product, pk=product_id)
    try:
        qty = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        qty = 1
    qty = max(1, qty)

    bag = request.session.get('bag', {})
    pid = str(product_id)
    bag[pid] = bag.get(pid, 0) + qty
    request.session['bag'] = bag

    messages.success(request, f"Added {qty} × {product.name} to your bag.")
    return redirect('view_bag')
```

## 3) `bag/urls.py` — **REPLACE/CREATE**
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_bag, name='view_bag'),
    path('add/<int:product_id>/', views.add_to_bag, name='add_to_bag'),
]
```

## 4) `bag/templates/bag/bag.html` — **REPLACE/CREATE**
```html
{% extends 'base.html' %}
{% block content %}
  <div class="container mt-5">
    <h1>Your Bag</h1>
    <p class="mt-3">
      <a class="btn btn-primary" href="{% url 'checkout' %}">Proceed to Checkout</a>
    </p>
  </div>
{% endblock %}
```

---

## 5) `checkout/models.py` — **REPLACE**
```python
from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    full_name = models.CharField(max_length=80)
    email = models.EmailField()
    phone_number = models.CharField(max_length=32, blank=True)
    country = models.CharField(max_length=40, blank=True)
    postcode = models.CharField(max_length=20, blank=True)
    town_or_city = models.CharField(max_length=40, blank=True)
    street_address1 = models.CharField(max_length=80, blank=True)
    street_address2 = models.CharField(max_length=80, blank=True)

    order_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stripe_pid = models.CharField(max_length=254, blank=True)
    original_bag = models.TextField(blank=True)
    paid = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    lineitem_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order {self.order_id})"
```

## 6) `checkout/forms.py` — **REPLACE/CREATE**
```python
from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'full_name', 'email', 'phone_number', 'country', 'postcode',
            'town_or_city', 'street_address1', 'street_address2'
        )
```

## 7) `checkout/views.py` — **REPLACE**
```python
import json
from decimal import Decimal

import stripe
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render, reverse

from products.models import Product
from .forms import OrderForm
from .models import Order, OrderLineItem

STRIPE_ENABLED = bool(getattr(settings, "STRIPE_PUBLIC_KEY", "") and getattr(settings, "STRIPE_SECRET_KEY", ""))
if STRIPE_ENABLED:
    stripe.api_key = settings.STRIPE_SECRET_KEY


def _calc_bag_items_and_total(request):
    bag = request.session.get('bag', {})
    items, total = [], Decimal('0.00')
    for pid, qty in bag.items():
        product = get_object_or_404(Product, pk=int(pid))
        line_total = product.price * qty
        items.append({'product': product, 'quantity': qty, 'line_total': line_total})
        total += line_total
    return items, total


def checkout(request):
    items, total = _calc_bag_items_and_total(request)
    if not items:
        messages.info(request, "Your bag is empty.")
        return redirect('product_list')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            client_secret = request.POST.get('client_secret', '')
            pid = client_secret.split('_secret')[0] if '_secret' in client_secret else ''

            order = form.save(commit=False)
            order.user = request.user if request.user.is_authenticated else None
            order.order_total = total
            order.stripe_pid = pid
            order.original_bag = json.dumps(request.session.get('bag', {}))
            order.save()

            for i in items:
                OrderLineItem.objects.create(order=order, product=i['product'], quantity=i['quantity'])

            request.session['bag'] = {}

            try:
                send_mail(
                    subject=f"Cake It Easy — Order #{order.id} confirmed",
                    message=f"Thanks for your order! Total: €{order.order_total}",
                    from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
                    recipient_list=[order.email],
                    fail_silently=True,
                )
            except Exception:
                pass

            messages.success(request, f"Order placed! Reference #{order.id}")
            return redirect(reverse('checkout_success', args=[order.id]))
    else:
        form = OrderForm()

    # GET branch: create PaymentIntent if Stripe is enabled; else demo mode
    client_secret = ''
    do_stripe = STRIPE_ENABLED
    if do_stripe:
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(total * 100),
                currency=getattr(settings, 'STRIPE_CURRENCY', 'eur'),
                metadata={'integration': 'cake_it_easy_v2'},
            )
            client_secret = intent.client_secret
        except stripe.error.AuthenticationError:
            messages.error(request, "Stripe keys look invalid. Continuing without payment for now.")
            do_stripe = False
        except Exception:
            messages.error(request, "Stripe is temporarily unavailable. Continuing without payment.")
            do_stripe = False

    if not do_stripe:
        client_secret = "test_secret_disabled"
        messages.warning(request, "Stripe is not configured. Running in no-payment demo mode.")

    return render(request, 'checkout/checkout.html', {
        'form': form,
        'items': items,
        'total': total,
        'stripe_public_key': getattr(settings, "STRIPE_PUBLIC_KEY", ""),
        'client_secret': client_secret,
    })


def checkout_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'checkout/checkout_success.html', {'order': order})
```

## 8) `checkout/templates/checkout/checkout.html` — **REPLACE**
```html
{% extends 'base.html' %}
{% load static %}
{% block content %}
  <div class="container mt-5">
    <h1 class="mb-3">Checkout</h1>

    <ul class="list-unstyled">
      {% for i in items %}
        <li>{{ i.product.name }} × {{ i.quantity }} — €{{ i.line_total }}</li>
      {% endfor %}
    </ul>
    <p class="lead"><strong>Total: €{{ total }}</strong></p>

    <form id="checkout-form" method="POST" class="card card-body mt-3">
      {% csrf_token %}
      {{ form.as_p }}
      <input type="hidden" name="client_secret" id="client_secret" value="{{ client_secret }}">

      {% if stripe_public_key and client_secret and client_secret != 'test_secret_disabled' %}
        <hr>
        <h5>Card details</h5>
        <div id="card-element" class="form-control" style="padding:.6rem .75rem;"></div>
        <div id="card-errors" class="text-danger mt-2" role="alert"></div>
        <button type="submit" id="pay-btn" class="btn btn-primary mt-3">Pay €{{ total }}</button>
      {% else %}
        <button type="submit" class="btn btn-primary mt-3">Place Order</button>
        <p class="text-muted small mt-2">Payment is disabled in this environment. Your order will still be recorded for assessment.</p>
      {% endif %}
    </form>
  </div>

  {% if stripe_public_key and client_secret and client_secret != 'test_secret_disabled' %}
    <script src="https://js.stripe.com/v3/"></script>
    <script>
      (function () {
        const stripe = Stripe("{{ stripe_public_key }}");
        const clientSecret = "{{ client_secret }}";
        const elements = stripe.elements();
        const card = elements.create('card');
        card.mount('#card-element');

        const form = document.getElementById('checkout-form');
        const payBtn = document.getElementById('pay-btn');
        const errorBox = document.getElementById('card-errors');

        form.addEventListener('submit', async (e) => {
          e.preventDefault();
          if (payBtn) payBtn.disabled = true;
          errorBox.textContent = '';

          const billingDetails = {
            name: document.getElementById('id_full_name')?.value || '',
            email: document.getElementById('id_email')?.value || '',
            address: {
              line1: document.getElementById('id_street_address1')?.value || '',
              line2: document.getElementById('id_street_address2')?.value || '',
              postal_code: document.getElementById('id_postcode')?.value || '',
              city: document.getElementById('id_town_or_city')?.value || '',
              country: document.getElementById('id_country')?.value || '',
            }
          };

          const { error, paymentIntent } = await stripe.confirmCardPayment(clientSecret, {
            payment_method: { card, billing_details: billingDetails }
          });

          if (error) {
            errorBox.textContent = error.message || 'Payment failed. Please try again.';
            if (payBtn) payBtn.disabled = false;
            return;
          }
          if (paymentIntent && paymentIntent.status === 'succeeded') form.submit();
          else {
            errorBox.textContent = 'Payment not completed. Please try again.';
            if (payBtn) payBtn.disabled = false;
          }
        });
      })();
    </script>
  {% endif %}
{% endblock %}
```

## 9) `checkout/templates/checkout/checkout_success.html` — **REPLACE/CREATE**
```html
{% extends 'base.html' %}
{% block content %}
  <div class="container mt-5">
    <h1>Thanks!</h1>
    <p>Your order number is <strong>#{{ order.id }}</strong>.</p>
  </div>
{% endblock %}
```

## 10) `checkout/webhooks.py` — **CREATE**
```python
import json
import stripe
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import Order

@csrf_exempt
def stripe_webhook(request):
    \"\"\"Minimal webhook to mark orders paid when Stripe confirms payment.\"\"\"
    webhook_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', '')
    if not webhook_secret:
        # No secret configured: acknowledge to avoid retries but do nothing
        return HttpResponse(status=200)

    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')

    try:
        event = stripe.Webhook.construct_event(
            payload=payload, sig_header=sig_header, secret=webhook_secret
        )
    except Exception:
        return HttpResponseBadRequest()

    if event.get('type') == 'payment_intent.succeeded':
        pid = event['data']['object']['id']
        try:
            order = Order.objects.get(stripe_pid=pid)
            if not order.paid:
                order.paid = True
                order.save(update_fields=['paid'])
        except Order.DoesNotExist:
            pass  # Optional: log for reconciliation

    # You can handle other event types if desired
    return HttpResponse(status=200)
```

## 11) `checkout/urls.py` — **REPLACE**
```python
from django.urls import path
from . import views
from . import webhooks

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('success/<int:order_id>/', views.checkout_success, name='checkout_success'),
    path('wh/', webhooks.stripe_webhook, name='stripe_webhook'),
]
```

## 12) Project URLs — **EDIT `cake_it_easy_v2/urls.py`** (ensure these lines exist)
```python
from django.urls import include, path

urlpatterns = [
    # ... existing patterns ...
    path('bag/', include('bag.urls')),
    path('checkout/', include('checkout.urls')),
]
```

---

## Commands to run (local first, then Heroku console)
```bash
# Local
python manage.py makemigrations checkout
python manage.py migrate
python manage.py runserver

# Heroku (Dashboard → More → Run console)
python manage.py migrate
python manage.py collectstatic --noinput
```

## Stripe webhook setup (test mode)
1) Stripe Dashboard → **Developers → Webhooks → Add endpoint**.
2) URL: `https://<your-heroku-app>.herokuapp.com/checkout/wh/`.
3) Select events: **payment_intent.succeeded** (and optionally payment_intent.payment_failed).
4) After creating, click the endpoint → **Reveal signing secret** → set it as `STRIPE_WEBHOOK_SECRET` in Heroku **Config Vars**.

## Acceptance checks
- Add product → **Bag** → **Checkout** page renders with correct total.
- With test keys set: enter `4242 4242 4242 4242` → payment succeeds → order saved → redirect to success page.
- Stripe Dashboard shows the PaymentIntent; webhook marks the order **paid=True**.
- With Stripe keys unset/invalid: friendly warning; order still records (demo mode) without crash.
- Non‑staff users don’t see product CRUD controls; staff do.



---

## Bag module review — fixes & morning checklist
**Status:** URLs and views are correctly wired; context processor present; template path correct. Minimal fixes below to harden for PASS.

### 1) Harden optional legacy context (`bag/contexts.py`) — REPLACE
```python
from decimal import Decimal
from products.models import Product


def bag_contents(request):
    """
    Safe bag contents for templates (only if you explicitly use it).
    Not registered by default; 'bag.context_processors.bag_totals' is used for header count.
    """
    bag = request.session.get('bag', {})
    items = []
    total = Decimal('0.00')

    # Collect all product ids in one query
    ids = [int(pid) for pid in bag.keys()]
    products = {p.id: p for p in Product.objects.filter(id__in=ids)}

    for pid_str, qty in bag.items():
        try:
            pid = int(pid_str)
            product = products.get(pid)
            if not product:
                continue
            line_total = product.price * qty
            items.append({
                'product': product,
                'quantity': qty,
                'line_total': line_total,
            })
            total += line_total
        except Exception:
            # Skip any bad entries rather than crashing
            continue

    return {
        'bag_items': items,
        'bag_total': total,
        'bag_count': sum(bag.values()) if bag else 0,
    }
```
> Alternatively: delete `bag/contexts.py` if unused to avoid confusion.

### 2) Comment sync in `bag/views.py` (optional tidy)
Change the final comment to reflect current behavior:
```python
# For the PASS demo flow, redirect to the Bag so users can proceed to checkout
return redirect('view_bag')
```

### 3) Settings tidy (optional)
Remove the earlier env-based `EMAIL_BACKEND` so there’s only one:
- Keep: `EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"`
- Remove the earlier `EMAIL_BACKEND = os.getenv(...` line.

### Morning quick test
1) Product detail → **Add to Bag** → lands on **/bag/** with success message; header count updates.
2) **Proceed to Checkout** → totals render correctly; can place order in demo mode.
3) With Stripe keys + webhook set: card `4242 4242 4242 4242` → success → order saved → webhook flips `paid=True`.

### One last file to confirm
Please paste `templates/base.html` tomorrow so I can verify `{% load static %}`, messages block, and referenced static assets. That’s the final guardrail for avoiding production 500s.

