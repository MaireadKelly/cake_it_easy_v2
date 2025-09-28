# TESTING.md

## Overview
Testing combines **automated unit tests** for critical flows with a concise **manual matrix** aligned to rubric requirements. Screenshots are stored in `docs/screens/` and referenced below.

---

## Automated Tests
_Run_: `python manage.py test` → **OK (all green)**

- `bag/tests/test_views.py` – render + add/adjust/remove
- `products/tests/test_rbac.py` – non‑staff blocked on product CRUD
- `custom_cake/tests.py` – create/update/delete; invalid create message; update persists name

_Insert screenshot of green test run_

---

## Manual Test Matrix
| Area | Scenario | Steps | Expected |
|---|---|---|---|
| Products | View list | Visit `/products/` | Grid renders; links work |
| Products | Detail | Open a product | Add‑to‑bag visible; price shown |
| Bag | Add item | From detail, add qty 1 | Toast + bag count updates |
| Bag | Adjust qty/remove | On `/bag/` change qty/remove | Totals recalc; threshold messaging updates |
| Checkout | Payment | Card `4242 4242 4242 4242` + valid form | Success page shows **order number** |
| Webhook | Mark paid | Stripe Events shows delivered | Order flips to `paid=True` |
| Profile | Save defaults | Update and submit | Success message; values persist |
| Orders | History | `/checkout/orders/` | Orders list shows recent order |
| Orders | Detail (owner‑only) | Open `/checkout/orders/<id>/` | Owner/staff can view; others denied |
| Custom Cake | Create valid | Minimal required fields | Redirect to detail; success message |
| Custom Cake | Create invalid | Past **Needed for** date | Validation error shown |
| Custom Cake | Update | Change name | Saved; detail shows updated name |
| Custom Cake | Delete | Confirm delete | Redirect to list; message contains “deleted successfully” |
| RBAC | Hide admin links | As non‑staff | No product edit/delete links |
| RBAC | Block admin routes | Hit edit URL as non‑staff | Redirect/403 |
| Auth | Login/Signup | Use valid/invalid | Errors shown; success redirects |
| Auth | Logout | Confirm via card | Session cleared; redirected |
| Allauth UI | Forms layout | Login/Signup/Reset/Logout | Centered card; **Cancel** buttons present |
| SEO/404 | 404 page | Bad URL with `DEBUG=False` | Branded 404 |
| Footer | Sticky footer | Short page (e.g., logout) | Footer sticks to bottom |

_Evidence_: drop screenshots for each row into `docs/screens/` and reference them inline in this file if desired.

---

## Validation
- **HTML**: W3C – key pages pass (screenshots)  
- **CSS**: Jigsaw – `base.css` passes  
- **Python**: PEP8 (CI tool) – first‑party files pass  
- **Lighthouse**: Mobile & Desktop snapshots; no mixed‑content; reasonable scores (attach images)

---

## Browser & Device Coverage
- Chrome, Firefox, Edge, Safari  
- iOS Safari/Chrome, Android Chrome  
- Responsive checks at 360px, 768px, 1024px, 1440px

---

## Known Issues / Out‑of‑Scope
- Newsletter/stub pages may be linked to About or removed to avoid 404s.  
- Advanced product filters and marketing integrations are **out of scope**.

---

## Evidence Index (suggested filenames)
- `docs/screens/checkout-success-order-number.png`
- `docs/screens/stripe-event-delivered.png`
- `docs/screens/admin-order-paid-true.png`
- `docs/screens/profile-saved.png`
- `docs/screens/my-orders.png`
- `docs/screens/order-detail.png`
- `docs/screens/custom-cake-create.png`
- `docs/screens/custom-cake-edit.png`
- `docs/screens/custom-cake-delete.png`
- `docs/screens/allauth-login.png`
- `docs/screens/allauth-signup.png`
- `docs/screens/allauth-reset.png`
- `docs/screens/allauth-logout.png`
- `docs/screens/404.png`
- `docs/screens/lighthouse-desktop.png`, `lighthouse-mobile.png`
- `docs/validation/html-validation.png`, `css-validation.png`, `pep8.png`

