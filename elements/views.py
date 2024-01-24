from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from .forms import ElementForm
from .models import Element

def add(request):
    if request.method == 'POST':
        form = ElementForm(request.POST)
        if form.is_valid():
            element = Element()
            element.title = form.cleaned_data['title']
            element.slug = form.cleaned_data['slug']
            element.description = form.cleaned_data['description']
            # element.price = form.cleaned_data['price']
            element.category = form.cleaned_data['category']
            element.type = form.cleaned_data['type']
            element.save()
        # return redirect('elements:index')
    else:
        form = ElementForm()
    
    return render(request, 'element/add.html', {'form':form})

def index(request):
    elements = Element.objects.all()
    paginator = Paginator(elements, 10)

    page_number = request.GET.get('page')

    return render(request, 'element/index.html',{'elements': paginator.get_page(page_number)})