from .models import Category

def all_categories(request):
    return {'ALL_CATEGORIES': Category.objects.all()}
