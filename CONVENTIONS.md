## 1) `CONVENTIONS.md`

```markdown
# Cake It Easy v2 — Repository Conventions (Authoritative)

> This project follows strict, PASS‑oriented conventions. All code reviews and patches MUST honor these rules.

## Pass‑first, with safe nice‑to‑haves
- Default stance: deliver a PASS with the **smallest, safest** changes.
- Nice‑to‑haves are allowed **only when** they are trivial (≈<5 minutes), low risk, reversible, and don’t add new libraries or migrations.

## Naming & Data Model (canonical)
- **Timestamp fields:** `created_on` (🔒 DO NOT rename to `date`, `created`, `created_at`, etc.).
- **Orders:** `Order(order_total, stripe_pid, original_bag, paid, created_on)`.
- **Order lines:** `OrderLineItem(order, product, quantity, lineitem_total)` — `lineitem_total` computed in `save()`.
- **Profiles:** `UserProfile` (O2O `User`) with **default_*** fields:
  - `default_phone_number`, `default_country`, `default_postcode`, `default_town_or_city`, `default_street_address1`, `default_street_address2`.
- **Bag session structure:** `request.session['bag'] = { "<product_id_str>": <int_quantity>, ... }`.

## Templates & Frontend
- Each app keeps its own templates directory: `app/templates/app/...`.
- Always `{% load static %}` at the top when using static files.
- Use `{% url 'route_name' %}` (no hardcoded URLs).
- Preserve existing HTML **IDs/classes**. Do not rename unless fixing a bug.

## RBAC (staff‑only)
- Admin CRUD guarded by:
  - Templates: `{% if request.user.is_staff %}…{% endif %}`
  - Views: `@staff_member_required` when relevant.

## Stripe/Checkout Reliability
- PaymentIntent flow with graceful fallback: if keys missing/invalid → **demo mode** (no crash).
- Webhook endpoint `/checkout/wh/` marks `Order.paid = True` on `payment_intent.succeeded`.

## Admin display
- Use `created_on` in `list_display` and `date_hierarchy`.

## Commit style
- Conventional commits, small diffs. Examples:
  - `feat(checkout): save profile defaults on order`
  - `fix(admin): use created_on in list_display`
  - `chore(heroku): switch to .python-version (3.12)`

## Reviewer Workflow (required before proposing patches)
1) **Scan** the repo to infer conventions and verify they match this file.
2) **Echo back** a brief Conventions Map (what → where → examples/paths).
3) Propose **minimal** patches that align with these rules (see patch format below).

## Required pre‑patch scan (practical checks)
- [ ] Grep for timestamp names: `\bdate\b|\bcreated(?:_at)?\b|created_on` and list mismatches.
- [ ] Confirm `UserProfile` uses `default_*` fields.
- [ ] Confirm bag session structure matches `{str(id): int(qty)}`.
- [ ] Confirm templates use `{% url %}` and `{% load static %}`.
- [ ] Confirm product CRUD is staff‑guarded in templates and views.

## Patch format (to keep diffs obvious)
```

# File: <path>

## REPLACE | ADD | INSERT AFTER "<anchor>"

<full code block>
```

```
# File: checkout/views.py
## INSERT AFTER "return render(request, 'checkout/checkout.html', {"
    'stripe_public_key': getattr(settings, "STRIPE_PUBLIC_KEY", ""),
```

```
# File: profiles/signals.py
## REPLACE
<full file content>
```

```
```

---

