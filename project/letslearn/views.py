from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, CreateView
from .models import UserMaterial, TrainingMaterials, Platform, Category, Author


class IndexView(View):
    def get(self, request):
        current_user = request.user
        context = {'current_user': current_user}
        return render(request, 'index.html', context)


class MaterialListView(ListView):
    template_name = 'material_list.html'
    paginate_by = 10

    def get_queryset(self):
        all_materials = UserMaterial.objects.filter(user_id=self.request.user)
        return [material for material in all_materials if material.material_id.is_archived is False]
#       return UserMaterial.objects.filter(Q(user_id=self.request.user) & Q(is_archived=False))


class MaterialDetailView(View):
        def get(self, request, material_id):
            material = get_object_or_404(TrainingMaterials, id=material_id)
            return render(request, "material_details.html", {"material": material})

        def post(self, request, material_id):
            material = get_object_or_404(TrainingMaterials, id=material_id)
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


class MaterialCreateView(CreateView):
    model = TrainingMaterials
    fields = '__all__'


    def form_valid(self, form):
        self.object = form.save()
        UserMaterial.objects.create(material_id = self.object, user_id =self.request.user)
        return redirect(f"/materials/list/")

    # def save(self):


class CategoryListView(ListView):
    template_name = 'category_list.html'
    model = Category


class CategoryCreateView(CreateView):
    model = Category
    fields = '__all__'


class MaterialCategoryListView(ListView):
    pass


class PlatformListView(ListView):
    template_name = 'platform_list.html'
    model = Platform


class PlatformDetailView(ListView):
    def get(self, request, platform_id):
        platform = get_object_or_404(Platform, id=platform_id)
        return render(request, "platform_details.html", {"platform": platform})


class PlatformCreateView(CreateView):
    model = Platform
    fields = '__all__'


class AuthorListView(ListView):
    template_name = 'author_list.html'
    model = Author


class AuthorDetailView(ListView):
    def get(self, request, author_id):
        author = get_object_or_404(Author, id=author_id)
        return render(request, "author_details.html", {"author": author})


class AuthorCreateView(CreateView):
    model = Author
    fields = '__all__'

    def form_valid(self, form):
        self.object = form.save()
        new_id = self.object.id
        return redirect(f"/author/{ new_id }/")
