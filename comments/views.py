from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.core.paginator import Paginator
from django.http import Http404

from .models import Comment
from .forms import CommentForm, ContactForm

# Create your views here.
def add(request):
    if(request.method == 'POST'):
        form = CommentForm(request.POST)
        form.save()
        return redirect('comments:index')
    else:
        #GET
        form = CommentForm()
    return render(request, 'comments/add.html', {'form':form})
# def add(request):
#     if(request.method == 'GET'):
#         pass
#     if(request.method == 'POST'):
#         #save
#         if request.POST.get('text') != '':
#             comment = Comment()
#             comment.text = request.POST.get('text')
#             comment.save()
#         else: 
#             print('Campo es vacio')

#     return render(request, 'add.html')

def index(request):
    comments = Comment.objects.all()
    # comments = get_list_or_404(Comment, pk__gt=14)
    paginator = Paginator(comments,2)

    page_number = request.GET.get('page')
    comments_page = paginator.get_page(page_number)

    return render(request, 'comments/index.html', {'comments': comments_page})

def update(request, pk):

    comment = get_object_or_404(Comment,pk=pk)

    # try:
    #     comment = Comment.objects.get(pk=pk)
    # except Comment.DoesNotExist:
    #     raise Http404

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
    
        if form.is_valid():
            form.save()
            return redirect('comments:index')
    else:
        form = CommentForm(instance=comment)
        
    return render(request, 'comments/add.html', {'form':form, 'comment':comment })

def delete(request, pk):
    # comment = Comment.objects.get(pk=pk)
    comment = Comment.objects.get(pk=pk)


    if request.method == 'POST':
        comment.delete()
        return redirect('comments:index')
    

def contact(request):
    
    form = ContactForm()
    return render(request, 'comments/contact.html', {'form':form})

def filter(request):
    contentHTML = '<button type="button">Send</button>'
    return render(request, 'comments/filter.html', { 'array': [1,2,3,4,5,6], 'contentHTML': contentHTML})