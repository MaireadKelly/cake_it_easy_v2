# PP5 — E‑commerce Applications: Assessment Criteria (Markdown)

> Converted to Markdown for easy printing and check‑off. Use this as your PASS/MERIT/DISTINCTION checklist.

---

## Portfolio Project 5: Overview

Build a Full‑Stack, cloud‑hosted Django application with a centrally‑owned dataset, authentication/authorisation, and an online payment system (e.g., Stripe). Include a dummy social media product page (or provided mockups/screenshots) in your README.

**Main technologies:** HTML, CSS, JavaScript, Python + Django, relational DB (MySQL/Postgres recommended), Stripe.

---

## Learning Outcomes (LO)

- **LO1** — Integrate an e‑commerce payment system and product structure in a cloud‑hosted Full‑Stack web application
- **LO2** — Employ advanced UX to build a commercial‑grade Full‑Stack web application
- **LO3** — Employ SEO techniques to improve audience reach
- **LO4** — Create a secure Full‑Stack web application with Authentication and role‑based Authorisation
- **LO5** — Employ marketing techniques to create brand reach
- **LO6** — Understand the fundamentals of e‑commerce applications

---

## PASS Criteria (all must be achieved)

### LO1 — E‑commerce integration & product structure

1.1 Implement at least one Django app with e‑commerce functionality using an online payment system (e.g., Stripe). This may be cart checkout, subscriptions, single payments/donations.

1.2 Implement a feedback system that reports successful and unsuccessful purchases to the user with a helpful message.

1.3 Build a Full‑Stack web app using Django with a relational database, interactive front‑end, and **multiple apps** (each reusable component is its own app).

1.4 Implement at least **one form** with validation that allows users to create/edit models in the backend.

1.5 Django file structure is **consistent and logical**, following Django conventions.

1.6 Code demonstrates **clean code** characteristics.

1.7 Application URLs are defined consistently.

1.8 Include a **main navigation menu** and structured layout.

1.9 Demonstrate proficiency in Python with sufficient **custom logic**.

1.10 Include functions with compound statements (ifs/loops, etc.).

1.11 Design a relational **database schema** with clear relationships between entities.

1.12 Create at least **three original custom Django models**.

1.13 Implement full **CRUD** (create, read, update, delete) functionality.

1.14 Deploy the final version to hosting and confirm production matches development.

1.15 Final deployed code is free of commented‑out code and has **no broken internal links**.

1.16 Keep the deployed version **secure**: no secrets in git; all keys in env vars; **DEBUG=False**.

1.17 Use git effectively for the entire application; reflect development via regular commits and README documentation.

1.18 Provide a **well‑structured README.md** with consistent Markdown.

1.19 Document complete **deployment** (incl. database) and **testing** procedures in the README; explain the application’s purpose and user value.

---

### LO2 — UX Design (advanced)

2.1 Design a front‑end that meets **accessibility** guidelines, aligns with UX principles, meets the project purpose, and provides coherent user interactions.

2.2 Document & implement **User Stories** in an Agile tool and map them to project goals.

2.3 Design & implement **manual or automated test procedures** to assess functionality, usability, responsiveness, and data management across the app.

2.4 Present a clear rationale in the README: well‑defined purpose addressing the needs of a target audience.

2.5 Document the UX design process (wireframes/mockups/diagrams) and show it was followed through to implementation.

2.6 Use an **Agile tool** to plan and implement primary functionality.

2.7 Document and implement all User Stories and map them to the project within the Agile tool.

---

### LO3 — SEO

3.1 Ensure **all pages** are reachable by a link from another findable page.

3.2 Include **Meta Description** tags.

3.3 Include a **site title** on the parent template.

3.4 Correctly use link `rel` values: `nofollow` for paid/distrusted links; `sponsored` for sponsored/compensated links.

3.5 Include a **sitemap** for crawling.

3.6 Include **robots.txt** to control crawling.

3.7 Provide a **404 response page** with appropriate redirect/UX for non‑existent content.

3.8 Ensure all text content supports the application’s purpose (no Lorem Ipsum).

---

### LO4 — Security, Auth, RBAC

4.1 Implement **authentication** (register/log in) with a clear reason for users to do so.

4.2 Login/registration pages are only available to **anonymous** users.

4.3 Prevent non‑admin users from accessing the datastore directly without going through app code.

4.4 Apply **role‑based** login/registration functionality.

4.5 Reflect current login state to the user.

4.6 Users must not access restricted content/functionality before role‑based login.

---

### LO5 — Marketing

5.1 Create a **Facebook Business Page** (or include approved mockups/screenshots in README if not creating a real page).

5.2 Add a **newsletter signup form** to your application.

---

### LO6 — E‑commerce fundamentals

6.1 Document the **business model** underlying your application.

> **Important:** All PASS criteria must be achieved for a Pass to be awarded.

---

## MERIT Performance (all MERIT criteria must be achieved)

High‑level summary: A fully functioning, well‑documented, relational, e‑commerce Django app for a real audience. Clean templates, no logic errors, payments work; purpose is clear; feedback and progress indicators present; responsive and accessible; data model documented; configuration organised; deployed to Heroku (or equivalent); SEO and marketing evident; version control used effectively.

**Criteria (extract):**

- **1.1** Build a real‑world full‑stack MVC e‑commerce app; easy navigation, intuitive info discovery.
- **1.2** Produce a **fully robust** codebase.
- **1.3** CRUD actions are immediately reflected in the UI.
- **1.4** Follow a thorough **testing approach** (manual and/or automated) evidenced in commits.
- **1.5** Configure efficiently: Procfile, requirements.txt, settings; single datastore configuration location.
- **1.6** Fully describe the **data schema** in the README.
- **1.7** Use version control effectively to record development.
- **2.1** User has full control of their interaction.
- **2.2** Site purpose is immediately evident to a new user.
- **2.3** Site provides a good solution to user demands/expectations.
- **3.1** Control sitemap via **robots.txt**.
- **3.2** All sitemap links are **canonical**.
- **3.3** Use descriptive metadata that accurately reflects the site’s purpose.
- **4.1** Users only access intended views and functionality.
- **5.1** Document the **primary marketing strategy**.
- **6.1** Clear, well‑defined purpose addressing target audience needs.

> **Important:** All MERIT criteria must be achieved for a Merit to be awarded.

---

## DISTINCTION Performance (characteristics of high‑level performance)

- **Clear, justified rationale** for a real‑world application; fully functioning, interactive app.
- **Publishable quality** UI/UX adhering to current practice; no logic errors. Any deviations from accepted design/UX are justified for the target user.
- **Original** application (not a copy of walkthroughs).

### Amplification — Craftsmanship

**Front‑End Design**
- Information hierarchy with semantic markup; content organised and easy to find.
- Resources discoverable; layout intuitive; information prioritised.
- Positive emotional response: clear navigation/feedback; no aggressive pop‑ups/autoplay.
- Users who land on non‑existent pages are gracefully redirected.
- Do not ask for data you already have; show **progress indicators** and **feedback** on transactions.
- **Accessibility** guidelines followed across pages/interactions.

**Development & Implementation**
- **Clean code**; consistent naming conventions (files, classes, functions, variables); cross‑platform friendly names.
- Consistent app URLs and file structure (assets grouped; clear separation of custom vs libraries).
- Readability: consistent indenting; no unnecessary blank lines; semantic markup; HTML/CSS/JS/Python in appropriate files; JS linked appropriately; defensive design (validation, error handling, graceful API failures); comments explain purpose.
- Compliant code: HTML (W3C), CSS (Jigsaw), JS (linter), Python (PEP8/explicit style guide).
- Robust code: no logic errors; errors handled; back/forward navigation cannot break the site; no broken links; user actions don’t cause internal errors.

**Security & Config**
- Secrets in env vars or ignored files; logged‑in gating enforced; permissions appropriate.
- Framework conventions followed correctly (Django templates/apps/models/views; MVC/MVT separation; organised settings).

**Data**
- Well‑structured data with clear relationships; shared across apps (no duplication); CRUD present and reflected immediately; datastore config centralised and easy to change.

**Testing & Real‑World Fit**
- Comprehensive testing with good coverage; errors corrected or documented.
- SEO/marketing features evident; one or more marketing strategies employed and documented.
- Real content (no Lorem Ipsum); external links open in new tab where appropriate; design aligned to initial user stories and purpose.

---

## README Notes (recommended structure)

- Project summary, **Live site link**, **Repo link**
- Features with screenshots
- How to run locally (venv, install, env vars, migrate, runserver)
- Deployment steps (including DB)
- Testing approach (manual/automated) and Stripe test card details
- Data schema/ERD
- Accessibility & performance notes
- Credits & attributions

---

## Plagiarism Reminder

You must attribute any external code or assets used. Secrets stay out of the repo. Reuse is fine **with citation**; uncredited code is treated as plagiarism.

---

### Quick PASS Evidence Checklist (printable)

- [ ] Products list/detail; Add→Bag→Checkout works
- [ ] Stripe test payment succeeds; feedback shown on success/failure
- [ ] Three+ **custom models** implemented
- [ ] CRUD implemented (admin + at least one form with validation)
- [ ] Auth + RBAC (non‑staff blocked from admin functions)
- [ ] SEO: title, meta description, sitemap, robots.txt; 404 page
- [ ] README complete (purpose, run/deploy/testing, screenshots)
- [ ] Secure deploy: secrets in env; DEBUG=False; no broken links

