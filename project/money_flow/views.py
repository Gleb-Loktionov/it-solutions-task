from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.db.models import Q

from money_flow.models import Category, Note, Status, Type
from money_flow.forms import CategoryForm, NoteForm, StatusForm, TypeForm


class NoteListView(LoginRequiredMixin, ListView):
    template_name = 'notes/index.html'
    context_object_name = 'notes'
    model = Note
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()

        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        if date_from:
            queryset = queryset.filter(created_at__gte=parse_date(date_from))
        if date_to:
            queryset = queryset.filter(created_at__lte=parse_date(date_to))

        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        note_type = self.request.GET.get('type')
        if note_type:
            queryset = queryset.filter(type=note_type)
            
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)

        main_category = self.request.GET.get('main_category')
        if main_category:
            queryset = queryset.filter(Q(category__parent=main_category) | Q(category=main_category))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['statuses'] = Status.objects.all()
        context['types'] = Type.objects.all()
        context['main_categories'] = Category.objects.filter(parent__isnull=True)
        context['categories'] = Category.objects.filter(parent__isnull=False)
        return context
    

class NoteCreateView(LoginRequiredMixin, CreateView):
    template_name = 'notes/create.html'
    model = Note
    form_class = NoteForm

    def form_valid(self, form):
        user = self.request.user
        note = form.save(commit=False)
        note.user = user
        if not note.created_at:
            note.created_at = timezone.localdate()
        note.save()
        return redirect('main')


class NoteUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'notes/update.html'
    model = Note
    form_class = NoteForm
    pk_url_kwarg = 'id'
    context_object_name = 'note'
    
    def form_valid(self, form):
        note = form.save(commit=False)
        
        if not note.created_at:
            note.created_at = self.get_object().created_at
        
        note.save()
        return redirect('main')


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    success_url = reverse_lazy('main')
    pk_url_kwarg = 'id'
    

class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'settings/create.html'
    success_url = reverse_lazy('settings_data')


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'settings/update.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('settings_data')


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    success_url = reverse_lazy('settings_data')
    pk_url_kwarg = 'id'


class TypeCreateView(LoginRequiredMixin, CreateView):
    model = Type
    form_class = TypeForm
    template_name = 'settings/create.html'
    success_url = reverse_lazy('settings_data')


class TypeUpdateView(LoginRequiredMixin, UpdateView):
    model = Type
    form_class = TypeForm
    template_name = 'settings/update.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('settings_data')


class TypeDeleteView(LoginRequiredMixin, DeleteView):
    model = Type
    success_url = reverse_lazy('settings_data')
    pk_url_kwarg = 'id'


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'settings/create.html'
    success_url = reverse_lazy('settings_data')


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'settings/update.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('settings_data')


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('settings_data')
    pk_url_kwarg = 'id'


def settings_data_view(request):
    if request.user.is_authenticated:
        statuses = Status.objects.all()
        types = Type.objects.all()
        categories = Category.objects.select_related('parent', 'type').all()
        context = {
            'statuses': statuses,
            'types': types,
            'categories': categories,
        }   
        return render(request, 'settings/settings_list.html', context)
    else:
        return redirect('login')


def get_subcategories(request):
    parent_id = request.GET.get('parent_id')
    subcategories = Category.objects.filter(parent__id=parent_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)
