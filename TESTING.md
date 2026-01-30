# TESTING.md

## Table of Contents

- [Overview](#overview)
- [Automated Tests](#automated-tests)
- [Manual Test Matrix](#manual-test-matrix)
  - [Manual Test 1: Products List](#)
  - [Manual Test 2: Product Detail](#)
  - [Manual Test 3: Shopping Bag](#)
  - [Manual Test 4: Checkout & Payment](#)
  - [Manual Test 5: Authentication & Profiles](#manual-test-5-authentication--profiles)
- [Validation](#validation)
  - [Python (PEP8 / pycodestyle)](#python-pep8--pycodestyle--79-cols)
  - [HTML (W3C Validator)](#html-w3c-validator)
  - [CSS (Jigsaw Validator)](#css-jigsaw-validator)
- [Lighthouse Audits](#lighthouse-performance--accessibility--best-practices--seo)
- [Browser & Device Coverage](#browser--device-coverage)
- [Known Issues / Out-of-Scope](#known-issues--out-of-scope)
- [Evidence Index](#evidence-index-examples)


## Overview
This project uses **automated tests**, a concise **manual test matrix**, and **validator evidence**.  
All screenshots are stored in:

- Python (PEP8/pycodestyle): `docs/testing/py/`
- HTML (W3C): `docs/testing/html/`
- CSS (Jigsaw): `docs/testing/css/`
- JavaScript (ESLint): `docs/testing/js/`

For feature descriptions and screenshots, see:
- [README Features section](README.md#features)
- [README SEO evidence](README.md#seo--responsiveness)

### Quick Evidence Links
- [Assessor-critical evidence (screenshots)](TESTING.md#evidence-index-assessor-critical)
- [Manual Test Matrix](TESTING.md#manual-test-matrix)
- [Validation evidence](TESTING.md#validation)



**Naming convention:** screenshots are saved as `val_<path-with-slashes-replaced-by-underscores>.png`.  
Example: `products/views.py` → `docs/testing/py/val_products_views.png`.

---

## Automated Tests

Automated tests were reused from the previous iteration of the project and re-run for this submission to ensure continued correctness after feature and documentation updates.

### Test Coverage

- **Shopping Bag**
  - `bag/tests/test_views.py`
  - Verifies bag page rendering and add / adjust / remove item behaviour.

- **Role-Based Access Control (RBAC)**
  - `products/tests/test_rbac.py`
  - Confirms non-staff users are blocked from product CRUD routes.

- **Custom Cake Requests**
  - `custom_cake/tests.py`
  - Covers create, update, delete flows, validation feedback, and data persistence.

### Test Execution Evidence

![Automated tests passing](docs/testing/py/automated_tests_pass.png)

---

## Manual Test Matrix
### Manual Test 1: Products List
| Area | Scenario | Steps | Expected | Result |
|------|---------|-------|----------|--------|
| Products List | View all products | Navigate to Shop / Products page | Products display in a grid with image, name, price, and category | Pass |
| Category Filter | Filter by Accessories | Click Accessories category | Only accessory products are shown | Pass |
| Category Filter | Filter by Cupcakes | Click Cupcakes category | Only cupcake products are shown with correct pricing indicators | Pass |
| Search | Search for product | Enter keyword in search bar and submit | Matching products are displayed | Pass |
| Sorting | Sort by price (low → high) | Select “Price (Low to High)” from sort dropdown | Products reorder correctly by ascending price | Pass |

### Manual Test 2: Product Detail
| Area           | Scenario                                  | Steps                                            | Expected                                                   | Result |
| -------------- | ----------------------------------------- | ------------------------------------------------ | ---------------------------------------------------------- | ------ |
| Product Detail | Load product detail page                  | Navigate to a product from the product listing   | Product detail page loads without errors                   | Pass   |
| Product Detail | Product information display               | View product name, image, description, and price | All product details are displayed clearly                  | Pass   |
| Product Detail | Cupcake box-size selector (cupcakes only) | Open a cupcake product detail page               | Box-size dropdown is visible above quantity selector       | Pass   |
| Product Detail | Dynamic price calculation                 | Change cupcake box size                          | Price updates dynamically based on selected box size       | Pass   |
| Product Detail | Quantity selector                         | Increase/decrease quantity                       | Quantity updates correctly without page reload             | Pass   |
| Product Detail | Add to bag (standard product)             | Click **Add to Bag**                             | Product is added to the bag and confirmation message shown | Pass   |
| Product Detail | Add to bag (cupcake with option)          | Select box size and add to bag                   | Correct box size and calculated price appear in bag        | Pass   |
| Product Detail | Custom cake CTA                           | Navigate to **Design Your Own** custom cake page | Custom cake form loads successfully                        | Pass   |
| Product Detail | Accessibility check                       | Navigate using keyboard                          | All interactive elements are reachable and usable          | Pass   |

 ### Manual Test 3: Shopping Bag
  
| Area         | Scenario                   | Steps                                                     | Expected                                       | Result |
| ------------ | -------------------------- | --------------------------------------------------------- | ---------------------------------------------- | ------ |
| Shopping Bag | View bag page              | Add an item and navigate to the bag                       | Bag page loads with added items displayed      | Pass   |
| Shopping Bag | Bag line item display      | View product name, image, price, quantity, and line total | All details display correctly                  | Pass   |
| Shopping Bag | Update quantity            | Increase or decrease quantity and click update            | Line total and bag totals update correctly     | Pass   |
| Shopping Bag | Remove item                | Click remove item button                                  | Item is removed and totals recalculate         | Pass   |
| Shopping Bag | Free delivery threshold    | Add items below and above threshold                       | Free delivery message updates correctly        | Pass   |
| Shopping Bag | Discount code apply        | Enter valid discount code and apply                       | Discount is applied and shown in totals        | Pass   |
| Shopping Bag | Discount code invalid      | Enter invalid or empty discount code                      | Error message displayed, no discount applied   | Pass   |
| Shopping Bag | Discount reuse prevention  | Attempt to reuse `WELCOME10` after previous order         | Discount is rejected with informative message  | Pass   |
| Shopping Bag | Discount removal           | Remove applied discount                                   | Discount line removed and totals restored      | Pass   |
| Shopping Bag | Mobile responsiveness      | View bag on mobile screen size                            | All content accessible without layout breakage. On smaller screens, the bag uses horizontal scrolling to preserve full pricing visibility without compressing content. | Pass   |
| Shopping Bag | Horizontal scroll (mobile) | Scroll bag table horizontally on mobile                   | All pricing columns remain accessible          | Pass   |
| Shopping Bag | Accessibility              | Navigate bag using keyboard                               | Controls reachable and usable                  | Pass   |

### Manual Test 4: Checkout & Payment
| Area     | Scenario                    | Steps                                             | Expected                                          | Result |
| -------- | --------------------------- | ------------------------------------------------- | ------------------------------------------------- | ------ |
| Checkout | Access checkout page        | Add item to bag and click **Checkout**            | Checkout page loads with order summary            | Pass   |
| Checkout | Required field validation   | Submit checkout form with required fields missing | Validation messages displayed, form not submitted | Pass   |
| Checkout | Country selection           | Attempt checkout without selecting country        | User prompted to select country                   | Pass   |
| Checkout | Order summary accuracy      | Review items, quantities, and totals on checkout  | Summary matches bag contents                      | Pass   |
| Checkout | Discount persistence        | Apply discount in bag, proceed to checkout        | Discount remains applied in checkout totals       | Pass   |
| Checkout | Stripe card form            | Enter valid Stripe test card details              | Card form accepts input                           | Pass   |
| Checkout | Successful payment          | Complete checkout using test card                 | Payment succeeds, order created                   | Pass   |
| Checkout | Stripe amount               | Complete checkout with discount applied           | Stripe charge reflects discounted total           | Pass   |
| Checkout | PaymentIntent duplication   | Refresh or resubmit checkout                      | Only one payment is created                       | Pass   |
| Checkout | Checkout success page       | Complete successful payment                       | Success page displayed with order confirmation    | Pass   |
| Checkout | Bag cleared                 | Complete checkout                                 | Bag is emptied after order completion             | Pass   |
| Checkout | Order saved                 | View order via profile                            | Order appears in order history                    | Pass   |
| Checkout | Order discount record       | View completed order                              | Discount code and amount stored on order          | Pass   |
| Checkout | Stripe webhooks (test mode) | Complete payment                                  | Webhook received and order marked paid            | Pass   |
| Checkout | Accessibility               | Navigate checkout via keyboard                    | All form fields accessible                        | Pass   |
| Checkout | Mobile checkout             | Complete checkout on mobile viewport              | Checkout usable and readable                      | Pass   |
| Card Number           | Result             |
| ----------------------------- | ------------------ |
| `4242 4242 4242 4242` | Successful payment |
| `4000 0000 0000 0002` | Declined payment   |


### Manual Test 5: Authentication & Profiles
| Area | Scenario | Steps | Expected | Result |
|---|---|---|---|---|
| Auth | Register new user | Go to Register → enter valid details → submit | Account created; success message shown | Pass |
| Auth | Register validation | Submit empty or invalid form | Validation errors displayed | Pass |
| Auth | Login success | Enter valid credentials | User logged in; redirected; success message | Pass |
| Auth | Login failure | Enter invalid credentials | Login blocked; error message shown | Pass |
| Auth | Logout | Click logout | User logged out; confirmation message shown | Pass |
| Profiles | Access profile (logged in) | Login → open Profile | Profile page loads | Pass |
| Profiles | Access profile (logged out) | Logout → visit profile URL | Redirected to login | Pass |
| Profiles | Update delivery details | Edit profile fields → save | Details saved and persist | Pass |
| Profiles | Order history visible | Open profile with orders | Orders listed | Pass |
| Profiles | View order detail | Click order from profile | Order detail page opens | Pass |
| Profiles | Discount shown on order | Place order with discount → view order | Discount visible in order detail | Pass |
| Profiles | Orders scoped to user | Login as different user | Cannot see other users’ orders | Pass |

| Area | Scenario | Steps | Expected | Result |
|------|----------|-------|----------|--------|
| Admin | Admin access, RBAC,  product & order management | 1. Log in as non-staff user and attempt to access `/admin/`.<br>2. Log in as staff/superuser.<br>3. Access Django Admin panel via shortcut.<br>4. Create/edit a product and inline ProductOptions.<br>5. View customer orders and order line items.<br>6. Toggle order `Paid` checkbox and save.<br>7. Use bulk action **Mark selected orders as paid**.<br>8. View custom cake requests including description and image preview. | 1. Non-staff user is denied access (RBAC enforced).<br>2. Staff user can access admin successfully.<br>3. Products and options can be managed.<br>4. Orders and line items are visible.<br>5. Orders can be marked Paid/Unpaid individually or in bulk.<br>6. Custom cake requests display full details and image preview. | Pass |

---

## Validation

### Python (PEP8 / pycodestyle @ 79 cols)

- **Tool:** `pycodestyle`
- **Configuration:** 79-character line length, migrations excluded
- **Command used:**
```bash
pycodestyle bag products custom_cake checkout profiles newsletter home cake_it_easy_v2 --exclude=migrations --max-line-length=79
```
All project Python files pass PEP8 validation with no errors reported.
Minor line-length issues identified during development were resolved prior to final submission.

Clean pycodestyle run (no output indicates zero violations)
![pycodestyle clean run](docs/testing/py/pep8_pass.png)


- **Representative files:**
  Screenshots below demonstrate validation across key areas of the project:
  - Settings: ![settings.py](docs/testing/py/val_settings.png)
  - Project URLs: ![cake_it_easy_v2/urls.py](docs/testing/py/val_project_url.png)
  - Home views: ![home/views.py](docs/testing/py/val_home_views.png)
  - Products models: ![products/models.py](docs/testing/py/val_products_models.png)
  - Custom Cake models: ![custom_cake/models.py](docs/testing/py/val_custom_models.png)
  - Products views: ![products/views.py](docs/testing/py/val_products_views.png)
  - Custom Cake views: ![custom_cake/views.py](docs/testing/py/val_custom_views.png)
  - Checkout models: ![checkout/models.py](docs/testing/py/val_checkout_models.png)
  - One tests file (example): ![custom_cake/tests.py](docs/testing/py/val_custom_tests.png)

---

### HTML (W3C Validator)
- **Tools:** https://validator.w3.org/ (Validate by URL or by direct input).
- **Key templates:**

  - Base layout: ![templates/base.html](docs/testing/html/val_templates_base.png)
  - Products list: ![templates/products/product_list.html](docs/testing/html/val_templates_products_product_list.png)
  - Products detail: ![templates/products/product_detail.html](docs/testing/html/val_templates_products_product_detail.png)
  - Checkout page: ![templates/checkout/checkout.html](docs/testing/html/val_templates_checkout_checkout.png)
  - 404 page: ![templates/404.html](docs/testing/html/val_templates_404.png)


---

### CSS (Jigsaw Validator)
- **Tools:** https://jigsaw.w3.org/css-validator/
- **Stylesheets:**

  - Base stylesheet: ![static/css/base.css](docs/testing/css/val_static_css_base.png)
  - (Optional) Additional CSS: ![static/css/forms.css](docs/testing/css/val_static_css_forms.png)

---

### Lighthouse (Performance / Accessibility / Best Practices / SEO)

We ran Lighthouse in **Chrome DevTools** for both **Desktop** and **Mobile** on key pages.

**How to reproduce**
1. Open page in Chrome → `F12` → **Lighthouse** tab.
2. Categories: Performance, Accessibility, Best Practices, SEO.
3. Run once for **Mobile**, then switch to **Desktop** and run again.
4. Save reports as screenshots (below).

**Results (screenshots)**

| Page | Desktop | Mobile |
|---|---|---|
| Home | ![Lighthouse Home Desktop](docs/testing/lighthouse_home_desk.png) | ![Lighthouse Home Mobile](docs/testing/lighthouse_home_mobile.png) |
| Products list | ![Lighthouse Products List Desktop](docs/testing/lighthouse_product_list_desk.png) | ![Lighthouse Products List Mobile](docs/testing/lighthouse_product_list_mobile.png) |

> If you rename files later (e.g., fix `moblile` → `mobile`), update the paths above accordingly.


---

## Browser & Device Coverage
- Chrome, Firefox, Edge, Safari  
- iOS Safari/Chrome, Android Chrome  
- Responsive checks at 360px, 768px, 1024px, 1440px

_Evidence (optional)_: `docs/testing/html/val_responsive_checks.png`

---

## Known Issues / Out‑of‑Scope
- Newsletter/stub pages may be linked to About or removed to avoid 404s.  
- Advanced product filters and marketing integrations are **out of scope**.
### Known Issues

| Issue | Impact | Status |
|------|-------|--------|
| Mobile bag table requires horizontal scrolling to view all columns | Minor UX issue on small screens; functionality unaffected | Documented for future improvement |

**Notes:**  
On mobile devices, the bag table layout can require horizontal scrolling to view all columns simultaneously. Core functionality (viewing items, updating quantities, applying discounts, and completing checkout) remains fully operational.  
A future enhancement would replace the table layout with a card-based mobile design or selectively hide columns for small viewports.


---
## Evidence Index (Assessor-critical)

- Manual: broken links check → docs/testing/manual/m_links_footer_logo.png
- Manual: empty bag totals (no delivery) → docs/testing/manual/m_bag_empty_totals.png
- Manual: RBAC direct URL blocked → docs/testing/manual/m_rbac_blocked.png
- Manual: admin CRUD edit/delete works → docs/testing/manual/m_admin_crud.png
- Manual: checkout success page with order number → docs/testing/manual/m_checkout_success.png
- Manual: Stripe webhook delivered / paid flag → docs/testing/manual/m_webhook_paid.png
- Deployed: static assets loaded → docs/testing/manual/m_deploy_static_loaded.png
- Deployed: DEBUG off + 404 page → docs/testing/manual/m_deploy_404.png
- SEO: robots.txt and sitemap.xml visible → docs/testing/manual/m_seo_robots_sitemap.png


## Evidence Index (Examples)
- Python clean run: `docs/testing/py/val_py_project_clean.png`
- Python reps: `docs/testing/py/val_cake_it_easy_v2_settings.png`, `val_products_models.png`, `val_products_views.png`, `val_custom_cake_models.png`, `val_custom_cake_views.png`, `val_checkout_models.png`, `val_custom_cake_tests.png`
- HTML: `docs/testing/html/val_templates_base.png`, `val_templates_products_product_list.png`, `val_templates_products_product_detail.png`, `val_templates_checkout_checkout.png`, `val_templates_404.png`
The following pages were validated because they were specifically flagged in assessment feedback:
Home, Products list, Product detail pages.

- CSS: `docs/testing/css/val_static_css_base.png`
- JS: `docs/testing/js/val_static_js_main.png`

## Production Parity Checks (Deployed vs Local)

- Deployed site loads CSS and images correctly (no missing static assets).
- Checkout works end-to-end on deployed site.
- DEBUG is disabled in production and custom 404 page is shown.
