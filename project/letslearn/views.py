from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from .models import UserMaterial, TrainingMaterials


class IndexView(View):
    def get(self, request):
        current_user = request.user
        context = {'current_user': current_user}
        return render(request, 'index.html', context)


class MaterialListView(ListView):
    template_name = 'material_list.html'

    def get_queryset(self):
        return UserMaterial.objects.filter(user_id=self.request.user)


class MaterialDetailView(View):
        def get(self, request, material_id):
            material = get_object_or_404(TrainingMaterials, id=material_id)
            return render(request, "material_details.html", {"material": material})
