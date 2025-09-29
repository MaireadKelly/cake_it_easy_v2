# Cake It Easy v2.0

Cake It Easy v2.0 is a full-stack e-commerce application for ordering cakes, cupcakes, and accessories. It builds on the Code Institute Boutique Ado walkthrough, extended with **custom cake ordering** and enhanced **cupcake box-size pricing**.

---

## Live Project
- **Live Site:** [https://your-deployed-domain.com](https://your-deployed-domain.com)
- **Repository:** [https://github.com/MaireadKelly/cake_it_easy_v2](https://github.com/MaireadKelly/cake_it_easy_v2)
- **Project Board (Agile):** [Cake It Easy v2.0 Project Board](https://github.com/users/MaireadKelly/projects/10)

---

## Business Goals
- Provide a user-friendly platform to order cakes and cupcakes online.
- Highlight transparent cupcake **per-unit pricing** and **box-size options** (4, 6, 12, 18).
- Enable customers to design custom cakes.
- Support business operations with easy product/option management.
- Drive engagement with marketing features (newsletter & social media).

## User Goals
- Browse and search cakes, cupcakes, and accessories.
- Understand pricing clearly (per cupcake and per box).
- Add products to a shopping bag with live feedback.
- Checkout securely with Stripe.
- Save delivery details and view past orders.
- Access special offers and promotional content.

---

## Agile Methodology
- Managed via [GitHub Project Board](https://github.com/users/MaireadKelly/projects/10).
- Issues mapped to **Epics**:
  - **Products:** List, filter, detail views.
  - **Bag & Checkout:** Add/update/remove, Stripe integration.
  - **Profiles:** Order history, saved address.
  - **Marketing:** Newsletter, Facebook mockup.
  - **SEO & Accessibility:** Meta, robots, sitemap, ARIA.
- **MoSCoW Prioritisation:**
  - **Must-have:** Stripe checkout, bag, cupcake packs, CRUD with RBAC.
  - **Should-have:** Newsletter modal, SEO fixes, responsive design.
  - **Could-have:** Custom cake ordering.
- Completed stories tagged and linked in commits. Backlog items noted in board.

---

## User Stories
Examples:
- As a customer I can register/login so that I can place and track orders.
- As a customer I can view per-cupcake and per-box prices so that I understand costs.
- As a customer I can update or remove items in my bag so that I can control my order.
- As a staff member I can add/edit products and options so that I can manage stock.
- As a business owner I can promote offers via newsletter/social so that I can increase sales.

---

## Design
- **Wireframes:** `/docs/wireframes/` (Home, Products, Product Detail, Bag, Profile).
- **Colour Palette:** Light pastels and accent colours (CSS variables in `base.css`).
- **Fonts:** Poppins, Roboto Condensed (Google Fonts).
- **Database Schema:**
  - Category → Product → ProductOption.
  - Order → OrderLineItem.
  - NewsletterSubscriber.

---

## Features
- **Navigation:** Responsive nav, free delivery banner, toasts for feedback.
- **Products:** Cakes, Cupcakes, Accessories (Balloons, Candles).
- **Cupcake Packs:** Box size dropdown (4, 6, 12, 18) with per-unit and per-box pricing.
- **Bag:** Dynamic update, per-cupcake breakdown, free-delivery threshold.
- **Checkout:** Stripe PaymentIntent, webhook handlers, order summary.
- **Profiles:** Saved address, order history.
- **Admin:** Staff-only product CRUD, inline product options.
- **Marketing:**
  - Newsletter modal with discount code & success panel.
  - Facebook mockup post highlighting box-size pricing.
- **SEO/Accessibility:**
  - Custom 404 page.
  - `<meta name="description">` tags.
  - `robots.txt` and `sitemap.xml`.
  - `rel="noopener noreferrer"` on external links.
  - ARIA labels on nav and footer links.

---
### Discount Codes

A discount code system has been implemented to support simple promotions.

- **WELCOME10** → Applies a **10% discount** to the subtotal (before delivery).  
- Discount is stored in the user’s session and persists while browsing.  
- A **Discount line** appears in the Bag and Checkout summaries, clearly showing the code and amount.  
- Discounts are passed through to Stripe so the customer is only charged the **discounted grand total**.  
- Orders store both the `discount_code` and `discount_amount` for reporting/admin review.  

**Usage:**
1. Add items to the Bag.  
2. Enter `WELCOME10` in the discount code field.  
3. Press **Apply** → success toast appears, Bag updates totals.  
4. Proceed to Checkout → summary shows discounted grand total.  
5. On payment success, the applied discount is cleared from the session.  

## Future Features
- Loyalty scheme (points per purchase).
- Multi-currency support.
- Admin dashboard with sales analytics.

---

## Testing
Full testing documentation is in [TESTING.md](TESTING.md).

- **End-to-End Test Script:** Covers navigation, auth, bag, checkout, admin, SEO, newsletter.
- **Screenshots:** Saved under `/docs/screens/` and linked below.

---

## End-to-End Test Evidence
### A. Navigation & Layout
- ![Home](docs/screens/01_home_nav_footer.png)
- ![Cakes](docs/screens/02_cakes_listing.png)
- ![Accessories](docs/screens/03_accessories_listing.png)

### B. Authentication
- ![Register Form](docs/screens/04_register_form.png)
- ![Register Feedback](docs/screens/05_register_feedback.png)
- ![Login Success](docs/screens/06_login_success.png)
- ![Logout Success](docs/screens/07_logout_success.png)

### C. Product Discovery
- ![Search Results](docs/screens/08_search_results.png)
- ![Sort Price](docs/screens/09_sort_price_low_high.png)
- ![Cupcakes Badge](docs/screens/10_cupcakes_badge.png)

### D. Product Detail
- ![Detail Top](docs/screens/11_product_detail_top.png)
- ![Box Dropdown](docs/screens/12_box_dropdown_open.png)
- ![Dynamic Pack Price](docs/screens/13_dynamic_pack_price.png)

### E. Bag
- ![Add Toast](docs/screens/14_add_to_bag_toast.png)
- ![Bag Line](docs/screens/15_bag_line.png)
- ![Bag Totals](docs/screens/16_bag_totals.png)
- ![Update Qty](docs/screens/17_bag_update_qty.png)
- ![Remove Item](docs/screens/18_bag_remove_item.png)

### F. Checkout
- ![Checkout Summary](docs/screens/19_checkout_summary.png)
- ![Payment Card](docs/screens/20_payment_card_form.png)
- ![Payment Success](docs/screens/21_payment_success.png)
- ![Checkout Success](docs/screens/22_checkout_success_page.png)
- ![Bag Cleared](docs/screens/23_bag_cleared.png)

### G. Admin
- ![Admin Options](docs/screens/24_admin_product_options.png)
- ![Admin Discount](docs/screens/25_admin_discounted_bundle.png)

### H. SEO, Errors, Responsive
- ![404](docs/screens/26_404_page.png)
- ![Meta](docs/screens/27_meta_title_description.png)
- ![Robots & Sitemap](docs/screens/28_robots_sitemap.png)
- ![Mobile Detail](docs/screens/29_mobile_product_detail.png)
- ![Mobile Bag](docs/screens/30_mobile_bag.png)

### I. Newsletter & Marketing
- ![Newsletter Form](docs/screens/newsletter_form.png)
- ![Newsletter Success](docs/screens/newsletter_success.png)
- ![Newsletter Duplicate](docs/screens/newsletter_duplicate.png)
- ![Facebook Post Mockup](docs/screens/FB_01_page_cover_about.png)

---

## Bugs & Fixes
- **Newsletter modal** initially showed success before submit; fixed by unifying modal IDs and JS.
- **Bag delivery** showed €15 on empty cart; fixed in context processor.
- **RBAC:** Non-staff could access product edit/delete; fixed with `@staff_member_required` and template gating.

---

## Validation
- **HTML:** W3C validator.
- **CSS:** Jigsaw CSS validator.
- **Python:** PEP8 (flake8).
- **Lighthouse:** Performance, accessibility, SEO checks.
- **WAVE:** Accessibility checks.

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

### Heroku/Render
- `Procfile`: `web: gunicorn cake_it_easy_v2.wsgi:application`
- `requirements.txt` pinned
- `runtime.txt` with Python 3.11
- Environment vars: `SECRET_KEY`, `DATABASE_URL`, `STRIPE_PUBLIC_KEY`, `STRIPE_SECRET_KEY`, `CLOUDINARY_URL`
- `DEBUG=False`, `ALLOWED_HOSTS` set
- `python manage.py collectstatic --noinput`

---

## Marketing & SEO Evidence
- **Newsletter Modal:**
  - ![Newsletter Form](docs/screens/newsletter_form.png)
  - ![Newsletter Success](docs/screens/newsletter_success.png)
  - ![Newsletter Already Subscribed](docs/screens/newsletter_duplicate.png)
- **Social Media:**
  - ![Facebook Page Post](docs/screens/FB_01_page_cover_about.png)
- **SEO:**
  - ![Meta Description](docs/screens/27_meta_title_description.png)
  - ![Robots & Sitemap](docs/screens/28_robots_sitemap.png)
  - ![404 Page](docs/screens/26_404_page.png)

---

## Business Model & UX Rationale
- **Revenue:** Cake and cupcake sales; upsell accessories; optional bundle discounts.
- **Differentiator:** Transparent per-cupcake pricing and box-size packs.
- **UX:** Responsive design, clear categories, free delivery banner, toast notifications.
- **Marketing:** Newsletter signups with discount code; Facebook presence.
- **Admin:** Inline product option management saves staff time.

---

## Credits
- Code Institute Boutique Ado walkthrough.
- Stripe API docs.
- Canva mockups for social posts.
- Unsplash placeholder images.

---

## Licence
For educational use only (Code Institute Portfolio Project 5).

