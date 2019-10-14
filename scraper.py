import requests, time, re
import argparse, sys, urllib
from bs4 import BeautifulSoup

def find_urls(text):
    '''self-explanatory'''
    url_reg = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    urls = re.findall(url_reg, text)
    print('URLS\n')
    print('\n'.join(urls) + '\n')
    
def find_atags(text): 
    '''helper for find_url'''
    a_tags = text.findAll('a')
    for link in a_tags:
        if link.get('href'):
            print(link.get('href'))

def find_img_tags(text):
    img_tags = text.findAll('img')
    for img in img_tags:
        if img.get('src'):
            print(img.get('src'))
    print('\n')
  
def find_emails(text):
    email_reg = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
    emails = re.findall(email_reg, text)
    print('EMAILS\n')
    print('\n'.join(set(emails)) + '\n')

def find_phones(text):
    phone_reg = r"1?\W*([2-9][0-8][0-9])\W*([2-9][0-9]{2})\W*([0-9]{4})(\se?x?t?(\d*))?"
    phones = re.findall(phone_reg, text)
    num_list = []
    for num in phones:
        area_code = num[0]
        middle_child = num[1]
        last_bit = num[2]
        let_me_get_them_digits = '({})-{}-{}'.format(area_code, middle_child, last_bit)
        num_list.append(let_me_get_them_digits)

    print('PHONES\n')
    print('\n'.join(set(num_list)) + '\n')

def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--todir',  help='destination directory for downloaded images')
    parser.add_argument('url', help='cmd line arg for url ')
    return parser

def main(args):
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)
    url = parsed_args.url

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    find_urls(response.text)
    find_atags(soup)
    find_img_tags(soup)
    find_emails(response.text)
    find_phones(response.text)

if __name__ == "__main__":
    main(sys.argv[1:])