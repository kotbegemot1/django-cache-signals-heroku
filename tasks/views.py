from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from tasks.models import TodoItem, Category, Priority


def ex():
    pass

def index(request):

    # 1st version
    # counts = {t.name: random.randint(1, 100) for t in Tag.objects.all()}

    # 2nd version
    # counts = {t.name: t.taggit_taggeditem_items.count()
    # for t in Tag.objects.all()}

    # 3rd version

    categories = Category.objects.all()
    priorities = Priority.objects.all()

    return render(request, "tasks/index.html", {"categories": categories, 'priorities':priorities})


def filter_tasks(tags_by_task):
    return set(sum(tags_by_task, []))


def tasks_by_cat(request, cat_slug=None):
    u = request.user
    tasks = TodoItem.objects.filter(owner=u).all()

    cat = None
    if cat_slug:
        cat = get_object_or_404(Category, slug=cat_slug)
        tasks = tasks.filter(category__in=[cat])

    categories = []
    for t in tasks:
        for cat in t.category.all():
            if cat not in categories:
                categories.append(cat)

    return render(
        request,
        "tasks/list_by_cat.html",
        {"category": cat, "tasks": tasks, "categories": categories},
    )


class TaskListView(ListView):
    model = TodoItem
    context_object_name = "tasks"
    template_name = "tasks/list.html"

    def get_queryset(self):
        u = self.request.user
        qs = super().get_queryset()
        return qs.filter(owner=u)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_tasks = self.get_queryset()
        # tags = []
        # print()
        # print(user_tasks)
        # print()
        categories = []

        for t in user_tasks:
            for cat in t.category.all():
                if cat not in categories:
                    categories.append(cat)
        context["categories"] = categories

        return context


class TaskDetailsView(DetailView):
    model = TodoItem
    template_name = "tasks/details.html"

from django.views.decorators.cache import cache_page
from datetime import datetime

@cache_page(60*5)
def cache_test(request):
    return render(request, 'tasks/cache_test.html', context={'now': datetime.now().strftime("%A, %d. %B %Y %H:%M:%S")})