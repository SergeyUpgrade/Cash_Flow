from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.generic import ListView
from django.db.models import Q
from .models import Record, Status, Type, Category, Subcategory
from .forms import RecordForm, StatusForm, TypeForm, CategoryForm, SubcategoryForm


class RecordListView(ListView):
    model = Record
    template_name = 'dds/index.html'
    context_object_name = 'records'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        # Фильтрация по параметрам GET-запроса
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        status = self.request.GET.get('status')
        type_ = self.request.GET.get('type')
        category = self.request.GET.get('category')
        subcategory = self.request.GET.get('subcategory')

        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
        if status:
            queryset = queryset.filter(status_id=status)
        if type_:
            queryset = queryset.filter(type_id=type_)
        if category:
            queryset = queryset.filter(category_id=category)
        if subcategory:
            queryset = queryset.filter(subcategory_id=subcategory)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        context['types'] = Type.objects.all()
        context['categories'] = Category.objects.all()
        context['subcategories'] = Subcategory.objects.all()
        return context


def record_create(request):
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = RecordForm()

    return render(request, 'dds/record_form.html', {'form': form})


def record_edit(request, pk):
    record = get_object_or_404(Record, pk=pk)
    if request.method == 'POST':
        form = RecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = RecordForm(instance=record)

    return render(request, 'dds/record_form.html', {'form': form})


def record_delete(request, pk):
    record = get_object_or_404(Record, pk=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('index')
    return render(request, 'dds/record_confirm_delete.html', {'record': record})


def reference_management(request):
    if request.method == 'POST':
        # Обработка форм для справочников
        if 'status_submit' in request.POST:
            status_form = StatusForm(request.POST, prefix='status')
            if status_form.is_valid():
                status_form.save()
                return redirect('reference_management')
        elif 'type_submit' in request.POST:
            type_form = TypeForm(request.POST, prefix='type')
            if type_form.is_valid():
                type_form.save()
                return redirect('reference_management')
        elif 'category_submit' in request.POST:
            category_form = CategoryForm(request.POST, prefix='category')
            if category_form.is_valid():
                category_form.save()
                return redirect('reference_management')
        elif 'subcategory_submit' in request.POST:
            subcategory_form = SubcategoryForm(request.POST, prefix='subcategory')
            if subcategory_form.is_valid():
                subcategory_form.save()
                return redirect('reference_management')
    else:
        status_form = StatusForm(prefix='status')
        type_form = TypeForm(prefix='type')
        category_form = CategoryForm(prefix='category')
        subcategory_form = SubcategoryForm(prefix='subcategory')

    # Получение всех записей справочников
    statuses = Status.objects.all()
    types = Type.objects.all()
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()

    return render(request, 'dds/reference.html', {
        'status_form': status_form,
        'type_form': type_form,
        'category_form': category_form,
        'subcategory_form': subcategory_form,
        'statuses': statuses,
        'types': types,
        'categories': categories,
        'subcategories': subcategories,
    })


def delete_status(request, pk):
    status = get_object_or_404(Status, pk=pk)
    if request.method == 'POST':
        status.delete()
        return redirect('reference_management')
    return render(request, 'dds/status_confirm_delete.html', {'status': status})


def delete_type(request, pk):
    type_ = get_object_or_404(Type, pk=pk)
    if request.method == 'POST':
        type_.delete()
        return redirect('reference_management')
    return render(request, 'dds/type_confirm_delete.html', {'type': type_})


def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('reference_management')
    return render(request, 'dds/category_confirm_delete.html', {'category': category})


def delete_subcategory(request, pk):
    subcategory = get_object_or_404(Subcategory, pk=pk)
    if request.method == 'POST':
        subcategory.delete()
        return redirect('reference_management')
    return render(request, 'dds/subcategory_confirm_delete.html', {'subcategory': subcategory})


def load_categories(request):
    type_id = request.GET.get('type')
    categories = Category.objects.filter(type_id=type_id).order_by('name')
    return render(request, 'dds/category_dropdown_list_options.html', {'categories': categories})


def load_subcategories(request):
    category_id = request.GET.get('category')
    subcategories = Subcategory.objects.filter(category_id=category_id).order_by('name')
    return render(request, 'dds/subcategory_dropdown_list_options.html', {'subcategories': subcategories})
