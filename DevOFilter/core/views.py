from django.shortcuts import render
from .models import Journal, Category
from django.db.models import Q


def is_vaild_query(param):
    return param != '' and param is not None


def BootstrapFilterView(request):
    qs = Journal.objects.all()
    categories = Category.objects.all()
    title_contains_query = request.GET.get('title_contains')
    ID_exact_query = request.GET.get('title_exact')
    title_or_author_query = request.GET.get('title_or_author')
    view_count_min = request.GET.get('view_count_min')
    view_count_max = request.GET.get('view_count_max')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    category = request.GET.get('category')
    reviewed = request.GET.get('reviewed')
    notreviewed = request.GET.get('notreviewed')

    if is_vaild_query(title_contains_query):
        qs = qs.filter(title__icontains=title_contains_query)

    elif is_vaild_query(ID_exact_query):
        qs = qs.filter(id=ID_exact_query)

    elif is_vaild_query(title_or_author_query):
        qs = qs.filter(Q(title__icontains=title_or_author_query) |
                       Q(author__name__icontains=title_or_author_query)
                       ).distinct()

    if is_vaild_query(view_count_min):
        qs = qs.filter(views__gte=view_count_min)
    if is_vaild_query(view_count_max):
        qs = qs.filter(views__lte=view_count_max)
    if is_vaild_query(date_min):
        qs = qs.filter(publishDate__gte=date_min)
    if is_vaild_query(date_max):
        qs = qs.filter(publishDate__lte=date_max)
    if is_vaild_query(category) and category != 'Choose...':
        qs = qs.filter(categories__name=category)
    if reviewed == 'on':
        qs = qs.filter(reviewed=True)
    elif notreviewed == 'on':
        qs = qs.filter(reviewed=False)
    context = {
        'querySet': qs,
        'categories': categories
    }
    return render(request, 'bootstrap_Form.html', context)
