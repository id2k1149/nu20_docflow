from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from .models import Task, Document
from .forms import SearchForm, DocumentAddEditForm
from django.views.generic import View, TemplateView, FormView, CreateView, DetailView
from django.views.generic.base import ContextMixin

from django.db.models import Q
# Create your views here.


class IndexView(TemplateView):
    """
    Здесь стартовая страница, поэтому не будем отображать ее как
    """

    template_name = 'docflowapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        documents = Document.objects.all().order_by('-date')[:5]
        tasks = Task.objects.all().order_by('-date')[:5]
        context['nbar'] = 'index'
        context['documents'] = documents
        context['tasks'] = tasks
        return context


class SearchView(View):
    """
    Здесь будут по разному отрабатываться get и post запрос
    """

    def get(self, request, *args, **kwargs):
        search_form = SearchForm()
        return render(request, 'docflowapp/search.html', context={'nbar': 'search', 'search_form': search_form})

    def post(self, request, *args, **kwargs):

        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            type = search_form.cleaned_data['type']
            nom = search_form.cleaned_data['nom']
            date_from = search_form.cleaned_data['date_from']
            date_to = search_form.cleaned_data['date_to']
            description = search_form.cleaned_data['description']
            all = search_form.cleaned_data['all']

            q1 = Document.objects
            if type is not None:
                q1 = q1.filter(type=type)
            if nom is not None:
                q1 = q1.filter(nom__istartswith=nom)
            if date_from is not None:
                q1 = q1.filter(date__gte=date_from)
            if date_to is not None:
                q1 = q1.filter(date__lte=date_from)
            if description is not None:
                q1 = q1.filter(description__icontains=description)
            if all is not None:
                q1 = q1.filter(Q(nom__icontains=all) | Q(description__icontains=all))
            documents = q1.all()
            documents_count = documents.count()
            return render(request, 'docflowapp/searchResult.html', context={'nbar': 'search', 'documents': documents, 'documents_count': documents_count})

        else:
            return render(request, 'docflowapp/search.html', context={'nbar': 'search', 'search_form': search_form})


class DocumentView(DetailView):

    model = Document
    template_name = 'docflowapp/documentView.html'
    context_object_name = 'document'


class DocumentAdd(CreateView):


    #fields = '__all__'
    #model = Document
    #fields = ('type', 'nom', 'date', 'counterpart', 'description', 'classifier')

    form_class = DocumentAddEditForm
    success_url = reverse_lazy('docflowapp:index')
    template_name = 'docflowapp/documentAdd.html'



#def index_view(request):
#
#    documents = Document.objects.all().order_by('-date')[:5]
#    tasks = Task.objects.all().order_by('-date')[:5]
#    return render(request, 'docflowapp/index.html', context={'nbar': 'index', 'documents': documents, 'tasks': tasks})


#def search_view(request):
#
#    if request.method == 'POST':
#        return render(request, 'docflowapp/UnderConstruction.html')
#    else:
#
#        return render(request, 'docflowapp/search.html', context={'nbar': 'search', 'search_form': search_form })


