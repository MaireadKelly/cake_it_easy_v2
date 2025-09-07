
---

# 📄 TESTING.md (minimal PASS version)

```markdown
# TESTING.md — Cake It Easy v2.0

This file records manual and validation testing.

---

## 1. Manual Test Matrix

| Scenario | Steps | Expected | Actual | Pass |
|----------|-------|----------|--------|------|
| Browse Products | Visit `/products/` | Product list displays |  |  |
| Product Detail | Click on product | Detail page loads |  |  |
| Add to Bag | Click “Buy Now” | Item added to bag |  |  |
| Checkout Success | Bag → Checkout → Stripe test card | Success page with order # and email |  |  |
| Empty Bag Guard | Visit `/checkout/` directly | Redirect to products with message |  |  |
| Admin Order | Admin → Orders | Order + line items visible |  |  |
| RBAC Restriction | Non-staff access `/products/edit/<id>/` | Redirect/403 |  |  |
| Navigation | Navbar links + logo | Each works |  |  |
| Footer Links | Footer links clicked | No broken links |  |  |
| 404 Page | Visit `/bad-url/` | Custom 404 page |  |  |
| Robots.txt | Visit `/robots.txt` | Shows sitemap line |  |  |
| Sitemap.xml | Visit `/sitemap.xml` | Shows XML urls |  |  |
| Newsletter Signup | Submit email | Success message + DB entry |  |  |

---

## 2. Validation Tests

| Page | Validator | Result |
|------|-----------|--------|
| Home | W3C HTML |  |
| Products | W3C HTML |  |
| Checkout | W3C HTML |  |

---

## 3. Browser & Device Testing
- Chrome, Firefox, Edge  
- Mobile view (DevTools simulation: iPhone/Android)  
- Responsive layout confirmed.

---

## 4. Deployment Verification
- Live Heroku site loads CSS/JS with `DEBUG=False`.  
- Screenshot of Heroku Config Vars attached.  

---

## 5. Known Issues
- (Add if any remain, e.g. styling quirks).  

---

## 6. Evidence
Screenshots in `/docs/screenshots/`:
- Checkout flow
- Admin Orders
- Console email
- 404 page
- SEO routes
- Newsletter
- Validator outputs
- Agile board
