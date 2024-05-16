from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from uuid import UUID

from .models import Document, DocMember
@login_required
def dashboard(request):
    documents = Document.objects.filter(created_by = request.user)
    
    return render(request, "dashboard/dashboard.html",{'documents':documents})


def editor(request, room):
    # room=room
    if not request.user.is_anonymous:
        print('hello buddy', room)
        try:
            room_uuid = UUID(room)
            doc = Document.objects.get(id=room_uuid)
            print('length of my doc is:', doc)
            temp = DocMember.objects.filter(doc_ID=room_uuid, approve=True)
            print('my temp is ', len(temp))
            for i in temp:
                print(i)
            
            if temp:
             
                return render(request, 'dashboard/editor.html', {'room': room,'document_title':doc.name,'content':doc.text})
            else:
               
                messages.error(request, "Not Approved.")
        except (ValueError, Document.DoesNotExist):
           
            print('gadbad hogyi')
            messages.error(request, "Document id does not exist.")

        return redirect('/join')

    return redirect('/login')

def save_content(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        print(content)
        doc_id = request.POST.get('room')
        Document.objects.filter(id=doc_id).update(text=content)
        return redirect(f'/document/{doc_id}')
    else:
        return HttpResponse('Invalid request method')

def create(request):
    return render(request, 'dashboard/create.html')




def join(request):
    print(request.user)
    docs =  Document.objects.filter(created_by = request.user)
    doc_list = list(docs.values_list('id',flat = True))
    joined_documents = DocMember.objects.filter(userId=request.user).exclude(doc_ID__in = doc_list)
    return render(request, 'dashboard/join.html',{'joined_documents':joined_documents})


def createRoom(request):
    doc_name = request.POST['doc_name']
    print('my room name is ', doc_name)
    new_room = Document.objects.create(name=doc_name, created_by=request.user)
    new_room.save()
    room_id = str(new_room.id)
    try:
        docmem = DocMember.objects.get_or_create(
            userId=request.user, doc_ID=new_room)
        temp = DocMember.objects.filter(doc_ID=room_id, approve=True)

        if temp:
            return redirect('/document/'+room_id)
        else:
            messages.error(request, "Not Approved.")
    except Document.DoesNotExist:
        print('gadbad hogyi')
        messages.error(request, "Document id does not exist.")


def joinRoom(request):
    if request.method == 'POST':
        doc_id = request.POST.get('doc_id')
        print('my document id is', doc_id)

        try:
          
            doc = Document.objects.get(id=doc_id)
            docmem = DocMember.objects.get_or_create(
                userId=request.user, doc_ID=doc)
            temp = DocMember.objects.filter(doc_ID=doc_id, approve=True)

            if temp:
             
                return redirect('/document/'+doc_id)
            else:
            
                messages.error(request, "Not Approved.")
        except Document.DoesNotExist:
           
            print('gadbad hogyi')
            messages.error(request, "Document id does not exist.")

    return redirect('/join')

