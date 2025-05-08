from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.contrib.auth import get_user_model


class Status(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Type(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='subcategory',
                               verbose_name='Родительская категория')
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='category', verbose_name='Тип')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    
class Note(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='notes',
        verbose_name='Пользователь')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='notes', verbose_name='Статус')
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='notes', verbose_name='Тип')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='notes', verbose_name='Категория')
    total_sum = models.DecimalField(max_digits=12, decimal_places=2,validators=[MinValueValidator(0.0)], 
                                    verbose_name="Сумма")
    comment = models.TextField(max_length=300, null=True, blank=True, verbose_name='Комментарий')
    created_at = models.DateField(blank=True, default=timezone.now)
    
    def __str__(self):
        return f'{self.category} - {self.total_sum}'
    
    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        