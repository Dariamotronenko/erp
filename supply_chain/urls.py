from django.urls import path
from . import views
from .views import (
    home,
    ЗаявкаНаПоставкуListView,
    ЗаявкаНаПоставкуDetailView,
    ЗаявкаНаПоставкуCreateView,
    ЗаявкаНаПоставкуDeleteView,
    ПоставщикListView,
    ПоставщикCreateView,
    ПоставщикUpdateView,
    ПоставщикDeleteView,
    ПеревозчикListView,
    ПеревозчикCreateView,
    ПеревозчикUpdateView,
    ПеревозчикDeleteView,
    ДоговорListView,
    ДоговорCreateView,
    ДоговорUpdateView,
    ДоговорDeleteView,
    ТранспортнаяНакладнаяListView,
    ТранспортнаяНакладнаяCreateView,
    ТранспортнаяНакладнаяUpdateView,
    ТранспортнаяНакладнаяDeleteView,
    ОтчетОДоставкеListView,
    ОтчетОДоставкеCreateView,
    ОтчетОДоставкеUpdateView,
    ОтчетОДоставкеDeleteView,
    ФинансовыйОтчетListView,
    ФинансовыйОтчетCreateView,
    ФинансовыйОтчетUpdateView,
    ФинансовыйОтчетDeleteView,
    финансовый_отчет_за_период,  # Явный импорт
)
urlpatterns = [
    #  Заявки на поставку
    path('', views.home, name='home'),
    path('заявки/', views.ЗаявкаНаПоставкуListView.as_view(), name='заявка_на_поставку_list'),
    path('заявки/<int:pk>/', views.ЗаявкаНаПоставкуDetailView.as_view(), name='заявка_на_поставку_detail'),
    path('заявки/create/', views.ЗаявкаНаПоставкуCreateView.as_view(), name='заявка_на_поставку_create'),
    path('заявки/<int:pk>/update/', views.ЗаявкаНаПоставкуDetailView.as_view(), name='заявка_на_поставку_update'),  # ИСПРАВЛЕНО
    path('заявки/<int:pk>/delete/', views.ЗаявкаНаПоставкуDeleteView.as_view(), name='заявка_на_поставку_delete'),

    #  Поставщики
    path('поставщики/', views.ПоставщикListView.as_view(), name='поставщик_list'),
    path('поставщики/create/', views.ПоставщикCreateView.as_view(), name='поставщик_create'),
    path('поставщики/<int:pk>/update/', views.ПоставщикUpdateView.as_view(), name='поставщик_update'),
    path('поставщики/<int:pk>/delete/', views.ПоставщикDeleteView.as_view(), name='поставщик_delete'),

    #  Перевозчики
    path('перевозчики/', views.ПеревозчикListView.as_view(), name='перевозчик_list'),
    path('перевозчики/create/', views.ПеревозчикCreateView.as_view(), name='перевозчик_create'),
    path('перевозчики/<int:pk>/update/', views.ПеревозчикUpdateView.as_view(), name='перевозчик_update'),
    path('перевозчики/<int:pk>/delete/', views.ПеревозчикDeleteView.as_view(), name='перевозчик_delete'),

    #  Договоры
    path('договоры/', views.ДоговорListView.as_view(), name='договор_list'),
    path('договоры/create/', views.ДоговорCreateView.as_view(), name='договор_create'),
    path('договоры/<int:pk>/update/', views.ДоговорUpdateView.as_view(), name='договор_update'),
    path('договоры/<int:pk>/delete/', views.ДоговорDeleteView.as_view(), name='договор_delete'),
    path('договоры/<int:pk>/', views.ДоговорDetailView.as_view(), name='договор_detail'), 

    #  Транспортные накладные
    path('накладные/', views.ТранспортнаяНакладнаяListView.as_view(), name='транспортная_накладная_list'),
    path('накладные/create/', views.ТранспортнаяНакладнаяCreateView.as_view(), name='транспортная_накладная_create'),
    path('накладные/<int:pk>/update/', views.ТранспортнаяНакладнаяUpdateView.as_view(), name='транспортная_накладная_update'),
    path('накладные/<int:pk>/delete/', views.ТранспортнаяНакладнаяDeleteView.as_view(), name='транспортная_накладная_delete'),

    #  Отчеты о доставке
    path('отчет/<int:pk>/', views.ОтчетОДоставкеDetailView.as_view(), name='отчет_о_доставке_detail'),
    path('отчеты/', views.ОтчетОДоставкеListView.as_view(), name='отчет_о_доставке_list'),
    path('отчеты/create/', views.ОтчетОДоставкеCreateView.as_view(), name='отчет_о_доставке_create'),
    path('отчеты/<int:pk>/update/', views.ОтчетОДоставкеUpdateView.as_view(), name='отчет_о_доставке_update'),
    path('отчеты/создать/<int:заказ_id>/', views.ОтчетОДоставкеCreateView.as_view(), name='отчет_о_доставке_form'),
    path('отчеты/<int:pk>/delete/', views.ОтчетОДоставкеDeleteView.as_view(), name='отчет_о_доставке_confirm_delete'),
    

    #  Финансовые отчеты
    path('фин_отчеты/', views.ФинансовыйОтчетListView.as_view(), name='финансовый_отчет_list'),
    path('фин_отчеты/create/', views.ФинансовыйОтчетCreateView.as_view(), name='финансовый_отчет_create'),
    path('фин_отчеты/<int:pk>/update/', views.ФинансовыйОтчетUpdateView.as_view(), name='финансовый_отчет_update'),
    path('фин_отчеты/<int:pk>/delete/', views.ФинансовыйОтчетDeleteView.as_view(), name='финансовый_отчет_delete'),
    path('фин_отчеты/period/', финансовый_отчет_за_период, name='финансовый_отчет_период'),
    path('generate_ttn/', views.generate_ttn_document, name='generate_ttn'),
    path('поставщики/create-ajax/', views.поставщик_create_ajax, name='поставщик_create_ajax'),
    path('get-carrier-data/', views.get_carrier_data, name='get_carrier_data'),
]