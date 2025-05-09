from django import forms
from django.utils import timezone

from .models import Note, Status, Type, Category


class NoteForm(forms.ModelForm):
    main_category = forms.ModelChoiceField(
        queryset=Category.objects.filter(parent__isnull=True),
        required=True,
        label='Категория',
        widget=forms.Select(attrs={'class': 'form-control mb-3', 'id': 'category-select'})
    )
    
    class Meta:
        model = Note
        fields = ['status', 'type', 'main_category', 'category',  'total_sum', 'comment', 'created_at']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control mb-3'}),
            'type': forms.Select(attrs={'class': 'form-control mb-3'}),
            'category': forms.Select(attrs={'class': 'form-control mb-3', 'id': 'subcategory-select'}),
            'total_sum': forms.NumberInput(attrs={'class': 'form-control mb-3', 'step': '0.01'}),
            'comment': forms.Textarea(attrs={'class': 'form-control mb-3', 'rows': 3}),
            'created_at': forms.DateInput(attrs={'class': 'form-control mb-3', 'type': 'date'})
        }
        
        labels = {
            'category': 'Подкатегория'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['category'].required = False
        self.fields['category'].queryset = Category.objects.none()

        if 'main_category' in self.data:
            try:
                parent_id = int(self.data.get('main_category'))
                self.fields['category'].queryset = Category.objects.filter(parent_id=parent_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.category:
            parent = self.instance.category.parent
            if parent:
                self.fields['main_category'].initial = parent
                self.fields['category'].queryset = Category.objects.filter(parent=parent)
            else:
                self.fields['main_category'].initial = self.instance.category
                self.fields['category'].queryset = Category.objects.filter(parent=self.instance.category)

    def clean(self):
        cleaned_data = super().clean()
        main_category = cleaned_data.get('main_category')
        category = cleaned_data.get('category')
        
        if not category:
            cleaned_data['category'] = main_category
    

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
        }


class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'parent', 'type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'parent': forms.Select(attrs={'class': 'form-control mb-3', 'id': 'id_parent'}),
            'type': forms.Select(attrs={'class': 'form-control mb-3', 'id': 'id_type'}),
        }
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['parent'].queryset=Category.objects.filter(parent__isnull=True)
        
        data = self.data or None
        if data and data.get('parent'):
            self.fields['type'].required = False

    def clean(self):
        cleaned_data = super().clean()
        parent = cleaned_data.get('parent')
        type_ = cleaned_data.get('type')

        if parent:
            cleaned_data['type'] = parent.type
        elif not type_:
            self.add_error('type', 'Укажите тип, если не выбрана родительская категория.')

        return cleaned_data