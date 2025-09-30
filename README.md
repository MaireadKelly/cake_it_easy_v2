# Cake It Easy v2.0

Cake It Easy v2.0 is a full‑stack e‑commerce site for ordering cakes, cupcakes, and accessories. It builds on the Code Institute **Boutique Ado** walkthrough and adds:

- **Cupcake box‑size pricing** (4/6/12/18) with transparent per‑cupcake price
- **Custom Cake Orders** (bespoke requests)
- **Discount codes** (e.g., `WELCOME10`)
- **Newsletter signup** modal with success flow
- **SEO** polish (meta, robots, sitemap, rel)

> This README aligns to the assessor feedback and PP5 criteria. See **TESTING.md** for the step‑by‑step test evidence.

---

## Live Project

- **Live Site:** [https://your-deployed-domain.com](https://cake-it-easy-7700e2082546.herokuapp.com/)
- **Repository:** [https://github.com/MaireadKelly/cake\_it\_easy\_v2](https://github.com/MaireadKelly/cake_it_easy_v2)
- **Project Board (Agile):** [https://github.com/users/MaireadKelly/projects/10](https://github.com/users/MaireadKelly/projects/10)

---

## Business Goals

- Provide a user‑friendly shop for artisan cakes and cupcakes.
- Make pricing clear: **per‑cupcake** and **per‑box**.
- Enable upsell of accessories (candles, balloons).
- Support admin efficiency with inline product options.
- Drive engagement via newsletter and social content.

## User Goals

- Browse and search products quickly.
- Understand costs before committing (per cupcake + per box).
- Add/update/remove items easily; see toasts.
- Checkout securely with Stripe.
- Save details and view previous orders.

---

## Agile Methodology

- Managed with a GitHub **Project Board** (link above).
- **Epics**: Products, Bag & Checkout, Profiles, Marketing, SEO/Accessibility, Custom Cakes.
- **MoSCoW**
  - **Must**: Product browsing, Bag, Stripe checkout, RBAC, Cupcake box pricing
  - **Should**: Newsletter modal, SEO (meta/robots/sitemap), responsive layout
  - **Could**: Custom Cake Orders
- Each User Story is tracked as a card with acceptance criteria; closed cards map to commits/deploys.

### User Stories (samples)

- As a shopper I can filter cupcakes so I see only relevant items.
- As a shopper I can choose a **box size** so I get the right quantity.
- As a shopper I can see a **per‑cupcake** price so pricing is transparent.
- As a shopper I can **apply a discount code** so I can redeem offers.
- As a staff user I can **add/edit product options** so I can manage packs.
- As a returning user I can **view past orders** so I can reorder.

> Full list and status are available on the project board.

---

## Design

- **Wireframes** (created in Balsamiq, stored in `docs/readme/`):
  ![Home](docs/readme/wireframe_home.png)
  ![Products List](docs/readme/wireframe_products_list.png)
  ![Product Detail](docs/readme/wireframe_product_detail.png)
  ![Shopping Bag](docs/readme/wireframe_bag.png)
  ![Custom Cake Form](docs/readme/wireframe_custom_cake.png)

- **Typography:** Poppins, Roboto Condensed (Google Fonts).
- **Colour Palette:** Light bakery palette with strong CTA accents (see `static/css/base.css`).
- **Responsiveness:** Bootstrap 5 grid; mobile nav + stacking forms; no horizontal scroll.

### Data Model / ERD

- See `` (exported from dbdiagram/mermaid). Core entities:
  - `Category` → `Product` → `ProductOption`
  - `Order` → `OrderLineItem`
  - `NewsletterSubscriber`
  - `CustomCake`
  - `UserProfile`

---

## Features

### Products & Discovery

- Product list, detail, search, sort, and category filters (Cakes/Accessories/Cupcakes).
- Cupcake cards display **“From €…”** based on the cheapest configured box.

### Cupcake Box‑Size Pricing

- Product detail shows **€X.XX per cupcake**.
- A **Box size** dropdown (4/6/12/18) appears above Quantity (boxes).
- Pack price auto‑calculates from per‑cupcake × quantity (or uses an override price for bundles).
- Bag line shows **(Box of N)** and **≈ € per cupcake**.

### Shopping Bag

- Add, update, remove with toasts; free‑delivery threshold message.
- **Discount codes** (see below) integrated into totals.

### Checkout (Stripe)

- Stripe PaymentIntent uses the **discounted** grand total.
- On success, order is created; bag/discount cleared; success page shown.
- Webhooks ready for robust fulfilment (test mode used).

### Profiles

- Saved default delivery details; order history.

### Admin

- Staff‑only product CRUD guarded by `@staff_member_required`.
- Inline **ProductOption** editing for cupcake packs.

### Discount Codes

- `` applies **10% off** the bag subtotal (before delivery).
- Stored in session; **Discount** line appears in Bag and Checkout.
- Stripe charges the **discounted** amount.
- Order records include `discount_code` and `discount_amount`.
- Evidence screenshots:
  - `docs/readme/discount_apply.png`
  - `docs/readme/discount_line_bag.png`
  - `docs/readme/discount_checkout.png`

### Newsletter (Marketing)

- Modal popup with email capture.
- Success view shows a welcome code (`WELCOME10`) with copy button.
- Duplicate emails are handled with a friendly message.
- Evidence screenshots:
  - `docs/readme/newsletter_form.png`
  - `docs/readme/newsletter_success.png`
  - `docs/readme/newsletter_duplicate.png`

### SEO & Accessibility

- `<title>` + `<meta name="description">` per page.
- External links use `rel="noopener noreferrer"`; decorative icons marked `aria-hidden`.
- Custom **404** page.
- **robots.txt** and **sitemap.xml** live endpoints.

---

## Future Features

- Loyalty scheme (points per order)
- Multi‑currency selector
- Product reviews & ratings

---

## Testing

All testing steps and expected outcomes are documented in [**TESTING.md**](TESTING.md). Screenshot evidence captured on the **deployed site**.

### Screenshot Index (placeholders)

## A. Navigation & Layout
![Home (nav + footer)](docs/readme/01_home_nav_footer.png)
![Cakes listing](docs/readme/02_cakes_listing.png)
![Accessories listing](docs/readme/03_accessories_listing.png)

## B. Auth
![Register form](docs/readme/04_register_form.png)
![Register feedback](docs/readme/05_register_feedback.png)
![Login success](docs/readme/06_login_success.png)
![Logout success](docs/readme/07_logout_success.png)

## C. Discovery
![Search results](docs/readme/08_search_results.png)
![Sort price low→high](docs/readme/09_sort_price_low_high.png)
![Cupcakes badge](docs/readme/10_cupcakes_badge.png)

## D. Product Detail
![Product detail top](docs/readme/11_product_detail_top.png)
![Box dropdown open](docs/readme/12_box_dropdown_open.png)
![Dynamic pack price](docs/readme/13_dynamic_pack_price.png)

## E. Bag
![Add to bag toast](docs/readme/14_add_to_bag_toast.png)
![Bag line item](docs/readme/15_bag_line.png)
![Bag totals](docs/readme/16_bag_totals.png)
![Update quantity](docs/readme/17_bag_update_qty.png)
![Remove item](docs/readme/18_bag_remove_item.png)

## F. Checkout
![Checkout summary](docs/readme/19_checkout_summary.png)
![Payment card form](docs/readme/20_payment_card_form.png)
![Payment success](docs/readme/21_payment_success.png)
![Checkout success page](docs/readme/22_checkout_success_page.png)
![Bag cleared](docs/readme/23_bag_cleared.png)

## G. Admin
![Admin product options](docs/readme/24_admin_product_options.png)
![Admin discounted bundle](docs/readme/25_admin_discounted_bundle.png)

## H. SEO / Responsive
![404 page](docs/readme/26_404_page.png)
![Meta title & description](docs/readme/27_meta_title_description.png)
![Robots & sitemap](docs/readme/28_robots_sitemap.png)
![Mobile product detail](docs/readme/29_mobile_product_detail.png)
![Mobile bag](docs/readme/30_mobile_bag.png)

## I. Marketing
![Facebook page/post mockup](docs/readme/FB_01_page_cover_about.png)
![Newsletter form](docs/readme/newsletter_form.png)
![Newsletter success](docs/readme/newsletter_success.png)
![Newsletter already subscribed](docs/readme/newsletter_duplicate.png)


---

## Validation

- **HTML:** W3C Validator – key pages validate (see TESTING.md).
- **CSS:** Jigsaw CSS validator – no blocking issues.
- **Python:** PEP8/flake8 – warnings addressed where practical.
- **Lighthouse:** Accessibility & SEO scores captured in TESTING.md.

---

## Deployment

### Local

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Production (Heroku/Render)

- `Procfile`: `web: gunicorn cake_it_easy_v2.wsgi:application`
- `requirements.txt` pinned versions
- `runtime.txt` (e.g., Python 3.11)
- Env vars: `SECRET_KEY`, `DATABASE_URL`, `STRIPE_PUBLIC_KEY`, `STRIPE_SECRET_KEY`, `STRIPE_CURRENCY`, `CLOUDINARY_URL`
- `DEBUG=False` and `ALLOWED_HOSTS` set to live domain
- Static: **Whitenoise** with `collectstatic` on build
- Media: Cloudinary (or S3) for user images

---

## Custom Cake Orders

- Customers can submit a bespoke cake request via a form capturing **flavour, filling, icing, dietary notes, message**, and optional image.
- Requests are linked to the logged‑in user and visible to staff via admin.
- Evidence screenshots: `docs/readme/custom_cake_form.png`, `docs/readme/custom_cake_list.png`.

---

## Known Issues / Fixes

- **Newsletter modal** previously showed code before submit → fixed by unifying modal IDs & JS.
- **Delivery shown on empty bag** → context processor logic fixed.
- **RBAC** for product CRUD → guarded with `@staff_member_required` and template gating.

---

## Marketing & SEO Evidence

- **Newsletter:** form/success/duplicate (see screenshots under I.)
- **Facebook:** branded post mockup showing box‑size pricing (`FB_01_page_cover_about.png`).
- **SEO:** meta description, `robots.txt`, `sitemap.xml`, custom 404.

---

## Business Model & UX Rationale

- **Revenue:** core product sales (cakes/cupcakes), accessories upsell, occasional bundles.
- **Differentiator:** transparent per‑cupcake price + selectable box sizes.
- **UX:** simple filters, big images, toasts, free‑delivery banner; checkout friction minimized.
- **Admin efficiency:** inline product options make updates fast.

---

## Credits

- Code Institute **Boutique Ado** walkthrough.
- Stripe Docs.
- Canva/Unsplash for imagery (placeholders).

## Licence

Educational use for Code Institute Portfolio Project 5.

