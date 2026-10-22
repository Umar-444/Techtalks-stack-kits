from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, View
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Item
from .forms import ItemForm

class ItemListView(ListView):
    model = Item
    template_name = 'index.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ItemForm()
        context['total_count'] = Item.objects.count()
        context['completed_count'] = Item.objects.filter(is_completed=True).count()
        context['pending_count'] = context['total_count'] - context['completed_count']
        return context

class ItemCreateView(CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'index.html'
    success_url = reverse_lazy('app:item_list')

    def form_valid(self, form):
        messages.success(self.request, "Item created successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        items = Item.objects.all()
        return render(self.request, 'index.html', {
            'form': form,
            'items': items,
            'total_count': items.count(),
            'completed_count': items.filter(is_completed=True).count(),
            'pending_count': items.filter(is_completed=False).count(),
        })

class ItemToggleView(View):
    def post(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        item.is_completed = not item.is_completed
        item.save()
        status_str = "completed" if item.is_completed else "marked pending"
        messages.info(request, f"Item '{item.title}' {status_str}.")
        return redirect('app:item_list')
