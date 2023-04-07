from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, CreateView,  UpdateView

#from .forms import PlatformForm
from .models import UserMaterial, TrainingMaterials, Platform, Category, Author
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout


class IndexView(View):
    def get(self, request):
        current_user = request.user
        context = {'current_user': current_user}
        return render(request, 'index.html', context)


class MaterialListView(LoginRequiredMixin, ListView):
    template_name = 'material_list.html'

    def get_queryset(self):
        all_materials = UserMaterial.objects.filter(user_id=self.request.user)
        return [material for material in all_materials if material.material_id.is_archived is False]
#       return UserMaterial.objects.filter(Q(user_id=self.request.user) & Q(is_archived=False))
# def planlist(request):
#     plans = Plan.objects.all().order_by('name')
#     p = Paginator(plans, 50)
#     page = request.GET.get('page')
#     plans_list = p.get_page(page)
#     nums = "a" * plans_list.paginator.num_pages
#     if request.method == 'GET':
#         template = loader.get_template('app-schedules.html')
#         context = {'plans': plans, 'plans_list': plans_list, 'nums': nums}
#         return HttpResponse(template.render(context, request))


class MaterialDetailView(LoginRequiredMixin, View):
        def get(self, request, pk):
            material = get_object_or_404(TrainingMaterials, id=pk)
            return render(request, "material_details.html", {"material": material})

        def post(self, request, pk):
            material = get_object_or_404(TrainingMaterials, id=pk)
            if 'finished' in request.POST:
                material.is_finished = True
            elif 'unfinished' in request.POST:
                material.is_finished = False

            if 'archive' in request.POST:
                material.is_archived = True
                material.save()
                return redirect('material_list')
            elif 'restore' in request.POST:
                material.is_archived = False

            material.save()
            return render(request, "material_details.html", {"material": material})


class MaterialCreateView(LoginRequiredMixin, CreateView):
    model = TrainingMaterials
    fields = '__all__'


    def form_valid(self, form):
        self.object = form.save()
        UserMaterial.objects.create(material_id=self.object, user_id=self.request.user)
        return redirect(f"/materials/list/")

    # def save(self):


class CategoryListView(LoginRequiredMixin, ListView):
    template_name = 'category_list.html'
    model = Category


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = '__all__'


class MaterialCategoryListView(ListView):
    pass


class PlatformListView(LoginRequiredMixin, ListView):
    template_name = 'platform_list.html'
    model = Platform


class PlatformDetailView(LoginRequiredMixin, ListView):
    def get(self, request, pk):
        platform = get_object_or_404(Platform, id=pk)
        return render(request, "platform_details.html", {"platform": platform})


class PlatformCreateView(LoginRequiredMixin, CreateView):
    model = Platform
    fields = '__all__'


class AuthorListView(LoginRequiredMixin, ListView):
    template_name = 'author_list.html'
    model = Author


class AuthorDetailView(LoginRequiredMixin, ListView):
    def get(self, request, pk):
        author = get_object_or_404(Author, id=pk)
        return render(request, "author_details.html", {"author": author})


class AuthorCreateView(LoginRequiredMixin, CreateView):
    model = Author
    fields = '__all__'

    def form_valid(self, form):
        self.object = form.save()
        new_id = self.object.id
        return redirect(f"/author/{ new_id }/")


class SignUpView(View):
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(f"/materials/list/")

    def get(self, request):
        form = UserCreationForm()
        return render(request, 'sign_up.html', {'form': form})


class LogInView(LoginView):
    template_name = 'login_form.html'
    # next_page = 'material_list'
    login_redirect_url = 'material_list'
    #redirect_authenticated_user = True  # czy po zalogowaniu użytkownik ma zostać przekierowany
    # def get(self, request):
    #     form = self.form_class()
    #     message = ''
    #     return render(request, self.template_name, context={'form': form, 'message': message})
    #
    # def post(self, request):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         user = authenticate(
    #             username=form.cleaned_data['username'],
    #             password=form.cleaned_data['password'],
    #         )
    #         if user is not None:
    #             login(request, user)
    #             return redirect('home')
    #     message = 'Login failed!'
    #     return render(request, self.template_name, context={'form': form, 'message': message})

class LogOutView(LogoutView):
    next_page = 'index'    #url na który zostanie przekierowany zalogowany uzytkownik
    # redirect_authenticated_user = True   # czy po zalogowaniu użytkownik ma zostać przekierowany

class ProfileView(View):
    def get(self, request):
        return redirect(f"/materials/list/")


class PlatformUpdateView(LoginRequiredMixin, UpdateView):
    model = Platform
    fields = '__all__'
 #   template_name_suffix = '_update_form'
    template_name = "letslearn/platform_update_form.html"
    success_url = '/platform/list/'

    # def get_object(self, queryset=None):
    #     return Platform.objects.get(pk=self.request.GET.get('pk'))

class AuthorUpdateView(LoginRequiredMixin, UpdateView):
    model = Author
    fields = '__all__'
 #   template_name_suffix = '_update_form'
    template_name = "letslearn/author_update_form.html"
    success_url = '/author/list/'