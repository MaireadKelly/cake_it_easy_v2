## Project: Cake It Easy

A Django-based e‑commerce site for ordering custom occasion cakes, inspired by the Code Institute **Boutique Ado** walkthrough and adapted for my use case. Features include product browsing with categories/filters, a custom cake order flow, basket & checkout with Stripe Payment Intents + webhooks, and user profiles for order history.

**Live Site:** https://DEPLOYED_APP_URL  
**Repository:** https://github.com/MaireadKelly/cake_it_easy_v2

---

## Table of Contents
- [UX](#ux)
  - [User Goals](#user-goals)
  - [Business Goals](#business-goals)
  - [Target Audience](#target-audience)
  - [User Stories](#user-stories)
  - [Wireframes](#wireframes)
  - [Design](#design)
- [Agile](#agile)
- [Features](#features)
- [Information Architecture](#information-architecture)
- [Data Model](#data-model)
- [Security](#security)
- [Technologies](#technologies)
- [Testing](#testing)
- [Deployment](#deployment)
- [Credits](#credits)
- [License](#license)

---

## UX

### User Goals
- Quickly find and purchase cakes and accessories.
- Configure a **Custom Cake** (flavour, filling, size, inscription, date needed).
- Pay securely and receive email confirmation.
- Review past orders via profile.

### Business Goals
- Accept online payments and manage orders.
- Promote seasonal products and upsell accessories.
- Collect non-sensitive analytics (page visits, conversion).

### Target Audience
- Individuals/companies ordering celebration cakes in Ireland.

### User Stories
(Tracked as GitHub Issues & Project board.)  
See: `docs/readme/user-stories-overview.png` (board snapshot).

### Wireframes
Exported from Visily.  
Screenshots placed in `docs/readme/`:
- `wireframe-home-desktop.png`
- `wireframe-product-list-desktop.png`
- `wireframe-product-detail-desktop.png`
- `wireframe-basket-desktop.png`
- `wireframe-checkout-desktop.png`
- `wireframe-profile-desktop.png`
- `wireframe-custom-cake-desktop.png`
- `wireframe-mobile-composite.png`

### Design
- **Colour palette:** Dark Blue `#044762`, Gold `#a68f51`, Dark Grey `#555253`, Light BG.
- **Typography:** Bootstrap base + (TODO: add chosen Google Fonts).
- **Imagery:** Product photos via Cloudinary; credits in [Credits](#credits).
- **Branding:** Simple wordmark logo; favicon included.

Screenshots (put into `docs/readme/`):
- `ui-home-hero.png`
- `ui-header-nav.png`
- `ui-product-cards.png`
- `ui-custom-cake-form.png`
- `ui-checkout-elements.png`

---

## Agile
- **Method:** MoSCoW + Kanban board on GitHub Projects.  
- Epics & stories link: https://github.com/MaireadKelly/cake_it_easy_v2/projects (or specific board URL).
- Evidence screenshots (in `docs/readme/`):
  - `agile-board-sprint-snapshot.png`
  - `agile-issue-example.png`
  - `agile-issue-closure.png`

---

## Features

### Implemented
- Product catalogue with categories, sorting, search, and filtering.
- Product detail pages with add‑to‑basket.
- Basket (bag) with update/remove and toast messages.
- Checkout with Stripe Payment Intents, webhooks, and email confirmation.
- Custom Cake builder form with validation and date‑needed.
- User Accounts: register/login/logout via Allauth.
- Profiles with default delivery info and order history.
- Admin management (create/update products & categories).
- Responsive Bootstrap layout; accessible forms and buttons.

### Future Enhancements
- Guest checkout.
- Accessories (candles, toppers) bundle offers.
- Product reviews/ratings.

Screenshots (place in `docs/readme/`):
- `feature-search-results.png`
- `feature-sort-filter.png`
- `feature-basket-toast.png`
- `feature-profile-orders.png`
- `feature-webhook-log.png`

---

## Information Architecture
- **Apps:** `home`, `products`, `basket`, `checkout`, `profiles`, `custom_cake`.
- **Static/Media:** `static/` for CSS/JS; images via Cloudinary; `media/` for dev.
- **Templates:** Base template + app‑specific templates.

Repository structure snapshot (put image in `docs/readme/` as `repo-tree.png`).

---

## Data Model

High-level ERD (place in `docs/readme/erd.png`).

**Core models:**
- `Category(id, name, friendly_name, parent?)`
- `Product(id, category, name, description, price, image, ... )`
- `Order(id, user, contact fields, totals, stripe_pid, original_bag, date)`
- `OrderLineItem(id, order, product, quantity, lineitem_total, options...)`
- `UserProfile(user OneToOne, default_* fields)`
- `CustomCakeOrder(id, user?, flavour, filling, size, colour, inscription, date_needed, ... )`

---

## Security
- Environment variables via `.env` (never committed).
- DEBUG = False in production.
- CSRF enabled; secure cookies on Heroku; SSL via `SECURE_SSL_REDIRECT`.
- Stripe keys and webhook secret stored in config vars.
- Allowed Hosts set to deployed hostname.

---

## Technologies
- **Backend:** Python, Django, Gunicorn.
- **Frontend:** HTML, CSS (Bootstrap 5), JavaScript.
- **Payments:** Stripe (Elements, Payment Intents, Webhooks).
- **DB:** Postgres (Neon/Heroku Postgres) in production; SQLite for local dev.
- **Media:** Cloudinary.
- **Deployment:** Heroku.
- **Dev:** Git/GitHub, VS Code, djlint/djhtml, PEP8CI linter.

---

## Testing
See full write‑up in [`TESTING.md`](./TESTING.md).  
Quick links to reports in `docs/testing/`.

---

## Deployment

### Local Development
1. Clone repo: `git clone https://github.com/MaireadKelly/cake_it_easy_v2`
2. Create & activate venv, install deps: `pip install -r requirements.txt`
3. Create `.env` (example below) and set **DJANGO_SETTINGS_MODULE** if needed.
4. Run migrations & load fixtures (optional):
   ```bash
   python manage.py migrate
   python manage.py loaddata categories.json products.json  # if present
   python manage.py createsuperuser
   python manage.py runserver
   ```

**`.env` template:**
```bash
SECRET_KEY=YOUR_SECRET_KEY
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
CLOUDINARY_URL=cloudinary://...  # dev only
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WH_SECRET=whsec_...
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### Heroku Deployment
1. Create Heroku app and Postgres; set **Config Vars** from `.env`.
2. Set `DISABLE_COLLECTSTATIC=1` during initial deploy if needed, then remove.
3. Add buildpacks (Python). Push to Heroku.
4. Run `python manage.py migrate` and create a superuser.
5. Ensure `ALLOWED_HOSTS` includes app domain and `DEBUG=False`.
6. Set up Stripe webhook endpoint → copy **Signing Secret** to `STRIPE_WH_SECRET`.

Screenshots:
- `deploy-heroku-config-vars.png`
- `deploy-stripe-webhook-endpoint.png`
- `deploy-dynos.png`

---

## Credits
- **Walkthrough Base:** Code Institute – Boutique Ado.
- **Inspiration:** https://ohehirs.ie/ (structure & UX).
- **Images:** Product images via Cloudinary (see `docs/readme/image-credits.md`).
- **Libraries:** See [Technologies](#technologies).
- **Acknowledgements:** Built with guidance from tutors and an AI assistant for boilerplate.

---

## License
This project is for educational purposes.
```
