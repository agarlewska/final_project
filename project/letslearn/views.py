from datetime import date, timedelta

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
    """ View to check whether user is logged in or log out. """
    def get(self, request):
        current_user = request.user
        context = {'current_user': current_user}
        return render(request, 'index.html', context)


class MaterialListView(LoginRequiredMixin, View):
    """
    Display a training materials' list.

    **Context**

    ``UserMaterial``
        Instances of UserMaterial model connected to logged user.
        Training materials can't have atribute is_archived = True.

    **Template:**

    :template: 'material_list.html'
    """
    def get(self, request):
        """
        Prepares data for context in MaterialListView.
        :return:
            Instances of UserMaterial model connected to logged user.
            Training materials can't have atribute is_archived = True.
        """
        all_materials = UserMaterial.objects.filter(user_id=self.request.user)
        materials = [material for material in all_materials if material.material_id.is_archived is False]
        materials_near_end = [material for material in materials
                              if material.material_id.is_time_limited is True
                              # and (material.material_id.expiration_date - date.today()).days <= 14
                              ]
        exp_date = date.today() + timedelta(days=14)
        categories = Category.objects.all()
        return render(request, 'material_list.html',
                      {'materials': materials,
                       'exp_date': exp_date,
                       'categories': categories})#, 'materials_near_end': materials_near_end})

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
    """
    Display an individual training material.

    **Context**

    ``TrainingMaterials``
        Instance of TrainingMaterials model connected to logged user.

    **Template:**

    :template: 'material_details.html' if instance is connected to logged user
                and  'page_404.html' if it's another user's material.
    """
    def get(self, request, pk):
        """
        Prepares context for MaterialDetailView.
        :param request: get request
        :param pk: pk of requested Training Material instance
        :return: context for MaterialDetailView
        """
        material_owner = UserMaterial.objects.get(material_id = pk)
        if material_owner.user_id == self.request.user:
            material = TrainingMaterials.objects.get(id=pk)
                # material = get_object_or_404(TrainingMaterials, id=pk)
            return render(request, 'material_details.html', {'material': material})
        else:
            return render(request, 'page_404.html', {'material': ''})

    def post(self, request, pk):
        """
        Changes parameters is_finished and is_archived of TrainingMaterials instance.
        :param request: post request
        :param pk: pk of requested Training Material instance
        :return: Saves parameters in the database and render "material_details.html" template.
        """
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
    """ Creates new TrainingMaterials model instance and redirect to "material_list.html" template. """
    model = TrainingMaterials
    fields = '__all__'

    def form_valid(self, form):
        """
        Saves information from the form and adds new record in UserMaterial model.
        :param form: form with all fields from TrainignMaterials instance.
        :return:
        New instance of TrainingMaterials model is saved in database. Corresponding record is added to UserMaterial model.
        Render "material_list.html" template.
        """
        self.object = form.save()
        UserMaterial.objects.create(material_id=self.object, user_id=self.request.user)
        return redirect(f"/materials/list/")


class CategoryListView(LoginRequiredMixin, ListView):
    """ Display a list of categories. """
    template_name = 'category_list.html'
    model = Category


class CategoryCreateView(LoginRequiredMixin, CreateView):
    """ Creates new Category model instance and redirect to "category_list.html" template."""
    model = Category
    fields = '__all__'


class MaterialCategoryListView(ListView):
    pass


class PlatformListView(LoginRequiredMixin, ListView):
    """ Displays a list of platforms. """
    template_name = 'platform_list.html'
    model = Platform


class PlatformDetailView(LoginRequiredMixin, ListView):
    """ Display an individual platform."""
    def get(self, request, pk):
        """
        Prepares context for PlatformDetailView and renders "platform_details.html".
        :param request: get request
        :param pk: pk of requested Platform instance.
        :return: render "platform_details.html" template with appropriate context.
        """
        platform = get_object_or_404(Platform, id=pk)
        return render(request, "platform_details.html", {"platform": platform})


class PlatformCreateView(LoginRequiredMixin, CreateView):
    """ Creates new Platform model instance and redirect to "platform_list.html" template."""
    model = Platform
    fields = '__all__'


class AuthorListView(LoginRequiredMixin, ListView):
    """ Displays a list of authors."""
    template_name = 'author_list.html'
    model = Author


class AuthorDetailView(LoginRequiredMixin, ListView):
    """ Display an individual author. """
    def get(self, request, pk):
        """
        Select author with id that equals pk stored in get request.
        :param request: get request
        :param pk: pk of requested Author instance.
        :return: Prepares context for AuthorDetailView and renders "author_details.html".
        """
        author = get_object_or_404(Author, id=pk)
        return render(request, "author_details.html", {"author": author})


class AuthorCreateView(LoginRequiredMixin, CreateView):
    """ Creates new Author model instance."""
    model = Author
    fields = '__all__'

    def form_valid(self, form):
        """
        Saves information stored in form. Selects new id from database and redirects to "author_detail" template.
        :param form: Form with all fields from Author instance.
        :return: New Author instance.
        """
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
    " log out current user and redirects to index page."
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