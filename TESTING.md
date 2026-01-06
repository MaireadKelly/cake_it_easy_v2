# Testing – Cake It Easy v2.0

<a id="top"></a>

## 📍 Table of Contents

- [Overview](#overview)
- [Manual Testing](#manual-testing)
- [User Stories Testing](#user-stories-testing)
- [Form Validation](#form-validation)
- [Payment Testing](#payment-testing)
- [Responsiveness](#responsiveness)
- [Accessibility](#accessibility)
- [Performance](#performance)
- [Bugs & Fixes](#bugs--fixes)

---

## Overview

This document records all testing carried out on Cake It Easy v2.0. Testing was completed on both local and deployed versions using multiple browsers and devices. Testing was carried out on both the local development server and the deployed Heroku application to ensure environment parity.

[Back to Top](#top)

---

## Manual Testing

| Feature | Action | Expected Result | Outcome |
|-------|--------|-----------------|---------|
| Navigation | Click menu links | Correct page loads | Pass |
| Footer links | Hover and click | Visual feedback and navigation | Pass |

![Navigation test](docs/testing/html/navigation.png)

[Back to Top](#top)

---

## User Stories Testing

Each user story from the GitHub Project Board was manually tested against acceptance criteria. Each user story was tested against its acceptance criteria as defined in the GitHub Project board.

![User story testing](docs/testing/flows/user_story_flow.png)

[Back to Top](#top)

---

## Form Validation

- Newsletter email validation
- Checkout required fields
- Custom cake form validation


The following validation checks were manually tested to ensure correct user feedback and data integrity:

| Form | Field | Invalid Input | Expected Behaviour | Result |
|-----|------|---------------|--------------------|--------|
| Newsletter | Email | Empty / invalid format | Error message displayed, form not submitted | Pass |
| Checkout | Country | Not selected | User prompted to select country | Pass |
| Checkout | Card details | Invalid card number | Stripe validation error shown | Pass |
| Custom Cake | Required fields | Missing required data | Inline validation message shown | Pass |

All validation feedback was clear, user-friendly, and prevented submission until corrected.


![Form validation error](docs/testing/html/form_validation.png)

[Back to Top](#top)

---

## Payment Testing

Stripe test cards were used to confirm successful and failed payments.

| Scenario | Card | Result |
|--------|------|--------|
| Successful payment | 4242 4242 4242 4242 | Pass |
| Declined payment | 4000 0000 0000 0002 | Pass |

![Stripe success](docs/testing/flows/stripe_success.png)

[Back to Top](#top)

---

## Responsiveness

Tested on:
- Chrome, Firefox, Edge
- Mobile, Tablet, Desktop

### Device & Browser Testing

The site was tested across multiple devices and browsers to ensure consistent layout, functionality, and performance.

| Device | Browser | Operating System | Result |
|------|--------|------------------|--------|
| Desktop | Chrome | Windows 11 | Pass |
| Desktop | Edge | Windows 11 | Pass |
| Desktop | Firefox | Windows 11 | Pass |
| Mobile | Chrome | Android | Pass |
| Mobile | Safari | iOS | Pass |
| Tablet | Safari | iPadOS | Pass |

All core functionality (navigation, bag, checkout, forms, and footer) behaved as expected across tested devices and browsers.


![Mobile view](docs/testing/lighthouse/mobile.png)

[Back to Top](#top)

---

## Accessibility

- Semantic HTML
- ARIA labels where required
- Colour contrast checked

### Accessibility Testing Checklist

Accessibility was manually tested to ensure the site is usable by all users and meets WCAG 2.1 AA guidelines where applicable.

| Check | Method | Result |
|-----|------|-------|
| Semantic HTML structure | Manual inspection | Pass |
| Form labels associated correctly | Manual inspection | Pass |
| Required fields clearly indicated | Manual testing | Pass |
| Keyboard navigation | Tab key testing | Pass |
| Focus indicators visible | Manual testing | Pass |
| Colour contrast | Lighthouse & manual check | Pass |
| ARIA labels (where required) | Manual inspection | Pass |
| Screen reader compatibility | Structural review | Pass |

No critical accessibility issues were identified during testing.



[Back to Top](#top)

---

## Performance

Lighthouse audits recorded for key pages.

| Page | Performance | Accessibility | SEO |
|------|-------------|---------------|-----|
| Home | 95 | 98 | 100 |

![Lighthouse audit](docs/testing/lighthouse/home.png)

[Back to Top](#top)

---

## Bugs & Fixes

## Bugs & Fixes

The following issues were identified during development and testing and were resolved prior to final submission.

| Bug | Cause | Fix | Status |
|---|---|---|---|
| Discount not updating when items added to bag | Discount calculated only on apply action | Discount recalculation added to bag context processor | Fixed |
| Discount not appearing in user order history | Discount value not stored on Order model | Discount amount saved during checkout success | Fixed |
| Duplicate Stripe PaymentIntents created | Checkout submit could be triggered twice on validation error | Submit button guarded and intent reuse enforced | Fixed |
| Custom cake deposit could be added multiple times | No quantity restriction on deposit product | Deposit product capped at quantity 1 in bag logic | Fixed |
| Toast messages causing template errors | Incorrect Django template tag usage | Template logic corrected using `{% with %}` blocks | Fixed |
| Footer social icons misaligned on mobile | Missing responsive layout rules | Mobile footer CSS rules added | Fixed |
| Newsletter discount not shown when subscribing from hero section | JS logic not shared across entry points | Shared newsletter logic implemented | Fixed |

All known issues have been resolved and retested successfully.


[Back to Top](#top)

