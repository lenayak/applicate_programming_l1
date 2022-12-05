import os
from time import sleep
import requests
from bs4 import BeautifulSoup as bs

import utils


if __name__ == "__main__":
    URL =  'https://www.livelib.ru/reviews/'
    max_num_of_requests = 9000
    least_num_of_marks = 1000   
    dataset = utils.parse_pages(max_num_of_requests, least_num_of_marks)
    utils.create_folder()
    one_data = [el for el in dataset if el.get_mark() < 1.5]
    utils.save_reviews(one_data, os.path.join("dataset", "1"))
    two_data = [el for el in dataset if (el.get_mark() >= 1.5) and (el.get_mark() < 2.5)]
    utils.save_reviews(two_data, os.path.join("dataset","2"))
    three_data = [el for el in dataset if (el.get_mark() >= 2.5) and (el.get_mark() < 3.5)]
    utils.save_reviews(three_data, os.path.join("dataset", "3"))
    four_data = [el for el in dataset if (el.get_mark() >= 3.5) and (el.get_mark() < 4.5)]
    utils.save_reviews(four_data, os.path.join("dataset", "4"))
    five_data = [el for el in dataset if (el.get_mark() >= 4.5) and (el.get_mark() <= 5.0)]
    utils.save_reviews(five_data, os.path.join("dataset", "5"))
    print("Работа завершена.")