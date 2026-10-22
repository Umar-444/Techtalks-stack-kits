from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'priority', 'is_completed']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-orange-500',
                'placeholder': 'e.g., Set up PostgreSQL connection pool'
            }),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'class': 'w-full px-4 py-2 border rounded-lg border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-orange-500',
                'placeholder': 'Add notes, acceptance criteria, or requirements...'
            }),
            'priority': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-orange-500'
            }),
            'is_completed': forms.CheckboxInput(attrs={
                'class': 'h-5 w-5 text-orange-500 rounded border-slate-300 focus:ring-orange-500'
            }),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 3:
            raise forms.ValidationError("Title must be at least 3 characters long.")
        return title
