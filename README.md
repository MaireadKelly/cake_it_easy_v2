# README.md

## Project Overview
**Cake It Easy v2.0** is a boutique e‑commerce site for artisan cakes. Users can browse products, add to bag, pay with **Stripe PaymentIntent** (Elements + webhooks), manage their profile, and view **order history**. A **Custom Cake** flow lets customers submit bespoke requests with a “**Needed for**” date.

**Live Site:** _ADD_URL_  
**Repository:** _ADD_URL_

---

## Table of Contents
- [Key Features](#key-features)
- [Information Architecture](#information-architecture)
- [Data Model](#data-model)
- [UX & Design](#ux--design)
- [Security](#security)
- [Testing (Summary)](#testing-summary)
- [Deployment](#deployment)
- [Running Locally](#running-locally)
- [Credits](#credits)

---

## Key Features
- **Products**: List, detail, search/filters.
- **Shopping Bag**: Add/adjust/remove; delivery threshold & free‑shipping messaging.
- **Checkout**: Stripe Elements → PaymentIntent confirmation; webhook marks orders **paid** securely.
- **Profiles**: Save default delivery details; **My Orders** & **Order Detail** (owner/staff only).
- **Custom Cake**: Create / edit / delete requests; includes **Needed for (date)** with future‑date validation.
- **RBAC**: Product management links/routes restricted to **staff**.
- **Auth (allauth)**: Login, signup, reset, logout — styled card layout; cancel buttons.
- **SEO/404**: Meta description + branded 404 page (with `DEBUG=False`).
- **Social mockups**: Facebook/Instagram cover & 3–4 posts (see Marketing section/screenshots).

---

## Information Architecture
- **Public**: Home, Products (grid, detail), Custom Cakes (list/detail), About.
- **Bag/Checkout**: Bag, Checkout, Success.
- **Account**: Login/Signup/Reset/Logout, Profile, My Orders, Order Detail.
- **Admin**: Django admin for staff; staff‑only product CRUD views.

---

## Data Model
**Core models**
- **Category** (name, friendly_name)
- **Product** (category→Category, name, price, rating, image, etc.)
- **Order** (user→User optional, contact/address fields, `stripe_pid`, `paid` bool, totals)
- **OrderLineItem** (order→Order, product→Product, quantity, line total)
- **UserProfile** (user→User OneToOne, default delivery fields)
- **CustomCake** (user→User FK, name, inscription, description, flavour/filling/size, image, **needed_date**, created_on)

_Insert ERD image here_

---

## UX & Design
- **Brand**: Primary `#044762`, Accent `#a68f51`, neutral light backgrounds; Poppins font.
- **Layout**: Fixed header with safe offset; **sticky footer** (flex layout); grid navbar (left menu / center logo / right icons).
- **Accessibility**: Focus outlines on links/controls; semantic headings; visible form labels.
- **Marketing assets**: Social mockups (cover + 3 posts) in `static/mockups/` and embedded in docs.

---

## Security
- **Stripe**: Client confirms PI; server verifies webhook signature and flips `paid=True` by `stripe_pid`.
- **Permissions**: Staff‑only decorators on product CRUD; template guards hide admin controls from non‑staff; success & order detail restricted to owner/staff.
- **Config**: Secrets in env; `DEBUG=False` in production; `ALLOWED_HOSTS` set; HTTPS enforced by platform.

---

## Testing (Summary)
See **TESTING.md** for full manual matrix and evidence.
- **Automated**: Minimal unit tests
  - Bag flow (render + add/adjust/remove) — pass
  - Products RBAC (non‑staff blocked from CRUD) — pass
  - Custom Cake (create/update/delete flows) — pass
- **Manual**: End‑to‑end checkout (test card 4242…), webhook delivery, profile save, order history, auth pages, 404, and link integrity.

_Evidence screenshots folder_: `docs/screens/`  
_Key images_: Bag→Checkout→Success (order #), Stripe Events (delivered), Admin order `paid=True`, Profile save, My Orders & Order Detail, Custom Cake CRUD + date validation, Auth pages, 404 page.

---

## Deployment
**Environment variables**
```
SECRET_KEY
DEBUG=false
ALLOWED_HOSTS=<your-domain>,127.0.0.1,localhost
DATABASE_URL=<if using Postgres>
CLOUDINARY_URL=<if using Cloudinary>
STRIPE_PUBLIC_KEY
STRIPE_SECRET_KEY
STRIPE_WEBHOOK_SECRET
STRIPE_CURRENCY=eur
```

**Stripe webhook**
- Endpoint: `/checkout/wh/`
- Events: `payment_intent.succeeded` (test mode for demo)

**Static/Media**
- `collectstatic` in CI/CD or pre‑deploy. Media via Cloudinary (optional).

---

## Running Locally
```bash
git clone <repo>
cd cake_it_easy_v2
python -m venv .venv
# Windows: .venv\Scripts\activate   # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # or set env vars
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## Credits
- Base walk‑through: Code Institute **Boutique Ado**
- Icons: Font Awesome (CDN)
- Hosting: _your platform_
- Mockups: Canva

---