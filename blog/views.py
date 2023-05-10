from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .forms import RegisterUserForm, LoginUserForm
from .models import Categories, Post


def post_list(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 3)  # ограничение вывода постов до 5 штук на страницу
    page = request.GET.get('page')  # получение номера текущей страницы из GET-параметров
    posts = paginator.get_page(page)  # получение постов для текущей страницы

    context = {'posts': posts, 'post_count': post_list.count(), 'categories': Categories.objects.all()}
    return render(request, 'index.html', context)


class BlogDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Categories.objects.all()
        return context


def aboutPageView(request):
    context = {'categories': Categories.objects.all()}
    return render(request, 'about.html', context)


class UserDetailView(DetailView):
    model = User
    template_name = "author_detail.html"


class SearchResultsView(ListView):
    model = Post
    template_name = 'search_results.html'
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('q'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        context['categories'] = Categories.objects.all()
        return context


class ViewCategory(ListView):
    model = Post
    template_name = 'view_category.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        context['categories'] = Categories.objects.all()
        return context


def post_list_by_category(request, category_id):
    category = Categories.objects.get(id=category_id)
    posts = Post.objects.filter(category=category)
    return render(request, 'view_category.html', {'posts': posts, 'categories': Categories.objects.all()})


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'registration/login.html'

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Post.objects.all()

        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('index')


@login_required
def profile_view(request):
    return render(request, 'profile.html')


class CustomLoginView(LoginView):
    template = "login.html"
    authentication_form = LoginUserForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get("remember_me")
        if not remember_me:
            self.request.session.set_expiry(0)
        return super().form_valid(form)


def signup(request):
    if request.method == 'POST':
        user_form = RegisterUserForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'registration/signup_done.html', {'new_user': new_user})
    else:
        user_form = RegisterUserForm()
    return render(request, 'registration/signup.html', {'user_form': user_form})
