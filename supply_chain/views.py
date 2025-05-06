from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import *
from .forms import *
from django.db.models import Sum, Q
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin  # Для защиты View (если нужна авторизация)
from django.urls import reverse_lazy
from .forms import (
    ЗаявкаНаПоставкуForm,
    ПоставщикForm,
    ПеревозчикForm,
    ДоговорForm,
    ТранспортнаяНакладнаяForm,
    ОтчетОДоставкеForm,
    ФинансовыйОтчетForm,
    ФинансовыйОтчетПериодForm,
)
from django.shortcuts import render
from .forms import ФинансовыйОтчетПериодForm
from .models import ФинансовыйОтчет
from django.db.models import Sum
from django.http import HttpResponse
from django.template.loader import get_template
from django.views.generic.edit import CreateView
from xhtml2pdf import pisa
from io import BytesIO
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json



def home(request):
    """
    View для отображения главной страницы.

    Args:
        request: Объект HttpRequest.

    Returns:
        HttpResponse: Ответ с отображенным HTML-шаблоном.
    """

    data = {
        'title': 'Главная страница',
        'content': 'Добро пожаловать в систему управления поставками!',
        'additional_info': 'Здесь может быть дополнительная информация или статистика.'
    }
    return render(request, 'supply_chain/home.html', data)
class ЗаявкаНаПоставкуListView(LoginRequiredMixin, ListView):
    model = ЗаявкаНаПоставку
    template_name = 'supply_chain/заявка_на_поставку_list.html'  #  ВАШЕ НАЗВАНИЕ
    context_object_name = 'заявки'
    paginate_by = 10
    ordering = ['дата_создания']  #  По умолчанию сортируем по дате создания

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.GET.get('search')
        if search_term:
            queryset = queryset.filter(
                Q(номер__icontains=search_term) | Q(клиент__icontains=search_term)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_term'] = self.request.GET.get('search', '')
        return context


class ЗаявкаНаПоставкуDetailView(LoginRequiredMixin, DetailView, UpdateView):
    model = ЗаявкаНаПоставку
    form_class = ЗаявкаНаПоставкуForm
    template_name = 'supply_chain/заявка_на_поставку_detail.html'  #  ВАШЕ НАЗВАНИЕ
    context_object_name = 'заявка'
    success_url = reverse_lazy('заявка_на_поставку_list')  #  Куда перенаправлять после успешного редактирования

    def form_valid(self, form):
        messages.success(self.request, 'Заявка успешно обновлена.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)


class ЗаявкаНаПоставкуCreateView(CreateView):
    model = ЗаявкаНаПоставку
    form_class = ЗаявкаНаПоставкуForm
    template_name = 'supply_chain/заявка_на_поставку_form.html'
    success_url = reverse_lazy('заявка_на_поставку_list')
    
    def form_valid(self, form):
        last_order = ЗаявкаНаПоставку.objects.order_by('-номер').first()
        form.instance.номер = (last_order.номер + 1) if last_order else 1
        return super().form_valid(form)

class ЗаявкаНаПоставкуUpdateView(UpdateView):
    model = ЗаявкаНаПоставку
    form_class = ЗаявкаНаПоставкуForm
    template_name = 'supply_chain/заявка_на_поставку_form.html'
    success_url = reverse_lazy('заявка_на_поставку_list')
class ЗаявкаНаПоставкуDeleteView(LoginRequiredMixin, DeleteView):
    model = ЗаявкаНаПоставку
    template_name = 'supply_chain/заявка_на_поставку_confirm_delete.html'  #  ВАШЕ НАЗВАНИЕ
    success_url = reverse_lazy('заявка_на_поставку_list')
    context_object_name = 'заявка'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Заявка успешно удалена.')
        return super().delete(request, *args, **kwargs)


class ПоставщикListView(LoginRequiredMixin, ListView):
    model = Поставщик
    template_name = 'supply_chain/поставщик_list.html'  #  ВАШЕ НАЗВАНИЕ
    context_object_name = 'поставщики'
    paginate_by = 10


class ПоставщикCreateView(LoginRequiredMixin, CreateView):
    model = Поставщик
    form_class = ПоставщикForm
    template_name = 'supply_chain/поставщик_form.html'  #  ВАШЕ НАЗВАНИЕ
    success_url = reverse_lazy('поставщик_list')

    def form_valid(self, form):
        messages.success(self.request, 'Поставщик успешно создан.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)


class ПоставщикUpdateView(LoginRequiredMixin, UpdateView):
    model = Поставщик
    form_class = ПоставщикForm
    template_name = 'supply_chain/поставщик_form.html'  #  ВАШЕ НАЗВАНИЕ
    success_url = reverse_lazy('поставщик_list')

    def form_valid(self, form):
        messages.success(self.request, 'Поставщик успешно обновлен.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)


class ПоставщикDeleteView(LoginRequiredMixin, DeleteView):
    model = Поставщик
    template_name = 'supply_chain/поставщик_confirm_delete.html'  #  ВАШЕ НАЗВАНИЕ
    success_url = reverse_lazy('поставщик_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Поставщик успешно удален.')
        return super().delete(request, *args, **kwargs)


class ПеревозчикListView(LoginRequiredMixin, ListView):
    model = Перевозчик
    template_name = 'supply_chain/перевозчик_list.html'  #  ВАШЕ НАЗВАНИЕ
    context_object_name = 'перевозчики'
    paginate_by = 10


class ПеревозчикCreateView(LoginRequiredMixin, CreateView):
    model = Перевозчик
    form_class = ПеревозчикForm
    template_name = 'supply_chain/перевозчик_form.html'  #  ВАШЕ НАЗВАНИЕ
    success_url = reverse_lazy('перевозчик_list')

    def form_valid(self, form):
        messages.success(self.request, 'Перевозчик успешно создан.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)


class ПеревозчикUpdateView(LoginRequiredMixin, UpdateView):
    model = Перевозчик
    form_class = ПеревозчикForm
    template_name = 'supply_chain/перевозчик_form.html'  #  ВАШЕ НАЗВАНИЕ
    success_url = reverse_lazy('перевозчик_list')

    def form_valid(self, form):
        messages.success(self.request, 'Перевозчик успешно обновлен.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)


class ПеревозчикDeleteView(LoginRequiredMixin, DeleteView):
    model = Перевозчик
    template_name = 'supply_chain/перевозчик_confirm_delete.html'  #  ВАШЕ НАЗВАНИЕ
    success_url = reverse_lazy('перевозчик_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Перевозчик успешно удален.')
        return super().delete(request, *args, **kwargs)


class ДоговорListView(LoginRequiredMixin, ListView):
    model = Договор
    template_name = 'supply_chain/договор_list.html'  #  ВАШЕ НАЗВАНИЕ
    context_object_name = 'договоры'
    paginate_by = 10


class ДоговорCreateView(LoginRequiredMixin, CreateView):
    model = Договор
    form_class = ДоговорForm
    template_name = 'supply_chain/договор_form.html'
    success_url = reverse_lazy('договор_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {
            'дата_заключения': timezone.now().date()
        }
        return kwargs
    
    def form_valid(self, form):
        form.instance.автор = self.request.user
        messages.success(self.request, 'Договор успешно создан.')
        return super().form_valid(form)

class ДоговорUpdateView(LoginRequiredMixin, UpdateView):
    model = Договор
    form_class = ДоговорForm
    template_name = 'supply_chain/договор_form.html'  #  ВАШЕ НАЗВАНИЕ
    success_url = reverse_lazy('договор_list')

    def form_valid(self, form):
        messages.success(self.request, 'Договор успешно обновлен.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)


class ДоговорDeleteView(LoginRequiredMixin, DeleteView):
    model = Договор
    template_name = 'supply_chain/договор_confirm_delete.html'  #  ВАШЕ НАЗВАНИЕ
    success_url = reverse_lazy('договор_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Договор успешно удален.')
        return super().delete(request, *args, **kwargs)


class ТранспортнаяНакладнаяListView(LoginRequiredMixin, ListView):
    model = ТранспортнаяНакладная
    template_name = 'supply_chain/транспортная_накладная_list.html'  #  ВАШЕ НАЗВАНИЕ
    context_object_name = 'накладные'
    paginate_by = 10

class ТранспортнаяНакладнаяCreateView(LoginRequiredMixin, CreateView):
    model = ТранспортнаяНакладная
    form_class = ТранспортнаяНакладнаяForm
    template_name = 'supply_chain/транспортная_накладная_form.html'

    def form_valid(self, form):
        # Сохраняем накладную
        self.object = form.save()
        
        # Подготавливаем данные для PDF
        context = {
            'data': {
                'номер_накладной': self.object.номер,
                'дата_составления': self.object.дата_составления.strftime('%d.%m.%Y'),
                'код_продукции': self.object.код_продукции or '-',
                'наименование_товара': self.object.наименование or '-',
                'единица_измерения': self.object.единица_измерения or '-',
                'количество': self.object.количество_мест or '-',
                'цена': f"{self.object.цена:.2f}" if self.object.цена else '-',
                'сумма': f"{self.object.сумма:.2f}" if self.object.сумма else '-',
                'общая_сумма': f"{self.object.сумма:.2f}" if self.object.сумма else '-',
                'грузоотправитель': self.object.грузоотправитель,
                'грузополучатель': self.object.грузополучатель,
                'перевозчик': self.object.перевозчик or '-',
                'автомобиль': f"{self.object.автомобиль_марка or ''} {self.object.автомобиль_гос_номер or ''}".strip() or '-',
                'водитель': self.object.водитель_фио,
                'отпуск_разрешил': self.request.user.get_full_name() or self.request.user.username,
                'главный_бухгалтер': 'Иванова И.И.',
                'отпуск_груза_произвел': 'Петров П.П.',
                'пункт_погрузки': self.object.пункт_погрузки or '-',
                'пункт_разгрузки': self.object.пункт_разгрузки or '-',
                'срок_доставки': self.object.срок_доставки.strftime('%d.%m.%Y') if self.object.срок_доставки else '-',
            }
        }

        # Рендерим HTML шаблон
        template = get_template('supply_chain/ttn_template.html')
        html = template.render(context)
        
        # Создаем PDF
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
        
        if not pdf.err:
            response = HttpResponse(
                result.getvalue(), 
                content_type='application/pdf'
            )
            # Используем timezone.now() вместо datetime.now() для Django
            response['Content-Disposition'] = f'attachment; filename="TTN_{self.object.номер}_{timezone.now().strftime("%Y%m%d")}.pdf"'
            return response
        
        # Если ошибка генерации PDF
        return super().form_valid(form)
class ТранспортнаяНакладнаяUpdateView(LoginRequiredMixin, UpdateView):
    model = ТранспортнаяНакладная
    form_class = ТранспортнаяНакладнаяForm
    template_name = 'supply_chain/транспортная_накладная_form.html'  #  ВАШЕ НАЗВАНИЕ
    success_url = reverse_lazy('транспортная_накладная_list')

    def form_valid(self, form):
        messages.success(self.request, 'Транспортная накладная успешно обновлена.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)


class ТранспортнаяНакладнаяDeleteView(LoginRequiredMixin, DeleteView):
    model = ТранспортнаяНакладная
    template_name = 'supply_chain/транспортная_накладная_confirm_delete.html'  #  ВАШЕ НАЗВАНИЕ
    success_url = reverse_lazy('транспортная_накладная_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Транспортная накладная успешно удалена.')
        return super().delete(request, *args, **kwargs)


class ОтчетОДоставкеListView(LoginRequiredMixin, ListView):
    model = ОтчетОДоставке
    template_name = 'supply_chain/отчет_о_доставке_list.html'  #  ВАШЕ НАЗВАНИЕ
    context_object_name = 'отчеты'
    paginate_by = 10


class ОтчетОДоставкеCreateView(LoginRequiredMixin, CreateView):
    model = ОтчетОДоставке
    form_class = ОтчетОДоставкеForm
    template_name = 'supply_chain/отчет_о_доставке_form.html'  #  ВАШЕ НАЗВАНИЕ
    success_url = reverse_lazy('отчет_о_доставке_list')

    def form_valid(self, form):
        messages.success(self.request, 'Отчет о доставке успешно создан.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)


class ОтчетОДоставкеUpdateView(LoginRequiredMixin, UpdateView):
    model = ОтчетОДоставке
    form_class = ОтчетОДоставкеForm
    template_name = 'supply_chain/отчет_о_доставке_form.html'  #  ВАШЕ НАЗВАНИЕ
    success_url = reverse_lazy('отчет_о_доставке_list')

    def form_valid(self, form):
        messages.success(self.request, 'Отчет о доставке успешно обновлен.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)


class ОтчетОДоставкеDeleteView(LoginRequiredMixin, DeleteView):
    model = ОтчетОДоставке
    template_name = 'supply_chain/отчет_о_доставке_confirm_delete.html'  #  ВАШЕ НАЗВАНИЕ
    success_url = reverse_lazy('отчет_о_доставке_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Отчет о доставке успешно удален.')
        return super().delete(request, *args, **kwargs)


class ФинансовыйОтчетListView(LoginRequiredMixin, ListView):
    model = ФинансовыйОтчет
    template_name = 'supply_chain/финансовый_отчет_list.html'  #  ВАШЕ НАЗВАНИЕ
    context_object_name = 'отчеты'
    paginate_by = 10


class ФинансовыйОтчетCreateView(LoginRequiredMixin, CreateView):
    model = ФинансовыйОтчет
    form_class = ФинансовыйОтчетForm
    template_name = 'supply_chain/финансовый_отчет_form.html'  #  ВАШЕ НАЗВАНИЕ
    success_url = reverse_lazy('финансовый_отчет_list')

    def form_valid(self, form):
        messages.success(self.request, 'Финансовый отчет успешно создан.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)


class ФинансовыйОтчетUpdateView(LoginRequiredMixin, UpdateView):
    model = ФинансовыйОтчет
    form_class = ФинансовыйОтчетForm
    template_name = 'supply_chain/финансовый_отчет_form.html'  #  ВАШЕ НАЗВАНИЕ
    success_url = reverse_lazy('финансовый_отчет_list')

    def form_valid(self, form):
        messages.success(self.request, 'Финансовый отчет успешно обновлен.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)
    

class ФинансовыйОтчетDeleteView(LoginRequiredMixin, DeleteView):
    model = ФинансовыйОтчет
    template_name = 'supply_chain/финансовый_отчет_confirm_delete.html'  #  Обязательно создайте этот шаблон
    success_url = reverse_lazy('финансовый_отчет_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Финансовый отчет успешно удален.')
        return super().delete(request, *args, **kwargs)

def финансовый_отчет_за_период(request):
    """
    View для отображения финансового отчета за выбранный период.
    """
    итоги = None
    if request.method == 'POST':
        form = ФинансовыйОтчетПериодForm(request.POST)
        if form.is_valid():
            начало_периода = form.cleaned_data['начало_периода']
            конец_периода = form.cleaned_data['конец_периода']
            отчеты = ФинансовыйОтчет.objects.filter(дата_создания__gte=начало_периода, дата_создания__lte=конец_периода)
            итоги = отчеты.aggregate(
                общая_сумма_доходов=Sum('сумма_доходов'),
                общая_сумма_расходов=Sum('сумма_расходов'),
                общая_прибыль=Sum('сумма_доходов') - Sum('сумма_расходов')
            )
    else:
        form = ФинансовыйОтчетПериодForm()

    context = {
        'form': form,
        'итоги': итоги,
    }
    return render(request, 'supply_chain/финансовый_отчет_form.html', context)


def generate_ttn_document(request):
    # 1. Получение данных 
    data = {
        'номер_накладной': '12345',
        'дата_составления': datetime.date.today(),
        'грузоотправитель': 'ООО Рога и Копыта',
        'грузополучатель': 'ООО Транзит',
        # ... и другие данные из вашей модели ТранспортнаяНакладная
    }

    # 2. Загрузка HTML-шаблона
    template = get_template('supply_chain/ttn_template.html')  # Убедитесь, что шаблон существует
    html = template.render(data)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse("Ошибка генерации PDF", status=400)

    return response

@csrf_exempt
def поставщик_create_ajax(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            поставщик = Поставщик.objects.create(
                название=data.get('название'),
                контактное_лицо=data.get('контактное_лицо')
            )
            return JsonResponse({
                'success': True,
                'supplier_id': поставщик.id,
                'supplier_name': поставщик.название
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    return JsonResponse({'success': False}, status=405)

from django.http import JsonResponse
from .models import Перевозчик, Водитель, ТранспортноеСредство

def get_carrier_data(request):
    carrier_id = request.GET.get('carrier_id')
    try:
        carrier = Перевозчик.objects.get(pk=carrier_id)
        
        # Получаем первого водителя и транспортное средство перевозчика
        driver = Водитель.objects.filter(перевозчик=carrier).first()
        vehicle = ТранспортноеСредство.objects.filter(перевозчик=carrier).first()
        
        return JsonResponse({
            'success': True,
            'driver_id': driver.id if driver else None,
            'vehicle_id': vehicle.id if vehicle else None,
            'driver_name': str(driver) if driver else '',
            'vehicle_info': str(vehicle) if vehicle else ''
        })
    except (Перевозчик.DoesNotExist, ValueError):
        return JsonResponse({'success': False})