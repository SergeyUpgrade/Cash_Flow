from django.db import migrations


def load_initial_data(apps, schema_editor):
    Status = apps.get_model('dds', 'Status')
    Type = apps.get_model('dds', 'Type')
    Category = apps.get_model('dds', 'Category')
    Subcategory = apps.get_model('dds', 'Subcategory')

    # Создаем статусы
    Status.objects.bulk_create([
        Status(name="Бизнес"),
        Status(name="Личное"),
        Status(name="Налог"),
    ])

    # Создаем типы
    Type.objects.bulk_create([
        Type(name="Пополнение"),
        Type(name="Списание"),
    ])

    # Получаем созданные типы
    income_type = Type.objects.get(name="Пополнение")
    expense_type = Type.objects.get(name="Списание")

    # Создаем категории
    Category.objects.bulk_create([
        Category(name="Доходы", type=income_type),
        Category(name="Инфраструктура", type=expense_type),
    ])

    # Получаем категории
    income_category = Category.objects.get(name="Доходы")
    infra_category = Category.objects.get(name="Инфраструктура")

    # Создаем подкатегории
    Subcategory.objects.bulk_create([
        Subcategory(name="Зарплата", category=income_category),
        Subcategory(name="VPS", category=infra_category),
    ])


class Migration(migrations.Migration):
    dependencies = [
        ('dds', 'последняя_миграция'),  # Укажите последнюю миграцию
    ]

    operations = [
        migrations.RunPython(load_initial_data),
    ]
