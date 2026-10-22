---
name: django-model-form
description: Generate robust, validated Django ModelForms styled seamlessly with Tailwind CSS and CSRF protection.
---

# Django ModelForm Skill

## Purpose
Enables automated generation of Django forms tied to PostgreSQL models with explicit validation, Tailwind CSS widget attributes, and clean error rendering.

## Example Pattern
```python
from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'priority', 'is_completed']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-lg border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:ring-2 focus:ring-brand-500',
                'placeholder': 'Enter item title...'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full px-3 py-2 border rounded-lg border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:ring-2 focus:ring-brand-500',
                'placeholder': 'Provide detailed description...'
            }),
            'priority': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border rounded-lg border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100'
            }),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 3:
            raise forms.ValidationError("Title must be at least 3 characters long.")
        return title
```
