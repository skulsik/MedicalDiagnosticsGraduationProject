from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView

from blog.forms import BlogCreateForm
from blog.models import Blog


class BlogCreateView(LoginRequiredMixin, CreateView):
    """ Создание блога """
    model = Blog
    form_class = BlogCreateForm

    def get_success_url(self):
        """ Берем slug из данного объекта """
        return reverse_lazy('blog:view_blog', args=(self.object.slug,))

    def form_valid(self, form):
        """ Автоматически сохраняет текущего пользователя в поле user """
        # Создает форму в памяти, без отправки в бд
        self.object = form.save(commit=False)
        # Передает текущего пользователя в user
        self.object.owner = self.request.user
        # Сохраняет в бд
        self.object.save()
        return super(BlogCreateView, self).form_valid(form)


class BlogView(DetailView):
    """ Отображение блога """
    model = Blog

    def get_object(self, queryset=None):
        """ Получает объект, увеличивает просмотры """
        object_blog = super().get_object()
        object_blog.number_of_views += 1
        object_blog.save()
        return object_blog


class BlogUserListView(LoginRequiredMixin, ListView):
    """ Все блоги данного пользователя """
    model = Blog
    template_name = 'blog/blog_user_list.html'

    def get_queryset(self):
        """ Получает статьи текущего пользователя """
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user) & queryset.filter(publication=True)
        return queryset


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    """ Удаление блога """
    model = Blog
    success_url = reverse_lazy('blog:user_list_blog')


class BlogListView(ListView):
    """ Все статьи с активной публикацией """
    model = Blog

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(publication=True)
        return queryset


class BlogUpdateView(UpdateView):
    """ Обновление блога """
    model = Blog
    form_class = BlogCreateForm
    success_url = reverse_lazy('blog:user_list_blog')
