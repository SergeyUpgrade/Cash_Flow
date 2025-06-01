from django.db import models
from django.core.exceptions import ValidationError


class Status(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"


class Type(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    type = models.ForeignKey(Type, on_delete=models.CASCADE, verbose_name="Тип")

    def __str__(self):
        return f"{self.name} ({self.type})"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        unique_together = ('name', 'type')


class Subcategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")

    def __str__(self):
        return f"{self.name} ({self.category})"

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        unique_together = ('name', 'category')


class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    date = models.DateField(verbose_name="Дата")
    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name="Статус")
    type = models.ForeignKey(Type, on_delete=models.PROTECT, verbose_name="Тип")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категория")
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT, verbose_name="Подкатегория")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Сумма")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")

    def clean(self):
        # Проверка, что подкатегория принадлежит выбранной категории
        if self.subcategory.category != self.category:
            raise ValidationError("Выбранная подкатегория не принадлежит выбранной категории")

        # Проверка, что категория принадлежит выбранному типу
        if self.category.type != self.type:
            raise ValidationError("Выбранная категория не принадлежит выбранному типу")

    def __str__(self):
        return f"{self.date} - {self.type} {self.amount}р. ({self.category}:{self.subcategory})"

    class Meta:
        verbose_name = "Запись ДДС"
        verbose_name_plural = "Записи ДДС"
        ordering = ['-date', '-created_at']
