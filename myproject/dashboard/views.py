from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic.edit import CreateView
# from .models import Room,Document
# from django.contrib.messages.views import SuccessMessageMixin
# from .forms import BlogForm
# from .models import Editor


# Create your views here.
@login_required
def dashboard(request):
    return render(request, "dashboard/dashboard.html")


# class AddBlog(SuccessMessageMixin, CreateView):
#     form_class = BlogForm
#     model = Editor
#     template_name = "dashboard/create.html"
#     success_message = "Added Succesfully"

#     def get_success_url(self):
#         return reverse('create')
# from django.shortcuts import render

def editor(request,room):
    # room=room
    return render(request, 'dashboard/editor.html',{'room':room})

def create(request):
    return render(request,'dashboard/create.html')

def join(request):
    return render(request,'dashboard/join.html')

def createRoom(request):
    doc_name = request.POST['doc_name']
#     print('my room name is ',doc_name)

#     # userEmail = request.POST['userEmail']
#     # if Room.objects.filter(name=room).exists():
#     #     return redirect('/'+room)
#     # else:

#     new_room = Document.objects.create(name=doc_name,created_by=request.user.username)

#     # new_member = RoomMember.objects.create(name=userEmail)

#     new_room.save()
#     room_id = str(new_room.id)

#     # new_member.save()

#     return redirect('/'+room_id)  

    # return redirect('/'+room+'/')  

def joinRoom(request):
    doc_id = request.POST['doc_id']
#     print('my document id is ',doc_id)
#     # userEmail = request.POST['userEmail']
#     if Room.objects.filter(id=doc_id).exists():
#         return redirect('/'+doc_id)
#     else:
#         messages.error(request, "Document id does not exist.")


    #     new_room = Room.objects.create(name=room)
    #     # new_member = RoomMember.objects.create(name=userEmail)
    #     new_room.save()
    #     # new_member.save()
    #     return redirect('/'+room) 
    
