from bookstore.tasks import email_sender_task

from bs4 import BeautifulSoup

from celery import shared_task

from django.conf import settings


import requests

from .models import Author, Quote, Tag


class AuthorPage:
    def __init__(self, page):
        self.page = page

    def get_born_date(self):
        return self.page.find("span", class_="author-born-date").get_text()

    def get_born_location(self):
        return self.page.find("span", class_="author-born-location").get_text()

    def get_bio(self):
        return self.page.find("div", class_="author-description").get_text()


class QuoteData:
    def __init__(self, data):
        self.data = data  # Beautifulsoup obj

    def get_author_name(self) -> str:
        return self.data.find("small", class_="author").getText()

    def get_author_link(self):
        return self.data.find("a").attrs.get("href")

    def get_quote_text(self) -> str:
        return self.data.find("span", class_="text").getText()[1:-1]

    def get_tags(self) -> list or None:
        tags_str = self.data.find("div", class_="tags").find("meta", class_="keywords").attrs.get("content")
        return tags_str.split(",")


class Page:
    def __init__(self, data):
        self.data = data

    def get_list_of_quotes(self):
        return self.data.find_all("div", class_="quote")

    def has_next(self) -> bool:
        next_page = self.data.find("nav").find("li", class_="next")
        if next_page:
            return True
        return False

    def get_next_page_link(self):
        return self.data.find("nav").find("li", class_="next").find("a").attrs.get("href")


def get_url(url):
    error = ""
    resp = None
    try:
        resp = requests.get(url)
        resp.raise_for_status()
    except Exception as err:
        error = str(err)
    return resp, error


def send_error_email(text):
    email_sender_task(
        subject="[ERROR] Celery bean scrapper",
        text=text,
        from_email=settings.EMAIL,
        recipient=settings.EMAIL,
    )


@shared_task
def scrap_scrap(url: str = "", counter: int = 0):  # NOQA
    base = "https://quotes.toscrape.com"
    counter = counter
    response, error = get_url(f"{base+url}")
    if error:
        send_error_email(f"Page Request failed \n [ERROR]: {error}")
        return None

    def get_soup_inst(resp):
        html = BeautifulSoup(resp.text, "html.parser")
        return html

    quotes_page = get_soup_inst(response)
    page = Page(quotes_page)
    quotes_list = page.get_list_of_quotes()
    for quote in quotes_list:
        quote_data = QuoteData(quote)
        """ PROCESSING AUTHOR"""
        author_name = quote_data.get_author_name()
        # if not in db - make request and fill data in
        author_obj, author_created = Author.objects.get_or_create(name=author_name)
        if author_created:
            """getting author data"""
            author_link = quote_data.get_author_link()
            auth_res, error = get_url(base + author_link)
            if error:
                send_error_email(f"Author Page Couldn't get {author_link}\n [ERROR]{error}")
                return None
            auth_soup = get_soup_inst(auth_res)
            author_page = AuthorPage(auth_soup)
            """ updating the created author """
            author_obj.born_date = author_page.get_born_date()
            author_obj.born_location = author_page.get_born_location()
            author_obj.bio = author_page.get_bio()
            author_obj.save()

        """ PROCESSING QUOTE """
        quote_text = quote_data.get_quote_text()
        if not quote_text:
            continue

        quote_obj, quote_created = Quote.objects.get_or_create(title=quote_text, author_id=author_obj.pk)
        if not quote_created:
            continue

        tags_list = quote_data.get_tags()
        if tags_list:
            # Check if tags exist, create new if not, refresh relations
            new_tag_list = []
            for tag in tags_list:
                tag_obj, created = Tag.objects.get_or_create(name=tag)
                new_tag_list.append(tag_obj)
            quote_obj.tags.set(new_tag_list)
        quote_obj.save()

        counter += 1
        if counter == 5:
            return None

    if page.has_next():
        #  go to next page
        scrap_scrap(url=page.get_next_page_link(), counter=counter)
    else:
        email_sender_task(
            subject="Celery bean scrapper",
            text="Nothing to scrap",
            from_email=settings.EMAIL,
            recipient=settings.EMAIL,
        )
