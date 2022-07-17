from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .form import AddPostForm, RegisterUserForm, LoginUserForm
from .models import *
from main.utils import DataMixin
from django.views.generic import DetailView, ListView

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        #{'title': "Войти", 'url_name': 'login'}
]


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class BlogHome(ListView):
    model = Post
    template_name = 'main/index.html'
    context_object_name = 'posts'
    extra_context = {'title': 'Главная страница'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context["title"] = 'Главная страница'
        context['cat_selected'] = 0
        return context

    def get_queryset(self):
        return Post.objects.filter(is_published=True)


#def index(request, cat_id):
#    posts=Post.objects.all()
#    cats=Category.objects.all()
#
#    if len(posts) == 0:
#        raise Http404
#
#    context = {
#        "posts": posts,
#        "cats": cats,
#        "menu": menu,
#        "title": 'Главная страница',
#        "cat_selected": cat_id,
#
#    }
#    return render(request, 'mian/index.html', context=context)


def about(request):
    return render(request, 'main/about.html', {'title': 'Страница о нас'})


#def login(request):
#   return HttpResponse("Авторизация")


class ShowPost(DataMixin, DetailView):
    model = Post
    template_name = 'main/post.html'
    slug_url_kwarg = 'post_slug'
    # pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post']
        context['menu'] = menu
        return context


# def show_post(request, post_slug):
#     post = get_object_or_404(Post, pk=post_slug)  # вместо pk - slug
#
#     context = {
#         'posts': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#
#     return render(request, 'main/post.html', context=context)


class PostCategory(ListView):
    model = Post
    template_name = 'main/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        context['menu'] = menu
        context['cat_selected'] = context['posts'][0].cat_id
        return context


# def show_category(request, cat_id):
#     posts=Post.objects.all()
#     cats=Category.objects.all()
#
#     context = {
#         "posts": posts,
#         "cats": cats,
#         "menu": menu,
#         "title": 'Отображение по рубрикам',
#         "cat_selected": cat_id,
#
#     }
#     return render(request, 'main/index.html', context=context)


class AddPage(CreateView):
    form_class = AddPostForm
    template_name = 'main/addpage.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьи'
        context['menu'] = menu
        return context


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             #print(form.cleaned_data)
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'main/addpage.html', {"menu": menu, 'form': form, "title": 'Добавление страницы'})


def contact(request):
    return HttpResponse("Обратная связь")


def categories(request):
    return HttpResponse("Авторизация")


def archive(request, year):
    if int(year) > 2022:
        # raise Http404()
        return redirect('home', permanent=True)
    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
