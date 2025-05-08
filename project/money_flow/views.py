from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from money_flow.models import Category, Note, Status, Type
from money_flow.forms import CategoryForm, NoteForm, StatusForm, TypeForm


class NoteList(LoginRequiredMixin, ListView):
    template_name = 'notes/index.html'
    context_object_name = 'notes'
    model = Note
    ordering = ['-created_at']
    

class NoteCreate(LoginRequiredMixin, CreateView):
    template_name = 'notes/create.html'
    model = Note
    form_class = NoteForm

    def form_valid(self, form):
        user = self.request.user
        note = form.save(commit=False)
        note.user = user
        note.save()
        return redirect('note_detail', id=note.id)


class NoteDetail(LoginRequiredMixin, DetailView):
    template_name = 'notes/detail.html'
    model = Note
    context_object_name = 'note'
    pk_url_kwarg = 'id'


class StatusCreateView(CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'settings/create.html'
    success_url = reverse_lazy('settings_data')


class TypeCreateView(CreateView):
    model = Type
    form_class = TypeForm
    template_name = 'settings/create.html'
    success_url = reverse_lazy('settings_data')


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'settings/create.html'
    success_url = reverse_lazy('settings_data')


def settings_data_view(request):
    statuses = Status.objects.all()
    types = Type.objects.all()
    categories = Category.objects.select_related('parent', 'type').all()

    context = {
        'statuses': statuses,
        'types': types,
        'categories': categories,
    }
    return render(request, 'settings/settings_list.html', context)