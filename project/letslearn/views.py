from django.shortcuts import render
from django.views import View


class IndexView(View):
    def get(self, request):
        current_user = request.user
        context = {'current_user': current_user}
        return render(request, 'index.html', context)

