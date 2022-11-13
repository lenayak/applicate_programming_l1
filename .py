import os
import requests
from bs4 import BeautifulSoup 
from time import sleep


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
        if mark >= 0 and mark <= 5:
            self.mark = mark
    def get_mark(self):
        return self.mark
    def get_name(self):
        return self.name
    def get_review(self):
        return self.review

headers = {           
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 '
                  'Safari/537.36 OPR/40.0.2308.81',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'DNT': '1',
    'Accept-Encoding': 'gzip, deflate, lzma, sdch',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'
}
def get_page(URL):        
    try:
        html_page = requests.get(URL, headers = headers)
        sleep(2)
        if html_page.status_code == 200:
            return BeautifulSoup(html_page.content, 'lxml')
        else:
            print("Страница не найдена.")
            exit()
    except:
        print('Ошибка соединения.')
        return -1
def get_marks(articles):       
    marks = list()
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
        soup = get_page(URL + "~" + str(i) + "#reviews")
        if soup == -1:
            continue
        if (soup.find('h1').text == "Пожалуйста, подождите пару секунд, идет перенаправление на сайт..."):
            print('Вылезла капча.')
            sleep(10)
            continue
        try:
            articles = (             
                soup.find('main', class_ = "main-body page-content")
                .find('section', class_ = "lenta__content")
                .find_all("article", class_="review-card lenta__item")
            )
        except AttributeError as e:
            print('Не удалось загрузить страницу')
            continue
        marks = get_marks(articles)
        if marks == -1:
            continue
        names = get_names(articles)
        if names == -1:
            continue
        reviews = get_reviews(articles)
        if reviews == -1:
            continue
        for j in range(0, len(marks)):
            k = Review(names[j], reviews[j], float(marks[j]))  
            if k.mark < 1.5:              
                if one < 1000:     
                    one +=1
                    dataset.append(k)
                else:           
                    one = one
            elif (k.mark >= 1.5 and k.mark < 2.5):
                if two < 1000:
                    two +=1
                    dataset.append(k)
                else:
                    two = two
            elif (k.mark >= 2.5 and k.mark < 3.5):
                if three < 1000:
                    three +=1
                    dataset.append(k)
                else: 
                    three = three
            elif (k.mark >= 3.5 and k.mark < 4.5):
                if four < 1000:
                    four +=1
                    dataset.append(k)
                else:
                    four = four
            elif (k.mark >= 4.5 and k.mark <= 5):
                if five < 1000:
                    five +=1
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
        os.mkdir('dataset/'+str(i))

def save_reviews(data, filename):
    for i in range(0, len(data)):
         file = open(filename + f"\\{(i+1):04}" + ".txt", "w", encoding="utf-8")
         file.write(data[i].get_name()) 
         file.write("\n\n\n")
         file.write(data[i].get_review())
         file.close


if __name__ == "__main__":
    URL =  'https://www.livelib.ru/reviews/'
    max_num_of_requests = 9000
    least_num_of_marks = 1000   
    dataset = parse_pages(max_num_of_requests, least_num_of_marks)
    create_folder()
    one_data = [el for el in dataset if el.get_mark()<1.5]
    save_reviews(one_data, "dataset\\1")
    two_data = [el for el in dataset if el.get_mark()>=1.5 and el.get_mark()<2.5]
    save_reviews(two_data, "dataset\\2")
    three_data = [el for el in dataset if el.get_mark()>=2.5 and el.get_mark()<3.5]
    save_reviews(three_data, "dataset\\3")
    four_data = [el for el in dataset if el.get_mark()>=3.5 and el.get_mark()<4.5]
    save_reviews(four_data, "dataset\\4")
    five_data = [el for el in dataset if el.get_mark()>=4.5 and el.get_mark()<=5.0]
    save_reviews(five_data, "dataset\\5")
    print("Работа завершена.")