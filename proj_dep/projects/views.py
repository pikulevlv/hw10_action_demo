from django.shortcuts import render
from .models import Staff, StaffListPosition, Direction, Sertificate
from .models import Project, Stage, Role
# from celery import current_app
from django.views.generic import ListView, DetailView, UpdateView, \
    CreateView, FormView, DeleteView
from .forms import ContactForm, StaffForm, RegistrationForm, LoginForm, ProjectForm, RoleForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class AdminOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        # просто сформулировать условие выдачи прав
        # return self.request.user.email.endswith('@example.com')
        return self.request.user.is_superuser


class StaffOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

# - - - - - - - - - - - - - - - - - - - - - - - - -

def index_view(request):
    context = {}
    context['staff_units'] = Role.objects.all().count()
    context['proj_units'] = Project.objects.all().count()
    context['dir_units'] = Direction.objects.all().count()
    context['sl_units'] = StaffListPosition.objects.all().count()
    context['sert_units'] = Sertificate.objects.all().count()
    context['active_page'] = '1'
    return render(request, 'projects/index.html', context)

# - - - - - - - - - - - - - - - - - - - - - - - - -


class StaffListView(ListView):
    model = Staff # Модель, которую нужно вывести в список
    template_name = 'projects/staff.html' # в какой шаблон выведем данные

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['active_page'] = '1'
        return context


class StaffDetailView(LoginRequiredMixin, DetailView):
    model = Staff
    template_name = 'projects/staff_detail.html'


class StaffCreateView(StaffOnlyMixin, CreateView):
    model = Staff
    template_name = 'projects/edit_create_staff.html'
    success_url = '/'
    form_class = StaffForm

    def form_valid(self, form):
        user = self.request.user # мы т.к. в форме создания змеи скрывали пользователя
        form.instance.user = user # прописываем его из инстанса формы
        return super().form_valid(form) # сохраняем форму


class StaffUpdateView(StaffOnlyMixin, UpdateView):
    model = Staff
    template_name = 'projects/edit_create_staff.html'
    success_url = '/'
    form_class = StaffForm


class StaffDeleteView(AdminOnlyMixin, DeleteView):
    model = Staff
    template_name = 'projects/delete_confirm_staff.html'
    success_url = '/'

# - - - - - - - - - - - - - - - - - - - - - - - - -

class ProjectListView(ListView):
    model = Project # Модель, которую нужно вывести в список
    template_name = 'projects/projects_page.html' # в какой шаблон выведем данные

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['active_page'] = '1'
        return context


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/projects_detail.html'


class ProjectCreateView(StaffOnlyMixin, CreateView):
    model = Project
    template_name = 'projects/edit_create_project.html'
    success_url = '/projects/'
    # fields = '__all__' # возьмем все поля
    # fields = ('name',) # перечислим нужные поля
    # исключить ненужные поля можно в формах
    form_class = ProjectForm

    def form_valid(self, form):
        user = self.request.user # мы т.к. в форме создания змеи скрывали пользователя
        form.instance.user = user # прописываем его из инстанса формы
        return super().form_valid(form) # сохраняем форму


class ProjectUpdateView(StaffOnlyMixin, UpdateView):
    model = Project
    template_name = 'projects/edit_create_project.html'
    success_url = '/'
    form_class = ProjectForm


class ProjectDeleteView(AdminOnlyMixin, DeleteView):
    model = Project
    template_name = 'projects/delete_confirm_project.html'
    success_url = '/'

# - - - - - - - - - - - - - - - - - - - - - - - - -

class RoleListView(ListView):
    model = Role # Модель, которую нужно вывести в список
    template_name = 'projects/roles_page.html' # в какой шаблон выведем данные

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['active_page'] = '1'
        return context


class RoleDetailView(LoginRequiredMixin, DetailView):
    model = Role
    template_name = 'projects/roles_detail.html'


class RoleCreateView(StaffOnlyMixin, CreateView):
    model = Role
    template_name = 'projects/edit_create_role.html'
    success_url = '/roles_page/'
    form_class = RoleForm

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)

class RoleUpdateView(StaffOnlyMixin, UpdateView):
    model = Role
    template_name = 'projects/edit_create_role.html'
    success_url = '/roles_page/'
    # fields = '__all__' # возьмем все поля
    form_class = RoleForm

class RoleDeleteView(AdminOnlyMixin, DeleteView):
    model = Role
    template_name = 'projects/delete_confirm_role.html'
    success_url = '/roles_page/'

# - - - - - - - - - - - - - - - - - - - - - - - - -

class ContactFormView(LoginRequiredMixin, FormView):
    template_name = "projects/contact_page.html"
    form_class = ContactForm
    success_url = '/'

# - - - - - - - - - - - - - - - - - - - - - - - - -


class LoginUserView(LoginView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'projects/login.html'


class LogoutUserView(LogoutView):
    pass

# - - - - - - - - - - - - - - - - - - - - - - - - -


class UserCreateView(CreateView):
    model = User
    form_class = RegistrationForm
    success_url = '/login/'
    template_name = 'projects/register.html'
