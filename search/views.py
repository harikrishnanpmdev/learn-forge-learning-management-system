from django.shortcuts import render
from django.views import View
from accounts.models import Course
from django.db.models import Q

class SearchView(View):
    def get(self, request):
        srh = request.GET.get('c', '')
        courses = Course.objects.filter(
            Q(title__icontains=srh) |
            Q(language__icontains=srh) |
            Q(category__name__icontains=srh) |
            Q(tags__name__icontains=srh) |
            Q(instructor__user__first_name__icontains=srh) |
            Q(instructor__user__last_name__icontains=srh) |
            Q(level__icontains=srh)
            ).distinct() #is used to remove duplicate records
        context = {'courses': courses, 'search_term': srh}
        return render(request, 'search.html', context)
