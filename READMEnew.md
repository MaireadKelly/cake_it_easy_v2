# Cake It Easy v2.0

## What the Project Does
"Cake It Easy v2.0" is a full-stack Django e-commerce application designed for custom cake and cupcake orders. It allows users to easily create and order bespoke desserts that can be tailored to their specific requests.

## Why the Project is Useful
This project provides a user-friendly experience for customers looking to order custom cakes. Key features include:
- **Promotional Discount Codes**: Encourage sales by offering discounts on orders.
- **Cupcake Box-Size Pricing**: Flexibly priced options based on box sizes for cupcakes.
- **Bespoke Custom Cake Requests**: Offers users the ability to personalize their cake orders.
- **Newsletter Signup**: Keeps users informed about promotions and new products.
- **SEO and User Authentication**: Enhance visibility and ensure secure user experiences.

## Getting Started
To get started with "Cake It Easy v2.0", follow the installation and setup instructions below:

### Installation/Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/MaireadKelly/cake_it_easy_v2.git
   cd cake_it_easy_v2
   ```  
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```  
3. Set up the database:
   ```bash
   python manage.py migrate
   ```  
4. Create a superuser (admin):  
   ```bash
   python manage.py createsuperuser
   ```  
5. Run the server:
   ```bash
   python manage.py runserver
   ```
   Now, go to `http://127.0.0.1:8000/` in your browser to view the application.

### Code Examples
Here's a simple example of how to create a new cake order in the application:
```python
order = CakeOrder.objects.create(size='Large', flavor='Chocolate', custom_message='Happy Birthday!')
order.save()
```

## Where to Get Help
For support, you can find helpful resources at the following:
- **Documentation**: [Project Documentation](https://path-to-docs.com)  
- **Support**: For issues, please open an issue on the GitHub repository.

## Who Maintains and Contributes
This project is maintained by MaireadKelly. If you'd like to contribute, please refer to the [CONTRIBUTING.md](https://path-to-contributing.md) file for guidelines on how to contribute.