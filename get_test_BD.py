words_for_formuls = 'йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,.'

from re import finditer
from json import dump
import wikipediaapi
import os 
wiki_wiki = wikipediaapi.Wikipedia(
    user_agent='MathRAGBot/1.0 (example@gmail.com)', language='ru'
)
titles = [
    "Производная",
    "Первообразная",
    "Интеграл",
    "Определенный интеграл",
    "Формула Ньютона — Лейбница",
    "Исследование функций",
    "Экстремум",
    "Точка перегиба",
    "Касательная",
    "Логарифм",
    "Показательная функция",
    "Тригонометрические функции",
    "Обратные тригонометрические функции",
    "Тригонометрические уравнения",
    "Модуль (математика)",
    "Стереометрия",
    "Многогранник",
    "Куб",
    "Параллелепипед",
    "Призма (геометрия)",
    "Пирамида (геометрия)",
    "Тела вращения",
    "Цилиндр",
    "Конус",
    "Шар",
    "Сфера",
    "Вектор (математика)",
    "Скалярное произведение",
    "Метод координат",
    "Угол между прямыми",
    "Расстояние от точки до плоскости",
    "Алгебраическое уравнение",
    "Система линейных алгебраических уравнений",
    "Неравенство",
    "Метод интервалов",
    "Параметр (математика)",
    "Теория вероятностей",
    "Вероятность",
    "Условная вероятность",
    "Теорема Байеса",
    "Комбинаторика",
    "Перестановка",
    "Сочетание",
    "Размещение",
    "Статистика",
    "Математическое ожидание",
    "Дисперсия случайной величины",
    "Комплексное число",
    "Арифметическая прогрессия",
    "Геометрическая прогрессия"
]
titles = ["Алгебраическое уравнение"]
if not os.path.exists("data"):
    os.makedirs("data")
def refactor(text, title):
    global cnt
    if text.text.strip() and text.title.strip() not in "ПримечанияЛитератураСсылкиСм. также":
        
        final_text[title + " " + str(cnt)] = text.title.strip() + clear(text.text) 
        cnt+=1
    for i in text.sections:
        refactor(i, title)



def clear(text):
    last = ''
    cleaned_lines = ''
    uncleaned_lines = text.split('\n')
    for i in uncleaned_lines:

        f1 = any(s in i.strip() for s in words_for_formuls) 
        f2 = len(i.strip())
        f3 = r"{\displaystyle " in i.strip() 
        if len(i.strip()) != 0:
            print(cleaned_lines[-10:], i)
            if f1 and (f2 > 100 or any(s in last.strip() for s in words_for_formuls)) and not(f3):
               
               cleaned_lines+= " " + i.strip()
            elif f1 or f3:
                
                line = i.strip()
                print(line)
                f4 = sum([len(d.group()) for d in finditer(r"{\\[a-z]+|\\[a-z]+|}",line)])
                if f3 and len(line) - f4 > 10:
                    
                    line = line.replace(r"{\displaystyle ", "")
                    #line = line.replace(" ", "")
                   
                    
                    
                    line = " $$" + line[:-1] + "$$"
                    cleaned_lines += line
                   
                elif f3:
                    
                    line = line.replace(r"{\displaystyle ", "")
                   
                    #line = line.replace(" ", "")
                    
                   
                    line = " $" + line[:-1] + "$"
                    cleaned_lines += line
                   
                elif line[0] not in '.,':
                    line = " " + line
                    cleaned_lines += line
                elif line[0] in ',.':
                    cleaned_lines += line


                
            else:
                
                pass
                #cleaned_lines.append(i.strip() + "22222222222")
        last = i.strip()
    return cleaned_lines 
for title in titles:
    print("download: " + title)
    page = wiki_wiki.page(title)
    final_text = dict()
    final_text["Введение" + "1" + title] = clear(page.summary)

    cnt = 2
    for i in page.sections:
        refactor(i, title)
        cnt+=1
    filepath = os.path.join("data", title.strip() + ".json")
    with open(filepath, "w", encoding="utf-8") as f:
        dump(final_text, f,ensure_ascii=False, indent=4)
        print("save")
        continue
    print("not save")