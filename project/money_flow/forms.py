from django import forms
from .models import Note, Status, Type, Category


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['status', 'type', 'category', 'total_sum', 'comment', 'created_at']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control mb-3'}),
            'type': forms.Select(attrs={'class': 'form-control mb-3'}),
            'category': forms.Select(attrs={'class': 'form-control mb-3'}),
            'total_sum': forms.NumberInput(attrs={'class': 'form-control mb-3', 'step': '0.01'}),
            'comment': forms.Textarea(attrs={'class': 'form-control mb-3', 'rows': 3}),
            'created_at': forms.DateInput(attrs={'class': 'form-control mb-3', 'type': 'date'})
        }


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

        # Если выбран родитель — делаем type необязательным
        data = self.data or None
        if data and data.get('parent'):
            self.fields['type'].required = False

    def clean(self):
        cleaned_data = super().clean()
        parent = cleaned_data.get('parent')
        type_ = cleaned_data.get('type')

        if parent:
            # Если есть родитель — берем type от него, игнорируем введенный
            cleaned_data['type'] = parent.type
        elif not type_:
            # Если родителя нет — type обязателен
            self.add_error('type', 'Укажите тип, если не выбрана родительская категория.')

        return cleaned_data