import heapq
from django.shortcuts import render
import requests
import json
import time
from requests.structures import CaseInsensitiveDict
from .models import *
import re
from Stemmer import Stemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .forms import *
import numpy as np
from .utils import *



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

api_key = "v3.r.136717909.1715a281dda2026605142480c85dd7a4f91bb532.4d1a51cbca77ee85590c375944986468db9499db"
headers = CaseInsensitiveDict()
headers["X-Api-App-Id"] = api_key

def getPageSJ(page):
    query = "разработчик"
    town = ["Москва", "Санкт-Петербург", "Казань"]
    position = [48, 37]
    url = f"https://api.superjob.ru/2.0/vacancies?catalogues[positions]={position}&town={town}&keyword={query}&count=99&page={page}"
    response = requests.get(url, headers=headers)
    data = response.content.decode()
    response.close()
    return data

def getPagSJ():
    for page in range(0, 5):
        jsObj = json.loads(getPageSJ(page))
        file = PagJsonSJ(file=jsObj)
        file.save()
        time.sleep(0.25)
    return ()

def getPage(page):
    params = {
            'professional_role': [156, 160, 10, 12, 150, 25, 165, 34, 36, 73, 155, 96, 164, 104, 157, 107, 112, 113,
                                  148, 114, 116, 121, 124, 125, 126],
            'area': [1, 2, 88],
            'page': page,
            'per_page': 20,
        }
    req = requests.get('https://api.hh.ru/vacancies', params)
    data = req.content.decode()
    req.close()

    return(data)

def getPag():
    for page in range(0, 80):
        jsObj = json.loads(getPage(page))
        file = PagJson(file=jsObj)
        file.save()
        time.sleep(0.25)
    return ()

def getVacSJ():
    pags = PagJsonSJ.objects.raw("SELECT id, file from main_pagjsonsj")
    for p in pags:
        jsonObj = p.file
        for v in jsonObj['objects']:
            req = requests.get("https://api.superjob.ru/2.0/vacancies/{}".format(v['id']))
            data = req.content.decode()
            req.close()
            data = json.loads(data)
            file = VacJsonSJ(vac_id=v['id'], file=data)
            file.save()
            time.sleep(0.25)
    return ()

def getVac():
    pags = PagJson.objects.raw("SELECT id, file from main_pagjson")
    for p in pags:
        jsonObj = p.file
        for v in jsonObj['items']:
            req = requests.get(v['url'])
            data = req.content.decode()
            req.close()
            data = json.loads(data)
            file = VacJson(vac_id=v['id'], file=data)
            file.save()
            time.sleep(0.25)
    return ()

def saveVacSJ():
    listSJ = []
    stemmer = Stemmer('russian')

    for fl in VacJsonSJ.objects.raw("SELECT * from main_vacjsonsj"):
        jsonObj = fl.file
        vectors = {}

        p_name = ''
        if (jsonObj['profession']):
            title = re.sub(r'[^a-zа-я]+', ' ', jsonObj['profession'].lower(), re.UNICODE)
            words = re.split(r'\s{1,}', title.strip())
            for title_word in words:
                title_word = stemmer.stemWord(title_word)
                if len(title_word.strip()) > 1:
                    p_name = p_name + " " + title_word.strip()

        p_doc = ''
        if (jsonObj['candidat']):
            doc = re.sub('<[^>]*>', '', jsonObj['candidat'].lower())
            doc = re.sub('&quot;', '', doc)
            doc = re.sub(r'[^a-zа-я]+', ' ', doc, re.UNICODE)
            words = re.split(r'\s{1,}', doc.strip())
            for word in words:
                word = stemmer.stemWord(word.strip())
                if len(word.strip()) > 1:
                    p_doc = p_doc + " " + word

        p_desc = p_name + " " + p_doc
        area = 0
        if jsonObj['town']['title'] == "Москва":
            area = 1
        elif jsonObj['town']['title'] == "Санкт-Петербург":
            area = 2
        elif jsonObj['town']['title'] == "Казань":
            area = 88
        else:
            area = 1
        spec = 0
        if bool(jsonObj['catalogues']):
            if jsonObj['catalogues'][0]['positions'] == 37:
                spec = 113
            else:
                spec = 96
        listSJ.append(p_desc)
        url = "https://api.superjob.ru/2.0/vacancies/{}".format(jsonObj['id'])
        file = Vacancies(vac_id=jsonObj['id'], website=1, desc=p_desc, skills="",
                         area=area, spec=spec, url=url)
        file.save()

    return listSJ

def saveVac():
    stemmer = Stemmer('russian')
    vectors = {}
    for fl in VacJson.objects.raw("SELECT * from main_vacjson"):
        jsonObj = fl.file


        p_name = ''
        if (jsonObj['name']):
            title = re.sub(r'[^a-zа-я]+', ' ', jsonObj['name'].lower(), re.UNICODE)
            words = re.split(r'\s{1,}', title.strip())
            for title_word in words:
                title_word = stemmer.stemWord(title_word)
                if len(title_word.strip()) > 1:
                    p_name = p_name + " " + title_word.strip()

        p_doc = ''
        doc = re.sub('<[^>]*>', '', jsonObj['description'].lower())
        doc = re.sub('&quot;', '', doc)
        doc = re.sub(r'[^a-zа-я]+', ' ', doc, re.UNICODE)
        words = re.split(r'\s{1,}', doc.strip())
        for word in words:
            word = stemmer.stemWord(word.strip())
            if len(word.strip()) > 1:
                p_doc = p_doc + " " + word

        p_skills = ''
        key_skills = ''
        vac_skills = jsonObj['key_skills']
        for skill in vac_skills:
            words = re.split(r'\s{1,}', skill['name'].lower().strip())
            for word in words:
                word = stemmer.stemWord(word)
                if len(word.strip()) > 1:
                    p_skills = p_skills + " " + word.strip()

        for skill in vac_skills:
            words = re.split(r'\s{1,}', skill['name'].lower().strip())
            for word in words:
                if len(word.strip()) > 1:
                    key_skills = key_skills + " " + word.strip()

        p_desc = p_name + " " + p_doc + " " + p_skills
        area = jsonObj['area']['id']
        if jsonObj['professional_roles'] is not None:
            specialization = jsonObj['professional_roles'][0]['id']
        vectors[jsonObj['id']] = p_desc

        file = Vacancies(vac_id=jsonObj['id'], website=0, desc=p_desc, skills=key_skills,
                         area=area, spec=specialization, url=jsonObj['alternate_url'])
        file.save()

    listSJ = saveVacSJ()
    listvec = [] # список с описаниями вакансий
    for value in vectors.values():
        listvec.append(value)
    for sj in listSJ:
        listvec.append(sj)
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(listvec)

    return(vectorizer)

def takeResInfo(position, about, skills):
    stemmer = Stemmer('russian')
    name = ''
    if position:
        title = re.sub(r'[^a-zа-я]+', ' ', position.lower(), re.UNICODE)
        words = re.split(r'\s{1,}', title.strip())
        for title_word in words:
            title_word = stemmer.stemWord(title_word)
            if len(title_word.strip()) > 1:
                name = name + " " + title_word.strip()

    upd_about = ''
    doc = re.sub('<[^>]*>', '', about.lower())
    doc = re.sub('&quot;', '', doc)
    doc = re.sub(r'[^a-zа-я]+', ' ', doc, re.UNICODE)
    words = re.split(r'\s{1,}', doc.strip())
    for word in words:
        word = stemmer.stemWord(word.strip())
        if len(word.strip()) > 1:
            upd_about = upd_about + " " + word

    for skill in SKILLS:
        if skill[0] == skills:
            skills = skill[1]

    upd_skills = ''
    words = re.split(r'\s{1,}', skills.lower().strip())
    for word in words:
        word = stemmer.stemWord(word)
        if len(word.strip()) > 1:
            upd_skills = upd_skills + " " + word.strip()

    new_about = name + " " + upd_about + " " + upd_skills

    return (new_about, skills)

def loadRecVacSJ(data):
    try:
        file = RecVacancy()
        file.vac_id = data['id']
        if data['profession']:
            file.title = data['profession']
        file.desc = data['candidat']
        file.url = "https://api.superjob.ru/2.0/vacancies/{}".format(data['id'])
        file.save()
    except:
        print("Вакансия не существует.")
    return ()

def loadRecVac(data):
    file = RecVacancy()
    file.vac_id = data['id']
    if data['name']:
        file.title = data['name']
    file.desc = data['description']
    file.url = data['alternate_url']
    file.save()
    return ()

def getRecs(vectorizer, resume):
    putRes = [resume.about]
    resVec = vectorizer.transform(putRes)

    vacs = Vacancies.objects.raw("SELECT * from main_vacancies WHERE spec = %s AND area = %s",
                                 [resume.field, resume.area])
    vecWeb = []
    vecId = []
    vecSim = []

    for vac in vacs:
        vVec = vac.desc
        putVec = [vVec]
        vacVec = vectorizer.transform(putVec)
        similar = cosine_similarity(resVec, vacVec)
        vecSim.append(similar)
        vecId.append(vac.vac_id)
        vecWeb.append(vac.website)
    """
    keyV = []
    valueV = []
    for key, value in vecDict.items():
        valueV.append(value)
        keyV.append(key)
    """

    array = np.asarray(vecSim)
    max_similarities = heapq.nlargest(20, range(len(array)), array.take)
    print(max_similarities)
    # номера вакансий в array, ранжированные по уменьшению схожести

    for item in max_similarities:
        #if vecWeb[item] == 0:
        req = requests.get('https://api.hh.ru/vacancies/{}'.format(vecId[item]))
        #else:
        #    req = requests.get('https://api.superjob.ru/2.0/vacancies/{}'.format(vecId[item]))
        data = req.content.decode()
        req.close()
        data = json.loads(data)
        #if vecWeb[item] == 0:
        loadRecVac(data)
        print('добавлено')
        #else:
            # loadRecVacSJ(data)

    return()

def city_graphs():
    xs = []
    ys = []
    qs = Vacancies.objects.all()
    for choice in AREAS:
        xs.append(choice[1])
        i = 0
        for item in qs:
            if item.area == int(choice[0]):
                i = i+1
        ys.append(i)
    return xs, ys

def spec_graphs():
    xs = []
    ys = []
    qs = Vacancies.objects.all()
    for choice in CHOICES:
        xs.append(choice[1])
        i = 0
        for item in qs:
            if item.spec == int(choice[0]):
                i = i+1
        ys.append(i)
    return xs, ys

def index(request):

    #records = VacJson.objects.all()
    #records.delete()
    #records = PagJson.objects.all()
    #records.delete()

    records = Vacancies.objects.all()
    records.delete()
    records = RecVacancy.objects.all()
    records.delete()
    records = VacJsonSJ.objects.all()
    records.delete()
    #records = PagJsonSJ.objects.all()
    #records.delete()

    #getPag()
    #getPagSJ()
    #getVac()
    #getVacSJ()
    vectorizer = saveVac()

    xs, ys = city_graphs()
    city_chart = get_cityplot(xs, ys)
    x, y = spec_graphs()
    spec_chart = get_plot(x, y)


    resume = Resume()
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume.name = form.cleaned_data.get("name")
            resume.area = form.cleaned_data.get("area")
            resume.field = form.cleaned_data.get("field")
            resume.position = form.cleaned_data.get("position")
            resume.about, resume.skills = takeResInfo(form.cleaned_data.get("position"),
                                                      form.cleaned_data.get("about"),
                                                      form.cleaned_data.get("skills"))
            resume.save()
            getRecs(vectorizer, resume)
    else:
        form = ResumeForm()

    recs = RecVacancy.objects.all()

    area_m = Vacancies.objects.filter(area="1").count()
    area_m = int(area_m)
    area_s = Vacancies.objects.filter(area="2").count()
    area_s = int(area_s)
    area_k = Vacancies.objects.filter(area="88").count()
    area_k = int(area_k)
    context = [["Москва", area_m], ["Санкт-Петербург", area_s], ["Казань", area_k]]

    jobs = []
    for choice in CHOICES:
        item = []
        item.append(choice[1])
        selected = Vacancies.objects.filter(spec=choice[0]).count()
        selected = int(selected)
        item.append(selected)
        jobs.append(item)

    return render(request, "main/index.html", {'res_form': form, 'recs': recs, 'chart': spec_chart,
                                               'citychart': city_chart, 'context': context, 'jobs': jobs})


def about(request):
    return render(request, "main/about.html")
