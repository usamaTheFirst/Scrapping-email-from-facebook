from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import re
import csv


class Crawler:
    """
    Class to to extract emnils from facebook pages
    it scraps all pages available in all categories

    """

    def __init__(self, start):

        # Retrieves main page which is fb.com/categories
        page = self.get_page(start)

        # Creating a file to store scrapped data
        self.file = open('emails.csv', 'a',newline='')

        # file writer object to write data to file
        # its instance variable so we can use it anywhere in instance methods
        self.file_writer = csv.writer(self.file)

        # entering field name which is 'emails
        self.file_writer.writerow(['email', ])

        # Getting links of all the links in category page
        self.categories = self.get_categories_link(page)

    def get_page(self, url):

        """
        Defining a method to get html page and return its BeautifulSoup object
        :param url:
        :return BeautifulSoup object:
        """

        # Sending request to targeted page which is specified by url

        html = requests.get(url).content

        # Creating a BeautifulSoup object and returning it
        page = BeautifulSoup(html, 'html.parser')
        return page

    def get_categories_link(self, page):
        """
        This method extracts internal links and converts them to absolute links
        :param page:
        :return links:
        """
        # Finding links
        cats = page.find_all('a', {'class': '_7179'})

        # Extracting the urls
        links = [link.attrs['href'] for link in cats]

        # Converting internal links to absoluter URLs
        mapper = lambda x: 'https://www.facebook.com/' + x
        links = list(map(mapper, links))

        return links

    def get_link_in_catg(self, url):
        """
        This method extracts targeted page links from inside the individual category page
        i.e extracting links of all business pages in business category
        :param url:
        :return:
        """

        page = self.get_page(url)
        new_page = str(page)
        pages_link = re.findall(r'https://www.facebook.com/(?!pages|login|recover|watch|help)[a-zA-Z0-9.]*/', new_page)
        pages_link = list(map(lambda x: x + "about", set(pages_link)))
        return pages_link

    def email_extractor(self, url):
        """
        this method first checks if targeted page has email and then it extracts email from them
        :param url:
        :return email:
        """
        # Getting BeautifulSoup object of the targetd email
        page = self.get_page(url)
        # Checking if the page has email class and then extraing email from it
        email = page.find_all('div', class_='_50f4', text=re.compile(('[a-zA-Z0-9.]+@.*')))
        # if email is not null return it
        if email:
            # Extracing the email string
            return email[0].text

    def crawl(self):
        # Iterating over categories
        for cat_link in self.categories:
            # Extracting link in one category
            page_link = self.get_link_in_catg(cat_link)
            # iterating over every page in a category
            for link in page_link:
                # extracting email
                email = self.email_extractor(link)
                if email:
                    # Writing email to file
                    print(email)
                    self.file_writer.writerow([email,])
                    self.file.flush()


if __name__ == '__main__':
    facebook_crawler = Crawler('https://www.facebook.com/pages/category/?_rdc=1&_rdr')
    facebook_crawler.crawl()
