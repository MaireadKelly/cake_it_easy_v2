# Cake It Easy v2.0

Securely order cakes and accessories with a simple checkout.

Live site: https://cake-it-easy-7700e2082546.herokuapp.com/  
Repository: https://github.com/MaireadKelly/cake-it-easy-v2

---

## Purpose & Audience
Cake It Easy v2.0 is an e-commerce application allowing customers to browse cakes, order standard products, or request custom cakes.  
The purpose is to provide a smooth online shopping experience with secure payments and clear confirmation.  
Target users are customers seeking cakes and accessories; the site owner manages products and receives orders.

---

## Features
- Browse products with categories and search.
- Product detail pages with “Buy Now” → Checkout.
- Stripe checkout using **PaymentIntent**.
- Order saved in database with line items.
- Success page with order reference + confirmation email (console).
- Newsletter signup form.
- Admin-only product management (RBAC).
- SEO features: meta description, robots.txt, sitemap.xml.
- 404 page for invalid routes.

---

## Data Model
Entities:
- **Category** → **Product**
- **Order** → **OrderLineItem**
- **CustomCake** (user requests)

![ERD](docs/erd/cake_it_easy_erd.png)

---

## Payments
- Integrated with Stripe PaymentIntent.
- Test with card number `4242 4242 4242 4242`.
- Orders and line items stored in the database.
- Confirmation email shown in dev console.

---

## Security & Role-Based Access
- Only staff users can add/edit/delete products.
- Environment variables hide secret keys (`SECRET_KEY`, Stripe keys).
- `DEBUG=False` in production.

---

## SEO
- Meta description in base template.
- robots.txt and sitemap.xml routes.
- Custom 404 error page.

---

## Marketing
- Newsletter signup form stores subscriber emails in DB.
- Facebook mockup page screenshot included.

---

## Agile / Project Management
This project was managed using **GitHub Projects** with user stories tracked as issues and grouped into milestones.

### Agile Process
- User stories were created for each functional requirement (e.g., *Checkout and Purchase*, *Custom 404 Page*, *Newsletter Signup*).
- Issues were labelled by priority (`Must`, `Should`, `Could`) to ensure focus on PASS criteria.
- Issues were organised into a Kanban board with **Todo / In Progress / Done** columns.
- Milestones grouped issues by learning outcomes (e.g., *Digital Marketing & SEO*, *Testing & Security*) and by deliverables (new **PASS Essentials** milestone).
- The board was reviewed daily, and priorities adjusted to keep aligned with assessment rubric.

### Agile Artefacts
- **Board Screenshot**: shows Todo/In Progress/Done workflow.
- **Milestones Screenshot**: shows grouping and % complete.
- **Closed Issues Screenshot**: shows completed admin CRUD stories.
- **PASS Essentials Milestone**: created to track only must-have issues for resubmission.

### Agile Reflection
- Prioritisation using **MoSCoW** (Must/Should/Could) ensured focus on PASS blockers.
- Iterative development allowed rapid progress on core features before enhancements.
- Evidence pack shows the progression of issues from creation to closure.

Screenshots:  
- `docs/screenshots/agile/board_kanban.png`  
- `docs/screenshots/agile/milestones.png`  
- `docs/screenshots/agile/closed_issues.png`

---

## Testing
See [TESTING.md](TESTING.md) for full test plan and results.

---

## Deployment
- Hosted on **Heroku**: https://cake-it-easy-7700e2082546.herokuapp.com/
- Config Vars set in Heroku Dashboard:
  - `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`
  - `STRIPE_PUBLIC_KEY`, `STRIPE_SECRET_KEY`
  - `DEFAULT_FROM_EMAIL`
- Static files served with WhiteNoise.
- Media via Cloudinary.
- Deploy steps:
  ```bash
  git push heroku main
  heroku run python manage.py migrate
  heroku run python manage.py collectstatic --noinput
