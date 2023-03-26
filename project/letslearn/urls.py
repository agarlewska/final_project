from django.urls import path

from .views import IndexView, MaterialListView, MaterialDetailView, PlatformCreateView, PlatformListView, \
    PlatformDetailView, MaterialCreateView, CategoryListView, CategoryCreateView, MaterialCategoryListView, \
    AuthorListView, AuthorDetailView, AuthorCreateView, SignUpView, LogInView, LogOutView, ProfileView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/login/', LogInView.as_view(), name='login'),
    path('accounts/profile/', ProfileView.as_view(), name='login_profile'),
    path('accounts/logout/', LogOutView.as_view(), name='logout'),
    path('materials/list/', MaterialListView.as_view(), name='material_list'),
    path('materials/<int:material_id>/', MaterialDetailView.as_view(), name='material_details'),
    path('materials/create/', MaterialCreateView.as_view(), name='material_create'),
    path('category/list/', CategoryListView.as_view(), name='category_list'),
    # path('categ/<int:platform_id>/', PlatformDetailView.as_view(), name='platform_details'),
    # path('category/materials/', MaterialCategoryListView.as_view(), name='material_list_by_category'),
    path('category/create/', CategoryCreateView.as_view(), name='category_create'),
    path('platform/list/', PlatformListView.as_view(), name='platform_list'),
    path('platform/<int:platform_id>/', PlatformDetailView.as_view(), name='platform_details'),
    path('platform/create/', PlatformCreateView.as_view(), name='platform_create'),
    path('author/list/', AuthorListView.as_view(), name='author_list'),  #to chyba bez sensu
    path('author/<int:author_id>/', AuthorDetailView.as_view(), name='author_details'),
    path('author/create/', AuthorCreateView.as_view(), name='author_create'),
]
