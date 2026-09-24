from accounts.models import Category

def dropdown_categories(request):
    c= Category.objects.all()
    return {'dropdown': c}
