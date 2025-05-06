from django.db import models
from django.core.validators import MinValueValidator
from datetime import date

class Водитель(models.Model):
    фио = models.CharField(max_length=100, verbose_name="ФИО водителя")
    права = models.CharField(max_length=20, verbose_name="Номер водительского удостоверения")
    
    class Meta:
        verbose_name = "Водитель"
        verbose_name_plural = "Водители"
    
    def __str__(self):
        return self.фио
class ТранспортноеСредство(models.Model):
    гос_номер = models.CharField(max_length=20, unique=True, verbose_name="Гос. номер")
    марка = models.CharField(max_length=50, verbose_name="Марка автомобиля")
    # Другие поля транспортного средства
    class Meta:
        verbose_name = "Транспортное средство"
        verbose_name_plural = "Транспортные средства"

    def __str__(self):
        return self.гос_номер

class Поставщик(models.Model):
    """Модель поставщика товаров"""
    название = models.CharField(max_length=100, verbose_name="Название поставщика")
    контактное_лицо = models.CharField(max_length=100, verbose_name="Контактное лицо")
    телефон = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email", blank=True, null=True)
    адрес = models.TextField(verbose_name="Юридический адрес")
    условия_поставки = models.TextField(verbose_name="Условия поставки")
    реквизиты = models.TextField(verbose_name="Банковские реквизиты", blank=True, null=True)

    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"
        ordering = ['название']

    def __str__(self):
        return self.название


class Перевозчик(models.Model):
    """Модель транспортной компании/перевозчика"""
    название = models.CharField(max_length=100, verbose_name="Название компании")
    контактное_лицо = models.CharField(max_length=100, verbose_name="Контактное лицо")
    телефон = models.CharField(max_length=20, verbose_name="Контактный телефон")
    email = models.EmailField(verbose_name="Email", blank=True, null=True)

    # Транспортные данные
    транспортное_средство = models.CharField(max_length=100, verbose_name="Тип транспорта")
    марка_автомобиля = models.CharField(max_length=50, verbose_name="Марка автомобиля")
    гос_номер = models.CharField(max_length=20, verbose_name="Гос. номер")

    # Данные водителя
    водитель_фио = models.CharField(max_length=100, verbose_name="ФИО водителя")
    водитель_удостоверение = models.CharField(max_length=50, verbose_name="Номер в/у")

    # Лицензии
    лицензия_номер = models.CharField(max_length=50, verbose_name="Номер лицензии")
    лицензия_срок = models.DateField(verbose_name="Срок действия лицензии")
    
    class Meta:
        verbose_name = "Перевозчик"
        verbose_name_plural = "Перевозчики"
        ordering = ['название']

    def __str__(self):
        return f"{self.название} ({self.гос_номер})"



from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class ЗаявкаНаПоставку(models.Model):
    """Модель заявки на поставку товаров с расширенной функциональностью"""
    
    class Статус(models.TextChoices):
        NEW = 'new', _('Новая')
        PROCESSING = 'processing', _('В обработке')
        DELIVERY = 'delivery', _('Доставляется')
        COMPLETED = 'completed', _('Завершена')
        CANCELED = 'canceled', _('Отменена')
    
    номер = models.PositiveIntegerField(
        verbose_name=_("Номер заявки"),
        unique=True,
        blank=True,  # Разрешаем пустое значение
        null=True,   # Разрешаем NULL в базе данных
        help_text="Уникальный номер заявки (генерируется автоматически)"
    )
    
    дата_создания = models.DateField(
        verbose_name=_("Дата создания"),
        default=timezone.now,
        help_text=_("Дата оформления заявки")
    )
    
    # Контрагенты
    клиент = models.CharField(
        verbose_name=_("Клиент"),
        max_length=100,
        help_text=_("Наименование клиента")
    )
    плательщик = models.TextField(
        verbose_name=_("Плательщик"),
        help_text=_("Реквизиты плательщика")
    )
    
    # Адреса
    адрес_отправки = models.TextField(
        verbose_name=_("Адрес отправки"),
        help_text=_("Полный адрес места отправки товара")
    )
    
    адрес_доставки = models.TextField(
        verbose_name=_("Адрес доставки"),
        help_text=_("Полный адрес места доставки товара")
    )
    
    # Товарные данные
    товар = models.CharField(
        verbose_name=_("Наименование товара"),
        max_length=100,
        help_text=_("Наименование поставляемого товара")
    )
    
    количество = models.PositiveIntegerField(
        verbose_name=_("Количество"),
        validators=[MinValueValidator(1)],
        help_text=_("Количество товара в единицах измерения")
    )
    
    срок_поставки = models.DateField(
        verbose_name=_("Срок поставки"),
        help_text=_("Планируемая дата поставки")
    )
    
    # Статус
    статус = models.CharField(
        verbose_name=_("Статус заявки"),
        max_length=20,
        choices=Статус.choices,
        default=Статус.NEW,
        help_text=_("Текущий статус заявки")
    )
    
    комментарий = models.TextField(
        verbose_name=_("Комментарий"),
        blank=True,
        null=True,
        help_text=_("Дополнительная информация по заявке")
    )
    
    дата_изменения = models.DateTimeField(
        verbose_name=_("Дата последнего изменения"),
        auto_now=True,
        help_text=_("Дата и время последнего обновления заявки")
    )

    class Meta:
        verbose_name = _("Заявка на поставку")
        verbose_name_plural = _("Заявки на поставку")
        ordering = ['-дата_создания', '-номер']
        indexes = [
            models.Index(fields=['номер']),
            models.Index(fields=['статус']),
            models.Index(fields=['дата_создания']),
            models.Index(fields=['срок_поставки']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(срок_поставки__gte=models.F('дата_создания')),
                name='check_delivery_date'
            )
        ]

    def __str__(self):
        return _("Заявка №{number} от {date} ({status})").format(
            number=self.номер,
            date=self.дата_создания.strftime('%d.%m.%Y'),
            status=self.get_статус_display()
        )

    def save(self, *args, **kwargs):
        if not self.номер:
            # Автоматическая генерация номера заявки
            last_order = ЗаявкаНаПоставку.objects.order_by('-номер').first()
            self.номер = (last_order.номер + 1) if last_order else 1
        super().save(*args, **kwargs)


class Договор(models.Model):
    """Модель договора на поставку"""
    номер = models.CharField(max_length=50, unique=True, verbose_name="Номер договора")
    дата_заключения = models.DateField(
        verbose_name="Дата заключения",
        default=date.today,  # Устанавливаем текущую дату по умолчанию
        help_text="Дата подписания договора"
    )
    
    # Связи
    поставщик = models.ForeignKey(
        Поставщик, 
        on_delete=models.PROTECT,
        verbose_name="Поставщик"
    )
    заявка = models.ForeignKey(
        ЗаявкаНаПоставку,
        on_delete=models.PROTECT,
        verbose_name="Заявка на поставку"
    )
    
    # Условия
    условия_оплаты = models.TextField(verbose_name="Условия оплаты")
    условия_поставки = models.TextField(verbose_name="Условия поставки")
    срок_действия = models.DateField(verbose_name="Срок действия договора")
    файл = models.FileField(
        upload_to='contracts/',
        verbose_name="Скан договора",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Договор"
        verbose_name_plural = "Договоры"
        ordering = ['-дата_заключения']

    def __str__(self):
        return f"Договор №{self.номер} от {self.дата_заключения}"

class ТранспортнаяНакладная(models.Model):
    """Модель товарно-транспортной накладной (ТТН)"""
    
    номер = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name="Номер ТТН"
    )
    дата_составления = models.DateField(
        auto_now_add=True,
        verbose_name="Дата составления"
    )
    
    # Контрагенты
    грузоотправитель = models.CharField(
        max_length=200,
        verbose_name="Грузоотправитель (наименование, адрес, телефон)"
    )
    грузополучатель = models.CharField(
        max_length=200,
        verbose_name="Грузополучатель (наименование, адрес, телефон)"
    )
    плательщик = models.CharField(
        max_length=200,
        verbose_name="Плательщик (наименование, адрес, реквизиты)"
    )
    
    # Товарный раздел
    код_продукции = models.CharField(
        max_length=50,
        verbose_name="Код продукции",
        blank=True,
        null=True
    )
    наименование = models.CharField(
        max_length=100,
        verbose_name="Наименование товара",
        blank=True,
        null=True
    )
    единица_измерения = models.CharField(
        max_length=10,
        verbose_name="Единица измерения",
        blank=True,
        null=True
    )
    вид_упаковки = models.CharField(
        max_length=50,
        verbose_name="Вид упаковки",
        blank=True,
        null=True
    )
    количество_мест = models.PositiveIntegerField(
        verbose_name="Количество мест",
        blank=True,
        null=True
    )
    масса_брутто = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        verbose_name="Масса брутто, т",
        blank=True,
        null=True
    )
    масса_нетто = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        verbose_name="Масса нетто, т",
        blank=True,
        null=True
    )
    цена = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена, руб.",
        blank=True,
        null=True
    )
    сумма = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Сумма, руб.",
        blank=True,
        null=True
    )
    
    # Транспортный раздел
    перевозчик = models.ForeignKey(Перевозчик, on_delete=models.CASCADE)
    автомобиль_марка = models.CharField(
        max_length=50,
        verbose_name="Марка автомобиля",
        blank=True,
        null=True
    )
    автомобиль_гос_номер = models.CharField(
        max_length=20,
        verbose_name="Гос. номер автомобиля",
        blank=True,
        null=True
    )
    водитель_фио = models.ForeignKey(Водитель, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Водитель")
    транспортное_средство = models.ForeignKey(
        ТранспортноеСредство,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Транспортное средство"
    )
    
    # Пункты погрузки/разгрузки
    перевозчик = models.ForeignKey(Перевозчик, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Перевозчик")
    пункт_погрузки = models.CharField(
        max_length=200,
        verbose_name="Пункт погрузки (адрес, телефон)",
        blank=True,
        null=True
    )
    пункт_разгрузки = models.CharField(
        max_length=200,
        verbose_name="Пункт разгрузки (адрес, телефон)",
        blank=True,
        null=True
    )
    срок_доставки = models.DateField(
        verbose_name="Срок доставки",
        blank=True,
        null=True
    )
    
    # Статусные поля
    статус = models.CharField(
        max_length=20,
        choices=[('draft', 'Черновик'), ('active', 'Активна'), ('completed', 'Завершена'), ('canceled', 'Аннулирована')],
        default='draft',
        verbose_name="Статус накладной"
    )
    
    # Дополнительные поля
    дата_отправки = models.DateField(
        verbose_name="Дата отправки",
        blank=True,
        null=True
    )
    дата_доставки = models.DateField(
        verbose_name="Дата доставки",
        blank=True,
        null=True
    )
    тип_груза = models.CharField(
        max_length=100,
        verbose_name="Тип груза",
        blank=True,
        null=True
    )
    платежные_реквизиты = models.CharField(
        max_length=200,
        verbose_name="Платежные реквизиты",
        blank=True,
        null=True
    )
    комментарий = models.TextField(
        verbose_name="Комментарий",
        blank=True,
        null=True
    )
    
    def save(self, *args, **kwargs):
        """Автоматический расчет суммы при сохранении"""
        if self.цена and self.количество_мест:
            self.сумма = self.цена * self.количество_мест
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Транспортная накладная"
        verbose_name_plural = "Транспортные накладные"
        ordering = ['-дата_составления']
        indexes = [
            models.Index(fields=['номер']),
            models.Index(fields=['дата_составления']),
            models.Index(fields=['статус']),
        ]

    def __str__(self):
        return f"ТТН №{self.номер} от {self.дата_составления}"



class ФинансовыйОтчет(models.Model):
    """Модель финансового отчета"""
    период_начала = models.DateField(verbose_name="Начало периода")
    период_окончания = models.DateField(verbose_name="Окончание периода")
    
    # Финансовые показатели
    доходы = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Сумма доходов")
    расходы = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Сумма расходов")
    прибыль = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Прибыль")
    
    # Дополнительно
    комментарий = models.TextField(verbose_name="Комментарий", blank=True, null=True)
    файл = models.FileField(
        upload_to='financial_reports/',
        verbose_name="Файл отчета",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Финансовый отчет"
        verbose_name_plural = "Финансовые отчеты"
        ordering = ['-период_начала']
        unique_together = ['период_начала', 'период_окончания']

    def save(self, *args, **kwargs):
        self.прибыль = self.доходы - self.расходы
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Финотчет за {self.период_начала} - {self.период_окончания}"

class ОтчетОДоставке(models.Model):
    """Модель отчета о доставке груза"""
    
    # Связи с другими моделями
    транспортная_накладная = models.ForeignKey(
        'ТранспортнаяНакладная',
        on_delete=models.PROTECT,
        related_name='отчеты_доставки',
        verbose_name="Транспортная накладная"
    )
    
    # Основные данные о доставке
    дата_прибытия = models.DateTimeField(
        verbose_name="Фактическая дата прибытия"
    )
    дата_убытия = models.DateTimeField(
        verbose_name="Фактическая дата убытия",
        blank=True,
        null=True
    )
    
    # Параметры транспортировки
    пробег = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Пробег, км",
        validators=[MinValueValidator(0)]
    )
    время_в_пути = models.DurationField(
        verbose_name="Общее время в пути"
    )
    средняя_скорость = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Средняя скорость, км/ч",
        blank=True,
        null=True
    )
    
    # Информация о водителе и транспорте
    водитель = models.ForeignKey(
        'Водитель',
        on_delete=models.SET_NULL,
        verbose_name="Водитель",
        blank=True,
        null=True
    )
    транспортное_средство = models.ForeignKey(
        'ТранспортноеСредство',
        on_delete=models.SET_NULL,
        verbose_name="Транспортное средство",
        blank=True,
        null=True
    )
    
    # Статус доставки
    СТАТУС_ДОСТАВКИ = [
        ('in_progress', 'В процессе доставки'),
        ('delivered', 'Доставлено'),
        ('partially', 'Доставлено частично'),
        ('canceled', 'Отменено'),
        ('problem', 'Проблема с доставкой'),
    ]
    статус = models.CharField(
        max_length=20,
        choices=СТАТУС_ДОСТАВКИ,
        default='in_progress',
        verbose_name="Статус доставки"
    )
    
    # Дополнительная информация
    примечание = models.TextField(
        verbose_name="Комментарий к доставке",
        blank=True,
        null=True
    )
    подтверждение_получателя = models.BooleanField(
        default=False,
        verbose_name="Подтверждение получения"
    )
    фото_документов = models.ImageField(
        upload_to='delivery_proofs/',
        verbose_name="Фото документов",
        blank=True,
        null=True
    )
    
    # Системные поля
    создано = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания отчета"
    )
    обновлено = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата последнего обновления"
    )

    class Meta:
        verbose_name = "Отчет о доставке"
        verbose_name_plural = "Отчеты о доставке"
        ordering = ['-дата_прибытия']
        indexes = [
            models.Index(fields=['статус']),
            models.Index(fields=['транспортная_накладная']),
        ]

    def __str__(self):
        return (
            f"Отчет о доставке №{self.id} по ТТН "
            f"{self.транспортная_накладная.номер} "
            f"({self.дата_прибытия.date()})"
        )

    def save(self, *args, **kwargs):
        """Автоматический расчет средней скорости при сохранении"""
        if self.пробег and self.время_в_пути:
            hours = self.время_в_пути.total_seconds() / 3600
            if hours > 0:
                self.средняя_скорость = float(self.пробег) / hours
        super().save(*args, **kwargs)

    @property
    def время_доставки(self):
        """Возвращает время доставки в часах"""
        return self.время_в_пути.total_seconds() / 3600 if self.время_в_пути else 0

    @property
    def задержка_доставки(self):
        """Рассчитывает задержку доставки в днях"""
        if not hasattr(self, 'транспортная_накладная'):
            return 0
        planned_date = self.транспортная_накладная.срок_доставки
        if planned_date and self.дата_прибытия:
            delta = self.дата_прибытия.date() - planned_date
            return delta.days if delta.days > 0 else 0
        return 0
    
