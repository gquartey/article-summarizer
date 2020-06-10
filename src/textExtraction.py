# imports for reading from pdfs
from tika import parser
# imports for reading from news sites 
import requests
import html5lib
from bs4 import BeautifulSoup
import regex as re


def read_from_pdf(pdf_path):
    '''
    F
    input:
        pdf_path - string
    output: 
        string
    '''
    raw = parser.from_file('pdf_path')
    return raw['content']

def strip_html(body):
    '''
    Helper function to strip html tags from string
    input:
        body - string
    output: 
        string 
    '''
    return body.get_text()

def read_from_website(url):
    '''
    input:
        url - string
    output: 
        string
    '''
    # get html for the webpage passed in 
    try:
        r1 = requests.get(url)
    except: 
        raise Exception('Request to given url failed')
    # get html content from given url 
    page = r1.content

    # create a soup so we can use beautiful soup 
    soup1 = BeautifulSoup(page, 'html5lib')

    # article = soup1.find_all('div',class_='article-body')
    article_paragraphs = soup1.find_all('p')
    article_body = ""
    for paragraph in article_paragraphs:
        article_body += strip_html(paragraph)
    return article_body
    
def get_title(url):
    try:
        r1 = requests.get(url)
    except:
        raise Exception('Request to given url failed')
    # get html content from given url
    page = r1.content

    # create a soup so we can use beautiful soup
    soup1 = BeautifulSoup(page,'html5lib')

    article_title = soup1.find_all('h1')

    title = strip_html(article_title[0])

    return title


# stuff  = read_from_website('https://english.elpais.com/society/2020-06-07/spains-regions-report-just-one-coronavirus-death-in-the-last-24-hours.html')
# print(stuff)