from django.db import models

AREAS = (
    ('1', 'Москва'),
    ('2', 'Санкт-Петербург'),
    ('88', 'Казань')
)

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

class PagJson(models.Model):
    file = models.JSONField()
    objects = models.Manager()

class VacJson(models.Model):
    vac_id = models.IntegerField()
    file = models.JSONField()
    objects = models.Manager()

class PagJsonSJ(models.Model):
    file = models.JSONField()
    objects = models.Manager()

class VacJsonSJ(models.Model):
    vac_id = models.IntegerField()
    file = models.JSONField()
    objects = models.Manager()

class Vacancies(models.Model):
    vac_id = models.IntegerField()
    website = models.TextField(default="")
    desc = models.TextField()
    skills = models.TextField()
    area = models.IntegerField()
    spec = models.IntegerField()
    url = models.TextField(default="")
    objects = models.Manager()

class RecVacancy(models.Model):
    vac_id = models.IntegerField()
    title = models.TextField(default="")
    desc = models.TextField()
    url = models.TextField(default="")
    objects = models.Manager()

class Resume(models.Model):
    name = models.TextField()
    position = models.TextField()
    about = models.TextField()
    skills = models.CharField(choices=SKILLS, max_length=255, default="CPP")
    area = models.CharField(choices=AREAS, max_length=255, default="Москва")
    field = models.CharField(choices=CHOICES, max_length=255, default="Программист, разработчик")

