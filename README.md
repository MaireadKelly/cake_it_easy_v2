# Cake It Easy v2.0

<a id="top"></a>

## 📍 Table of Contents

- [Overview](#overview)
- [Live Project](#live-project)
- [Business Goals](#business-goals)
- [User Goals](#user-goals)
- [Agile Methodology](#agile-methodology)
- [Design](#design)
- [Features](#features)
- [Future Features](#future-features)
- [Testing](#testing)
- [Validation](#validation)
- [Deployment](#deployment)
- [Known Issues / Fixes](#known-issues--fixes)
- [Marketing Strategy & Evidence](#marketing-strategy--evidence)
- [Business Model & UX Rationale](#business-model--ux-rationale)
- [Credits](#credits)
- [Licence](#licence)

---

## Overview

Cake It Easy v2.0 is a full-stack e-commerce web application for ordering cakes, cupcakes, and accessories. The project is based on the Code Institute **Boutique Ado** walkthrough and extended to meet Portfolio Project 5 requirements through custom business logic, enhanced UX, and marketing features.

Key additions include:
- Cupcake **box-size pricing** (4 / 6 / 12 / 18)
- **Custom cake orders** with deposit handling
- **Newsletter signup** with discount incentive
- **One-time-use discount code logic**
- Stripe payment verification using webhooks

![Home page with navigation, hero and footer](docs/readme/01_home_nav_footer.png)

[Back to Top](#top)

---

## Live Project

- **Live Site:** https://cake-it-easy-7700e2082546.herokuapp.com/
- **Repository:** https://github.com/MaireadKelly/cake_it_easy_v2
- **Project Board:** https://github.com/users/MaireadKelly/projects/10

[Back to Top](#top)

---

## Business Goals

- Provide a professional online storefront for an artisan cake business
- Offer transparent pricing and flexible ordering options
- Encourage repeat custom through newsletter incentives
- Allow efficient admin order management

[Back to Top](#top)

---

## User Goals

- Browse products easily across devices
- Understand pricing clearly before checkout
- Order standard and custom cakes securely
- Receive confirmation and view order history

[Back to Top](#top)

---

## Agile Methodology

Development was managed using GitHub Projects with epics and user stories prioritised using MoSCoW. Each completed story is supported by commits and deployed features.

![GitHub project board](docs/readme/agile_board.png)

[Back to Top](#top)

---

## Design

- **Wireframes:** Created during planning
- **Typography:** Google Fonts (Poppins, Roboto Condensed)
- **Responsiveness:** Bootstrap 5 grid system

![ERD diagram](docs/readme/erd.png)

[Back to Top](#top)

---

## Features

### Products & Discovery

- Product listings with category filtering, sorting, and search

![Product listing page](docs/readme/02_cakes_listing.png)

### Cupcake Box Pricing

- Per-cupcake pricing dynamically updates based on selected box size

![Cupcake pricing logic](docs/readme/13_dynamic_pack_price.png)

### Shopping Bag

- Add, update, and remove items with toast feedback
- Discount codes applied dynamically

![Shopping bag totals](docs/readme/16_bag_totals.png)

### Checkout & Payments

- Secure Stripe checkout
- Orders verified via webhooks
- Discounts stored separately and applied to final total

![Checkout summary](docs/readme/19_checkout_summary.png)

### Custom Cake Orders

- Dedicated form for bespoke cake requests
- Deposit product added once per order

![Custom cake form](docs/readme/custom_cake_form.png)

### Newsletter

- Site-wide modal triggered from hero and footer
- Displays discount code on successful signup

![Newsletter success modal](docs/readme/newsletter_success.png)

[Back to Top](#top)

---

## Future Features

- Product reviews
- Loyalty rewards
- Multi-currency support

[Back to Top](#top)

---

## Testing

All testing procedures and evidence are documented in **TESTING.md**.

[Back to Top](#top)

---

## Validation

- HTML validated using W3C Validator
- CSS validated using Jigsaw
- Python checked against PEP8
- Lighthouse audits recorded

[Back to Top](#top)

---

## Deployment

### Local Setup

```bash
git clone https://github.com/MaireadKelly/cake_it_easy_v2.git
cd cake_it_easy_v2
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Destructive Operations

The following commands can permanently modify or delete data and should be used with caution:

- `python manage.py migrate`  
  Applies database migrations. While safe in normal usage, rolling back or altering migrations can result in data loss.

- `python manage.py flush`  
  **Deletes all data** from the database and resets it to an empty state.  
  This should **never** be run in production.

- `python manage.py createsuperuser`  
  Creates an admin user. Running this multiple times may result in duplicate admin accounts.

- `python manage.py collectstatic`  
  Collects static files into a single directory. Existing files may be overwritten.

- Deleting a Heroku app or Postgres add-on  
  This will permanently remove the deployed application and all associated data.

These commands were used carefully during development and deployment. No destructive commands are required to run the deployed application.

[Back to Top](#table-of-contents)


### Heroku Deployment

```yaml
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=.herokuapp.com
DATABASE_URL=provided by Heroku
STRIPE_PUBLIC_KEY=pk_live_xxx
STRIPE_SECRET_KEY=sk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
CLOUDINARY_URL=cloudinary://...
```

[Back to Top](#top)

---

## Known Issues / Fixes

- Discount recalculation fixed on bag updates
- Custom cake deposit capped at one per order

[Back to Top](#top)

---

## Marketing Strategy & Evidence

- Newsletter signup incentivised with discount
- SEO basics implemented
- Facebook mock-ups included

![Facebook mockup](docs/readme/fb_01_page_cover_about.png)

[Back to Top](#top)

---

## Business Model & UX Rationale

Revenue is generated through product sales with transparent pricing and minimal checkout friction.

[Back to Top](#top)

---

## Credits

- Code Institute Boutique Ado
- Stripe documentation
- Unsplash / Canva

[Back to Top](#top)

---

## Licence

Educational use only.

[Back to Top](#top)

