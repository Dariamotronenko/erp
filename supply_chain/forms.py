from django import forms
from .models import (
    ЗаявкаНаПоставку,
    Поставщик,
    Перевозчик,
    Договор,
    ТранспортнаяНакладная,
    ОтчетОДоставке,
    ФинансовыйОтчет,
)
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date


class ЗаявкаНаПоставкуForm(forms.ModelForm):
    """Форма для создания и редактирования заявки на поставку"""
    
    class Meta:
        model = ЗаявкаНаПоставку
        exclude = ['номер']  
        
        widgets = {
            'дата_создания': forms.DateInput(attrs={'type': 'date'}),
            'срок_поставки': forms.DateInput(attrs={'type': 'date'}),
            'комментарий': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Для новой заявки устанавливаем текущую дату по умолчанию
        if not self.instance.pk:
            self.initial['дата_создания'] = timezone.now().date()
class ПоставщикForm(forms.ModelForm):
    """Форма для создания и редактирования поставщика"""
    
    class Meta:
        model = Поставщик
        fields = [
            "название",
            "контактное_лицо",
            "телефон",
            "email",
            "адрес",
            "условия_поставки",
            "реквизиты",
        ]
        widgets = {
            "адрес": forms.Textarea(attrs={"rows": 3}),
            "условия_поставки": forms.Textarea(attrs={"rows": 3}),
            "реквизиты": forms.Textarea(attrs={"rows": 4}),
        }
class ПеревозчикForm(forms.ModelForm):
    """Форма для создания и редактирования перевозчика"""
    
    class Meta:
        model = Перевозчик
        fields = [
            "название",
            "контактное_лицо",
            "телефон",
            "email",
            "транспортное_средство",
            "марка_автомобиля",
            "гос_номер",
            "водитель_фио",
            "водитель_удостоверение",
            "лицензия_номер",
            "лицензия_срок",
        ]
        widgets = {
            "лицензия_срок": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),
        }

class ДоговорForm(forms.ModelForm):
    class Meta:
        model = Договор
        fields = ['номер', 'дата_заключения', 'поставщик', 'заявка', 
                 'условия_оплаты', 'условия_поставки', 'срок_действия', 'файл']
        widgets = {
            'дата_заключения': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'required': 'required'
                },
                format='%Y-%m-%d'
            ),
            'срок_действия': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'required': 'required'
                },
                format='%Y-%m-%d'
            ),
            'условия_оплаты': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'условия_поставки': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'файл': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
        labels = {
            'файл': 'Скан договора (PDF)',
        }
        help_texts = {
            'срок_действия': 'Дата окончания действия договора',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Оптимизация queryset для поставщиков
        self.fields['поставщик'].queryset = Поставщик.objects.only('id', 'название')
        
        # Установка текущей даты по умолчанию для новой заявки
        if not self.instance.pk:
            self.initial['дата_заключения'] = date.today().strftime('%Y-%m-%d')
        
        # Добавление CSS классов для полей
        self.fields['номер'].widget.attrs.update({'class': 'form-control'})
        self.fields['поставщик'].widget.attrs.update({'class': 'form-control'})
        self.fields['заявка'].widget.attrs.update({'class': 'form-control'})
    
    def clean(self):
        cleaned_data = super().clean()
        дата_заключения = cleaned_data.get('дата_заключения')
        срок_действия = cleaned_data.get('срок_действия')
        
        # Валидация дат
        if дата_заключения and срок_действия:
            if срок_действия < дата_заключения:
                self.add_error(
                    'срок_действия',
                    'Срок действия не может быть раньше даты заключения'
                )
        
        return cleaned_data

class ТранспортнаяНакладнаяForm(forms.ModelForm):
    """Форма для создания и редактирования транспортной накладной"""
    
    # Добавляем дополнительные поля для автомобиля, если их нет в модели
    автомобиль_марка = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly'
        }),
        label="Марка автомобиля"
    )
    
    автомобиль_гос_номер = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly'
        }),
        label="Гос. номер автомобиля"
    )

    class Meta:
        model = ТранспортнаяНакладная
        fields = [
            "номер",
            "грузоотправитель",
            "грузополучатель",
            "плательщик",
            "код_продукции",
            "наименование",
            "единица_измерения",
            "вид_упаковки",
            "количество_мест",
            "масса_брутто",
            "масса_нетто",
            "цена",
            "сумма",
            "перевозчик",
            "водитель_фио",
            "пункт_погрузки",
            "пункт_разгрузки",
            "срок_доставки",
            "статус",
            "дата_отправки",
            "дата_доставки",
            "транспортное_средство",
            "тип_груза",
            "платежные_реквизиты",
            "комментарий",
        ]
        widgets = {
            "дата_отправки": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),
            "срок_доставки": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),
            "дата_доставки": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),
            "комментарий": forms.Textarea(attrs={
                "rows": 3,
                "class": "form-control"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Если экземпляр модели связан с перевозчиком, заполняем данные авто
        if self.instance and self.instance.перевозчик:
            self.fields['автомобиль_марка'].initial = self.instance.перевозчик.марка_автомобиля
            self.fields['автомобиль_гос_номер'].initial = self.instance.перевозчик.гос_номер

class ОтчетОДоставкеForm(forms.ModelForm):
    """Форма для создания и редактирования отчета о доставке"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Устанавливаем текущее время по умолчанию для даты прибытия
        if not self.instance.pk:
            self.fields['дата_прибытия'].initial = timezone.now()
        
        # Оптимизация выпадающих списков
        self.fields['транспортная_накладная'].queryset = self.fields['транспортная_накладная'].queryset.only(
            'id', 'номер'
        ).order_by('-id')
        
        self.fields['водитель'].queryset = self.fields['водитель'].queryset.order_by('фио')
        self.fields['транспортное_средство'].queryset = self.fields['транспортное_средство'].queryset.order_by('гос_номер')

    class Meta:
        model = ОтчетОДоставке
        fields = [
            "транспортная_накладная",
            "дата_прибытия",
            "дата_убытия",
            "пробег",
            "время_в_пути",
            "водитель",
            "транспортное_средство",
            "статус",
            "примечание",
            "подтверждение_получателя",
            "фото_документов",
        ]
        widgets = {
            "транспортная_накладная": forms.Select(attrs={
                "class": "form-select",
                "data-live-search": "true"
            }),
            "дата_прибытия": forms.DateTimeInput(attrs={
                "type": "datetime-local",
                "class": "form-control datetimepicker",
            }),
            "дата_убытия": forms.DateTimeInput(attrs={
                "type": "datetime-local",
                "class": "form-control datetimepicker",
            }),
            "пробег": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "0",
                "step": "0.01"
            }),
            "время_в_пути": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "ЧЧ:ММ:СС"
            }),
            "водитель": forms.Select(attrs={
                "class": "form-select",
                "data-live-search": "true"
            }),
            "транспортное_средство": forms.Select(attrs={
                "class": "form-select",
                "data-live-search": "true"
            }),
            "статус": forms.Select(attrs={"class": "form-select"}),
            "примечание": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Дополнительная информация о доставке..."
            }),
            "подтверждение_получателя": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
            "фото_документов": forms.FileInput(attrs={
                "class": "form-control",
                "accept": "image/*"
            })
        }
        help_texts = {
            "время_в_пути": "Формат: ЧЧ:ММ:СС (например: 02:30:00)",
            "фото_документов": "Загрузите фото подписанных документов или груза",
        }
        labels = {
            "подтверждение_получателя": "Получатель подтвердил доставку",
        }

    def clean(self):
        cleaned_data = super().clean()
        дата_прибытия = cleaned_data.get('дата_прибытия')
        дата_убытия = cleaned_data.get('дата_убытия')
        пробег = cleaned_data.get('пробег')

        # Проверка дат
        if дата_убытия and дата_прибытия and дата_убытия < дата_прибытия:
            self.add_error(
                'дата_убытия',
                'Дата убытия не может быть раньше даты прибытия'
            )

        # Проверка пробега
        if пробег is not None and пробег < 0:
            self.add_error(
                'пробег',
                'Пробег не может быть отрицательным'
            )

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Автоматический расчет средней скорости
        if instance.пробег and instance.время_в_пути:
            hours = instance.время_в_пути.total_seconds() / 3600
            if hours > 0:
                instance.средняя_скорость = float(instance.пробег) / hours

        if commit:
            instance.save()
            self.save_m2m()

        return instance

    
class ФинансовыйОтчетForm(forms.ModelForm):
    """Форма для создания и редактирования финансового отчета"""

    class Meta:
        model = ФинансовыйОтчет
        fields = [
            'период_начала',
            'период_окончания',
            'доходы',
            'расходы',
            # 'прибыль',  # Прибыль рассчитывается автоматически, не нужно в форме
            'комментарий',
            'файл',
        ]
        widgets = {
            'период_начала': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control'
            }),
            'период_окончания': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control'
            }),
            'доходы': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'расходы': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'комментарий': forms.Textarea(attrs={
                'rows': 3, 
                'class': 'form-control'
            }),
            'файл': forms.FileInput(attrs={
                'class': 'form-control-file'
            }),
        }
from django import forms


class ФинансовыйОтчетПериодForm(forms.Form):
    """Форма для фильтрации финансовых отчетов по периоду"""

    период_начала = forms.DateField(
        label="Период с",
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )

    период_окончания = forms.DateField(
        label="Период по",
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
