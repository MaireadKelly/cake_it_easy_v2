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

### Code Formatting

This project uses the following formatting setup for code consistency:

- **Python files** are automatically formatted on save using **Black Formatter** (PEP8-compliant).
- **Django templates** are formatted using **Beautify**, which provides clean indentation and spacing for improved readability.
    - Beautify has been selected for this project to restore familiar auto-indentation behavior within templates and minimise manual formatting.
    - Note: Beautify is no longer actively maintained but remains effective for Django templates in VS Code as of this project build.
- **Emmet** is enabled for rapid HTML/Django template expansion.

