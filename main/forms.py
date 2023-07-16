from django import forms

CHOICES = (
    ('156', 'BI-аналитик, аналитик данных'),
    ('160', 'DevOps-инженер'),
    ('10', 'Аналитик'),
    ('12', 'Арт-директор, креативный директор'),
    ('150', 'Бизнес-аналитик'),
    ('25', 'Гейм-дизайнер'),
    ('165', 'Дата-сайентист'),
    ('34', 'Дизайнер, художник'),
    ('36', 'Директор по информационным технологиям (CIO)'),
    ('73', 'Менеджер продукта'),
    ('155', 'Методолог'),
    ('96', 'Программист, разработчик'),
    ('164', 'Продуктовый аналитик'),
    ('104', 'Руководитель группы разработки'),
    ('157', 'Руководитель отдела аналитики'),
    ('107', 'Руководитель проектов'),
    ('112', 'Сетевой инженер'),
    ('113', 'Системный администратор'),
    ('148', 'Системный аналитик'),
    ('114', 'Системный инженер'),
    ('116', 'Специалист по информационной безопасности'),
    ('121', 'Специалист технической поддержки'),
    ('124', 'Тестировщик'),
    ('125', 'Технический директор (CTO)'),
    ('126', 'Технический писатель')
)

SKILLS = (
    ('1', 'Python'),
    ('2', 'CPP'),
    ('3', 'C#'),
    ('4', 'Java'),
    ('5', 'GO'),
    ('6', 'Ruby')
)

AREAS = (
    ('1', 'Москва'),
    ('2', 'Санкт-Петербург'),
    ('88', 'Казань')
)

class FieldForm(forms.Form):
    field = forms.ChoiceField(label="", choices=CHOICES)

class AreaForm(forms.Form):
    area = forms.ChoiceField(label="", choices=AREAS)

class ResumeForm(forms.Form):
    field = forms.ChoiceField(label="Что Вас интересует?", choices=CHOICES, widget=forms.Select(attrs={'class': 'myfieldclass'}))
    area = forms.ChoiceField(label="Где?", choices=AREAS, widget=forms.Select(attrs={'class': 'myfieldclass'}))
    name = forms.CharField(label="Имя", max_length=100)
    position = forms.CharField(label="Желаемая позиция", max_length=255)
    skills = forms.ChoiceField(label="Навыки", choices=SKILLS, widget=forms.Select(attrs={'class': 'myfieldclass'}))
    about = forms.CharField(label="О Вас", widget=forms.Textarea)


