from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView

from .models import *


def post_list(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 5)  # ограничение вывода постов до 5 штук на страницу
    page = request.GET.get('page')  # получение номера текущей страницы из GET-параметров
    posts = paginator.get_page(page)  # получение постов для текущей страницы

    context = {'posts': posts, 'post_count': post_list.count()}
    return render(request, 'index.html', context)


# class Bloglist(ListView):
#     model = Post
#     template_name = 'index.html'
#     paginate_by = 5


class BlogDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'


class AboutPageView(TemplateView):
    template_name = 'about.html'


class SearchResultsView(ListView):
    model = Post
    template_name = 'search_results.html'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('q'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context


class ViewCategory(ListView):
    class SearchResultsView(ListView):
        model = Post
        template_name = 'view_category.html'
        paginate_by = 5

        def get_context_data(self, *, object_list=None, **kwargs):
            context = super().get_context_data(**kwargs)
            context['q'] = self.request.GET.get('q')
            return context


def post_list_by_category(request, category_id):
    category = Categories.objects.get(id=category_id)
    posts = Post.objects.filter(category=category)
    return render(request, 'view_category.html', {'posts': posts})
