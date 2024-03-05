from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import BlogForm
from .models import Editor


# Create your views here.
@login_required
def dashboard(request):
    return render(request, "dashboard/dashboard.html")


class AddBlog(SuccessMessageMixin, CreateView):
    form_class = BlogForm
    model = Editor
    template_name = "dashboard/create.html"
    success_message = "Added Succesfully"

    def get_success_url(self):
        return reverse('create')
