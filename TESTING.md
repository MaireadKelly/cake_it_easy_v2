# TESTING.md

<!--
This TESTING document is structured for Code Institute PP5.
Work through the checklists and attach screenshots with the exact filenames below.
-->

## Overview
Comprehensive manual & automated testing for **Cake It Easy**.

- **Test accounts:**
  - Customer: `testuser@example.com` / `Pass1234!` (or use Allauth signup)
  - Staff/Admin: `admin@example.com` / `AdminPass1234!`
- **Browsers:** Chrome (primary), Firefox, Edge, Safari (where possible).
- **Devices:** Desktop 1440px, Laptop 1366px, iPad, iPhone/Android (responsive).
- **Data:** Demo products loaded via fixtures or admin.

## Test Evidence Index (Screenshots/Reports)
All files stored under `docs/testing/` unless otherwise stated.

### 1) User Stories — Acceptance Tests (manual)
- `us-guest-browse-categories.png`
- `us-search-products.png`
- `us-sort-price-name.png`
- `us-view-product-detail.png`
- `us-add-to-basket.png`
- `us-update-remove-basket.png`
- `us-checkout-stripe-elements.png`
- `us-order-confirmation-email.png`
- `us-profile-order-history.png`
- `us-custom-cake-submit.png`

### 2) Functional Areas
- Products: `func-products-list.png`, `func-products-detail.png`
- Basket: `func-basket-add.png`, `func-basket-update.png`, `func-basket-remove.png`
- Checkout: `func-checkout-success.png`, `func-checkout-webhook-log.png`
- Accounts: `func-register.png`, `func-login.png`, `func-logout.png`
- Admin: `func-admin-add-product.png`, `func-admin-edit-product.png`
- Errors: `func-404-page.png`, `func-500-simulated.png`

### 3) Responsiveness
- `resp-home-mobile.png`, `resp-home-tablet.png`, `resp-home-desktop.png`
- `resp-product-list-mobile.png`, `resp-product-detail-mobile.png`
- `resp-basket-mobile.png`, `resp-checkout-mobile.png`

### 4) Accessibility & Performance
- Lighthouse: `lh-home-mobile.png`, `lh-home-desktop.png`
- WAVE: `wave-home.png`, `wave-product.png`
- Axe DevTools: `axe-checkout.png`

### 5) Validation
- HTML (W3C): see [Validation](#validation) for file list & attach per‑page `*.png`.
- CSS (W3C): `val-css-base.png`
- JS (JSHint): `val-js-basket.png`, `val-js-checkout.png`
- Python (PEP8CI): `val-pep8-summary.png`

---

## Manual Test Plan — Step‑by‑Step Checklist

> Work through each section in order; mark ✅/❌ and add notes.

### A. Global Navigation & Layout
1. Header brand links to Home.  
2. Navbar links: Home, Our Story, Shop Now, Custom Cakes, Account, Basket.  
3. Search bar returns results; empty query shows message.  
4. Toast messages appear/disappear correctly.  
5. Footer links work and open in correct tab.

### B. Products & Catalogue
1. List page shows cards with name, price, category badge.  
2. Sorting: by price (low→high, high→low), name (A→Z), category; persists in querystring.  
3. Filtering: category chips/dropdowns combine with search.  
4. Pagination (if implemented) preserves filters.

### C. Product Detail
1. Quantity selector min=1; prevents non‑numeric input.  
2. Add to basket shows updated mini‑summary.  
3. Back to results preserves previous sort/filter.

### D. Basket (Bag)
1. Displays each line with product name, options, subtotal.  
2. Update quantity (0 removes item).  
3. Basket total updates correctly including delivery threshold (e.g., free over €50).  
4. Continue shopping / Secure checkout buttons work.

### E. Checkout — Stripe Payment Intents
1. Stripe Elements renders and blocks invalid inputs.  
2. Billing/shipping form validates required fields.  
3. Successful payment path → Order Confirmation page.  
4. Failed/declined card shows clear error; user can retry.  
5. Webhook creates Order on delayed confirmation (if client interrupted).  
6. Confirmation email received (console in dev; SMTP in prod).  
7. `stripe_pid` stored on `Order`; totals match basket.

### F. Profiles
1. Auth required to view Profile; redirect to login if unauthenticated.  
2. Default delivery info saves/loads correctly.  
3. Order history shows most recent first; links to order detail.

### G. Custom Cake Flow
1. Form fields validate (date in future, required options selected).  
2. Submits and creates record (or quote request) with success message.  
3. Appears in admin; staff can update status.

### H. Admin & RBAC
1. Staff‑only CRUD on Products/Categories.  
2. Non‑staff blocked from admin URL and from staff views/buttons.  
3. Images upload to Cloudinary and show in templates.

### I. Error Handling & Security
1. Custom 404 page displays and links back to shop/home.  
2. With `DEBUG=False`, static files serve and CSRF works.  
3. `SECURE_` settings active on production (HTTPS redirect).  
4. Sensitive keys only via env/config vars.

### J. Accessibility
1. All images have meaningful alt text.  
2. Headings are hierarchical (h1→h2→h3...).  
3. Labels/aria‑attributes on forms/interactive controls.  
4. Keyboard tab order is logical; visible focus states.  
5. Colour contrast meets WCAG AA; check using Lighthouse/WAVE.

### K. Performance
1. Lighthouse Performance ≥ 80 on Home.  
2. Unused images/CSS removed; images sized appropriately.  
3. Caching headers (Heroku default) acceptable.

---

## Automated Tests (if included)
- Example: Model tests for `Order` calculations.  
- Example: View tests for product list filters.

Run:
```bash
python manage.py test
```
Screenshots: `unit-tests-summary.png`.

---

## Validation

### HTML (W3C)
Validate these rendered pages (production if possible):

- `/` → `validation-html-home.png`
- `/products/` → `validation-html-products-list.png`
- `/products/<slug-or-id>/` → `validation-html-product-detail.png`
- `/basket/` → `validation-html-basket.png`
- `/checkout/` → `validation-html-checkout.png`
- `/accounts/login/` → `validation-html-login.png`
- `/accounts/signup/` → `validation-html-signup.png`
- `/profile/` → `validation-html-profile.png`
- `/custom_cake/` → `validation-html-custom-cake.png`
- `404` page (trigger a non‑existent URL) → `validation-html-404.png`

### CSS (W3C Jigsaw)
- `static/css/base.css` → `validation-css-base.png`
- (Any additional CSS files) → `validation-css-extra.png`

### JavaScript (JSHint)
- `static/js/stripe_elements.js` → `validation-js-stripe.png`
- `static/js/bag.js` (or basket related) → `validation-js-bag.png`
- (Any additional JS files) → `validation-js-extra.png`

### Python (PEP8 / Flake8 / PEP8CI)
- Run linter; attach summary: `val-pep8-summary.png`  
- If using PEP8CI website: `val-pep8ci-app.png`.

### Accessibility
- WAVE on Home & Product → `accessibility-wave-home.png`, `accessibility-wave-product.png`
- Axe DevTools on Checkout → `accessibility-axe-checkout.png`

### Performance
- Lighthouse Mobile/Desktop on Home → `lighthouse-home-mobile.png`, `lighthouse-home-desktop.png`

---

## Bugs & Resolutions Log
Maintain a simple table of significant bugs fixed during testing.

| ID | Summary | Where | Steps to Reproduce | Fix | Screenshot |
|---|---|---|---|---|---|
| B‑001 | 500 on checkout with DEBUG=False | Heroku logs | Go to /checkout | Added ALLOWED_HOSTS, COLLECTSTATIC, fixed STATIC_ROOT | `bug-500-fix.png` |
| B‑002 | Stripe webhook 400 | Webhooks | Test endpoint | Corrected `STRIPE_WH_SECRET` | `bug-webhook-400.png` |

---

## How to Re‑run Key Tests Quickly
```bash
# Start server
python manage.py runserver

# Create a test order using Stripe test card
# 4242 4242 4242 4242, future expiry, any CVC, any postcode
```

---

## Final Sign‑off Checklist
- [ ] All screenshots saved in `docs/readme/` and `docs/testing/` and referenced correctly.
- [ ] Validation screenshots attached for HTML, CSS, JS, Python.
- [ ] README sections complete (Deployment, Credits, UX, Features).
- [ ] TESTING.md updated with ✅/❌ per checklist.
- [ ] DEBUG=False on production; all secrets in config vars.
```
