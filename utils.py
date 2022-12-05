import os
from time import sleep
import requests
from bs4 import BeautifulSoup as bs

import info


class Review:
    def __init__(self, name, review, mark):
        if name != " ":
            self.name = name
        if name == None:
            print("Некорректное название.")
            exit()
        if review == None:
            print("Некорректное содержание.")
            exit()
        self.review = review         
        if (mark >= 0) and (mark <= 5):
            self.mark = mark

    def get_mark(self):
        return self.mark

    def get_name(self):
        return self.name

    def get_review(self):
        return self.review


def get_page(URL):        
    try:
        html_page = requests.get(URL, headers = info.headers)
        sleep(2)
        if html_page.status_code == 200:
            return bs(html_page.content, 'lxml')
        else:
            print("Страница не найдена.")
            exit()
    except:
        print('Ошибка соединения.')
        return -1


def get_marks(articles):       
    marks = []
    for article in articles:   
        try:
            lenta_card = article.find('div', class_="lenta-card")
            h3 = lenta_card.find('h3', class_="lenta-card__title")
            mark = h3.find('span', class_="lenta-card__mymark").text.strip()
            marks.append(mark)
        except AttributeError as e:
            print('Не найдена оценка.')
            return -1
    return marks


def get_names(articles):          
    names = list()
    for article in articles:    
        try:
            lenta_card = article.find('div', class_="lenta-card")
            lenta_card_book_wrapper = lenta_card.find('div', class_="lenta-card-book__wrapper")
            name = lenta_card_book_wrapper.find('a', class_="lenta-card__book-title").text.strip()
            names.append(name)
        except AttributeError as e:
            print('Не найдено название.')
            return -1
    return names


def get_reviews(articles):            
    reviews = list()
    for article in articles:
        try:
            lenta_card = article.find('div', class_="lenta-card")
            text_without_readmore = lenta_card.find('div', class_="lenta-card__text without-readmore")
            review = text_without_readmore.find(id="lenta-card__text-review-escaped").text
            reviews.append(review) 
        except AttributeError as e:
            print('Не найдена рецензия.')
            return -1
    return reviews


def parse_pages(max_num_of_requests, least_num_of_marks):   
    dataset = list()
    one = 0
    two = 0
    three = 0
    four = 0
    five = 0 
    for i in range(1, max_num_of_requests):
        print(f'Страница: {i}')
        soup = get_page(info.URL + "~" + str(i) + "#reviews")
        if soup == -1:
            continue
        if (soup.find('h1').text == "Пожалуйста, подождите пару секунд, идет перенаправление на сайт..."):
            print('Вылезла капча.')
            sleep(10)
            continue
        try:
            articles = (             
                soup.find('main', class_="main-body page-content")
                .find('section', class_="lenta__content")
                .find_all("article", class_="review-card lenta__item")
            )
        except AttributeError as e:
            print('Не удалось загрузить страницу')
            continue
        marks = get_marks(articles)
        names = get_names(articles)
        reviews = get_reviews(articles)
        if marks == -1 or names == -1 or reviews == -1:
            continue
        for j in range(0, len(marks)):
            k = Review(names[j], reviews[j], float(marks[j]))  
            if k.mark < 1.5:              
                if one < least_num_of_marks:     
                    one += 1
                    dataset.append(k)
                else:           
                    one = one
            elif (k.mark >= 1.5) and (k.mark < 2.5):
                if two < least_num_of_marks:
                    two += 1
                    dataset.append(k)
                else:
                    two = two
            elif (k.mark >= 2.5) and (k.mark < 3.5):
                if three < least_num_of_marks:
                    three += 1
                    dataset.append(k)
                else: 
                    three = three
            elif (k.mark >= 3.5) and (k.mark < 4.5):
                if four < least_num_of_marks:
                    four += 1
                    dataset.append(k)
                else:
                    four = four
            elif (k.mark >= 4.5) and (k.mark <= 5):
                if five < least_num_of_marks:
                    five += 1
                    dataset.append(k)
                else:
                    five = five          
        print(f"One = {one}, Two = {two}, Three = {three}, Four = {four}, Five = {five}") 
        if(
            one >= least_num_of_marks
            and two >= least_num_of_marks
            and three >= least_num_of_marks
            and four >= least_num_of_marks
            and five >= least_num_of_marks
        ):
            i = max_num_of_requests
            break
    return dataset   


def create_folder():
    os.mkdir('dataset')
    for i in range(1,6):
        os.mkdir('dataset/' + str(i))


def save_reviews(data, filename):
    for i in range(0, len(data)):
        file = open(filename + f"\\{(i+1):04}" + ".txt", "w", encoding="utf-8")
        file.write(data[i].get_name()) 
        file.write("\n\n\n")
        file.write(data[i].get_review())
        file.close
