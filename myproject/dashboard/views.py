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
    if not request.user.is_anonymous:
        return render(request, 'dashboard/create.html')
    return redirect('/login')




def join(request):
    if not request.user.is_anonymous:
        print(request.user)
        docs =  Document.objects.filter(created_by = request.user)
        doc_list = list(docs.values_list('id',flat = True))
        joined_documents = DocMember.objects.filter(userId=request.user).exclude(doc_ID__in = doc_list)
        return render(request, 'dashboard/join.html',{'joined_documents':joined_documents})
    return redirect('/login')


def createRoom(request):
    doc_name = request.POST['doc_name'] #getting document name from form 
    print('my room name is ', doc_name)
    new_room = Document.objects.create(name=doc_name, created_by=request.user)
    new_room.save() 
    room_id = str(new_room.id) 
    try:
        docmem = DocMember.objects.get_or_create(userId=request.user, doc_ID=new_room) 
        temp = DocMember.objects.filter(doc_ID=room_id, approve=True) 

        if temp: 
            return redirect('/document/'+room_id) #goes to editor page
        else:
            messages.error(request, "Not Approved.") 
    except Document.DoesNotExist:
        print('gadbad hogyi')
        messages.error(request, "Document id does not exist.") 


def joinRoom(request):
    if request.method == 'POST': 
        doc_id = request.POST.get('doc_id') #take doc_id from form
        print('my document id is', doc_id)

        try:
          
            doc = Document.objects.get(id=doc_id) #check doc_id exists or not
            docmem = DocMember.objects.get_or_create( userId=request.user, doc_ID=doc) #check member exists in docmember
            temp = DocMember.objects.filter(doc_ID=doc_id, approve=True) #check docmember approval 

            if temp:
             
                return redirect('/document/'+doc_id) #Go to editor page
            else:
            
                messages.error(request, "Not Approved.") 
        except Document.DoesNotExist:
           
            print('gadbad hogyi')
            messages.error(request, "Document id does not exist.")

    return redirect('/join')# redirect to same page


def delete_document(request):
    if not request.user.is_anonymous:
        if request.method == 'POST':
            try:
                doc_id = request.POST.get('docId') #doc_id from form
            # Code to delete the document with the given document_id
            # Replace this with your actual code to delete the document 
                document = Document.objects.get(id=doc_id) 
                document.delete()
            # Redirect to a success page or any other page after deletion
                documents = Document.objects.filter(created_by = request.user)
                return render(request, "dashboard/dashboard.html",{'documents':documents})
            except Document.DoesNotExist:
                return redirect('error_url')
            except Exception as e:
                return redirect('error_url')
        else:
            return HttpResponse('Invalid request method')
    return redirect('/login')


def rename_document(request):
    if not request.user.is_anonymous:
        if request.method == 'POST': 
            new_title = request.POST.get('new_title')
            print(new_title)
            doc_id = request.POST.get('room')
            Document.objects.filter(id=doc_id).update(name=new_title) 
            return redirect(f'/document/{doc_id}')
        else:
            return HttpResponse('Invalid request method')
    return redirect('/login')