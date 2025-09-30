# Testing Documentation

## Automated Tests

Unit tests run across `bag`, `products`, and `custom_cake` apps.

_Evidence_: ![pytest run showing green tests](docs/testing/val_pytest_run.png)

---

## Manual Test Matrix

| Area       | Feature                    | Action                          | Expected Result                                    | Evidence |
|------------|----------------------------|---------------------------------|----------------------------------------------------|----------|
| Products   | List view                  | Visit `/products/`              | Product grid displayed with categories             | docs/readme/02_cakes_listing.png |
| Products   | Detail view                 | Click a product                 | Product detail page shows image, desc, options     | docs/readme/11_product_detail_top.png |
| Discovery  | Search                      | Enter keyword                   | Search results filtered                           | docs/readme/08_search_results.png |
| Discovery  | Sort by price               | Select low-high                 | Products reordered by price                       | docs/readme/09_sort_price_low_high.png |
| Bag        | Add to bag                  | Select product + add            | Toast shows added; bag updated                    | docs/readme/14_add_to_bag_toast.png |
| Bag        | Update qty                  | Change quantity in bag          | Bag line updates subtotal                         | docs/readme/17_bag_update_qty.png |
| Bag        | Remove item                 | Click remove icon               | Bag line removed, toast confirms                  | docs/readme/18_bag_remove_item.png |
| Bag        | Apply discount code         | Enter WELCOME10 and update      | Bag shows discount line and reduced total         | docs/readme/discount_apply.png |
| Checkout   | Discount applied            | Proceed with WELCOME10 applied  | Checkout summary shows discount + Stripe correct  | docs/readme/discount_checkout.png |
| Checkout   | Payment                     | Enter test card                 | PaymentIntent created, success page shown         | docs/readme/21_payment_success.png |
| Checkout   | Success page                | After payment                   | Order confirmation with order number              | docs/readme/22_checkout_success_page.png |
| Profiles   | Register                    | Submit new account              | Success feedback, user logged in                  | docs/readme/05_register_feedback.png |
| Profiles   | Login/Logout                | Login/logout                    | Navbar updates appropriately                      | docs/readme/06_login_success.png / docs/readme/07_logout_success.png |
| Profiles   | Order history               | Log in, view profile            | Past orders listed                                | docs/readme/22_checkout_success_page.png |
| Admin      | Product CRUD                | Staff edits product             | Changes saved; guarded by staff auth              | docs/readme/24_admin_product_options.png |
| Marketing  | Newsletter subscribe        | Open modal, enter valid email   | Success view shows WELCOME10 code                 | docs/readme/newsletter_success.png |
| Marketing  | Duplicate email             | Submit existing email           | Error message displayed                           | docs/readme/newsletter_duplicate.png |
| SEO        | Meta tags                   | Inspect page source             | Title + meta description present                  | docs/readme/27_meta_title_description.png |
| SEO        | robots.txt                  | Visit /robots.txt               | Shows allow all + sitemap link                    | docs/readme/28_robots_sitemap.png |
| SEO        | sitemap.xml                 | Visit /sitemap.xml              | Sitemap XML with site URLs                        | docs/readme/28_robots_sitemap.png |

---

## Validation

- **HTML** – W3C Validator, no critical errors.  
  _Evidence_: ![HTML validation](docs/testing/val_html_index.png)

- **CSS** – Jigsaw Validator, clean run.  
  _Evidence_: ![CSS validation](docs/testing/val_css.png)

- **Python** – Flake8/pycodestyle, clean.  
  _Evidence_: ![pycodestyle clean run](docs/testing/val_py_console.png)

- **Lighthouse** – High scores for Accessibility & SEO.  
  _Evidence_: ![Lighthouse home mobile](docs/testing/lighthouse_home_mobile.png)

---

## Browser & Device Coverage

Tested on:
- Chrome (desktop, mobile emulator)
- Safari (iPhone)
- Firefox (desktop)

_Evidence_: ![Am I Responsive](docs/readme/am_i_responsive.png)

---

## Known Issues / Out of Scope

- **Future features not implemented**: loyalty scheme, reviews/ratings.  
- **Newsletter**: modal works, but limited to email capture + static code.  
- **Marketing**: only Facebook mockup provided, no full campaign pages.  
- No multi-currency support (future).

