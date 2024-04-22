from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from uuid import UUID

from .models import Document,DocMember
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
    if not request.user.is_anonymous:
        print('hello buddy',room)
        try:
            room_uuid = UUID(room)
            # Retrieve the document object
            doc = Document.objects.get(id=room)
            
            # Create DocMember object
            # docmem = DocMember.objects.get_or_create(userId=request.user, doc_ID=doc)
            temp =DocMember.objects.filter(doc_ID=room,approve=True)
            
            if temp:
                # Redirect to '/' with doc_id as a parameter
                return render(request, 'dashboard/editor.html',{'room':room})
            else:
                # If not approved, show error message
                messages.error(request, "Not Approved.")
        except (ValueError,Document.DoesNotExist):
            # If document does not exist, show error message
            print('gadbad hogyi')
            messages.error(request, "Document id does not exist.")
            


        return redirect('/join') 

    
    return redirect('/login')

def create(request):
    return render(request,'dashboard/create.html')

def join(request):
    return render(request,'dashboard/join.html')

def createRoom(request):
    doc_name = request.POST['doc_name']
    print('my room name is ',doc_name)

    # userEmail = request.POST['userEmail']
    # if Room.objects.filter(name=room).exists():
    #     return redirect('/'+room)
    # else:

    new_room = Document.objects.create(name=doc_name,created_by=request.user)

    # new_member = RoomMember.objects.create(name=userEmail)

    new_room.save()
    room_id = str(new_room.id)

    # new_member.save()

    return redirect('/document/'+room_id)  

    

def joinRoom(request):
    if request.method == 'POST':
        doc_id = request.POST.get('doc_id')  # Use get() to avoid KeyError
        print('my document id is', doc_id)
        
        try:
            # Retrieve the document object
            doc = Document.objects.get(id=doc_id)
            
            # Create DocMember object
            docmem = DocMember.objects.get_or_create(userId=request.user, doc_ID=doc)
            temp =DocMember.objects.filter(doc_ID=doc_id,approve=True)
            
            if temp:
                # Redirect to '/' with doc_id as a parameter
                return redirect('/document/'+doc_id)
            else:
                # If not approved, show error message
                messages.error(request, "Not Approved.")
        except Document.DoesNotExist:
            # If document does not exist, show error message
            print('gadbad hogyi')
            messages.error(request, "Document id does not exist.")


    return redirect('/join') 
    
def saveContent(request,room):
    data = request.POST.get('content')
    print('saving data',data)
    # return redirect('/')