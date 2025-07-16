# cake_it_easy_v2

## Agile Development and GitHub Project Management

This project uses Agile methodology and the MoSCoW prioritisation method to manage features and priorities.

### GitHub Project Setup:

- **Project Board:** Tracks all user stories and tasks across columns for easy workflow management (To Do, In Progress, Done).
- **Milestones:** Tasks are grouped under five functional epics:
  - User Authentication & Profile
  - E-commerce Features
  - Product Management (Admin)
  - Digital Marketing & SEO
  - Testing & Security
- **Labels:** MoSCoW prioritisation is applied via labels:
  - Must: High-priority features required for core functionality
  - Should: Important features that enhance functionality
  - Could: Optional features included if time allows
- All user stories are tracked through GitHub Issues linked to the project board, milestones, and MoSCoW labels.

This setup ensures an organised and iterative development process with clear visibility on progress and priorities.

### 📝 Code Formatting Setup

- **Python files** are automatically formatted on save using **Black Formatter** (PEP8 compliant).
- **Django templates (`django-html`)** are not auto-formatted to preserve intentional spacing and layout choices.
  - This ensures template readability and prevents unwanted collapsing of HTML structure.
  - Developers are encouraged to use **Emmet abbreviations** and manual indentation (4 spaces) for clean, maintainable template files.
- **VS Code Setup Includes**:
  - Auto-activation of Python virtual environment.
  - Prettier installed but **disabled for Django templates** to avoid structure disruption.
  - Emmet enabled for quick HTML/Django template expansions.
