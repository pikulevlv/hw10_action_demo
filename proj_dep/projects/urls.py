from django.urls import path
from .views import index_view, \
    StaffListView, StaffDetailView, StaffCreateView,\
    StaffUpdateView, StaffDeleteView, \
    ContactFormView, UserCreateView, LoginUserView, LogoutUserView, \
    ProjectListView, ProjectDetailView, ProjectUpdateView, ProjectDeleteView, \
    RoleListView, RoleDetailView, RoleUpdateView, RoleDeleteView


app_name = 'projects'

urlpatterns = [
    path('', index_view, name='index'),
    path('staff/<int:pk>/update/', StaffUpdateView.as_view(), name='update'),
    path('staff/<int:pk>/delete/', StaffDeleteView.as_view(), name='delete'),
    path('staff/<int:pk>/', StaffDetailView.as_view(), name='staff_detail'),
    path('staff/', StaffListView.as_view(), name='staff'),
    path('registry/', UserCreateView.as_view(), name='registry'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('create_staff/', StaffCreateView.as_view(), name='create_staff'),
    path('projects_page/<int:pk>/update/', ProjectUpdateView.as_view(),
         name='update_project'),
    path('projects_page/<int:pk>/delete/', ProjectDeleteView.as_view(),
         name='delete_project'),
    path('projects_page/<int:pk>/', ProjectDetailView.as_view(),
         name='projects_detail'),
    path('projects_page/', ProjectListView.as_view(), name='projects_page'),
    path('roles_page/<int:pk>/update/', RoleUpdateView.as_view(),
         name='update_role'),
    path('roles_page/<int:pk>/delete/', RoleDeleteView.as_view(),
         name='delete_role'),
    path('roles_page/<int:pk>/', RoleDetailView.as_view(), name='roles_detail'),
    path('roles_page/', RoleListView.as_view(), name='roles_page'),
    path('contact_page/', ContactFormView.as_view(), name='contact_page'),
]
