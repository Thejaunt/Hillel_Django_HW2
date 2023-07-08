import sys
from random import choice, randint

from django.core.management.base import BaseCommand

from bookstore.models import Author, Book, Publisher, Store

from faker import Faker


class Command(BaseCommand):
    help = "** Create Dummy Authors  **"

    def add_arguments(self, parser):
        parser.add_argument("--authors",
                            type=int, choices=range(0, 1001), default=0, help="Amount of new authors to create")
        parser.add_argument("--publishers",
                            type=int, choices=range(0, 101), default=0, help="Amount of new publishers")
        parser.add_argument("--books",
                            type=int, choices=range(0, 10_001), default=0, help="Amount of new books")
        parser.add_argument("--stores",
                            type=int, choices=range(0, 1001), default=0, help="Amount of new stores")
        parser.add_argument("--create_relations",
                            type=int, nargs="?", choices=range(0, 10_000), default=0, help="Create with relations")

    @staticmethod
    def __obj_creator(name):
        fake = Faker()
        obj, inst = None, None
        if name == "authors":
            inst = Author
            obj = Author(name=fake.name(), age=randint(18, 80))
        if name == "publishers":
            inst = Publisher
            obj = Publisher(name=fake.company())
        if name == "books":
            inst = Book
            obj = Book(name=fake.catch_phrase(),
                       pages=randint(10, 1000),
                       price=randint(0, 1000),
                       rating=randint(1, 10),
                       pubdate=fake.date_object(),
                       )
        if name == "stores":
            obj = Store(name=f"{fake.first_name()} - {fake.company_suffix()}")
        return obj, inst

    def __list_creator(self, name, iters: int):
        list_of_obj = list()
        sys.stdout.write(f"* CREATING LIST OF {iters} new {name} *\n")
        for i in range(1, iters + 1):

            obj, inst = self.__obj_creator(name)
            list_of_obj.append(obj)
        return list_of_obj

    def handle(self, *args, **options):
        models = ["authors", "publishers", "books", "stores"]
        num_rel = options.get("create_relations")
        if num_rel is None:
            sys.stdout.write(
                self.style.ERROR("[ERROR]: Please specify amount of relations you want to create [1, 100]"
                                 )
            )
            return None

        if num_rel > 0:
            sys.stdout.write("Retrieving books...\n")
            books = Book.objects.filter()
            sys.stdout.write("Retrieving publishers...\n")
            publishers = Publisher.objects.all()
            sys.stdout.write("Retrieving authors...\n")
            authors = Author.objects.all()
            sys.stdout.write("Retrieving stores...\n")
            stores = Store.objects.all()
            sys.stdout.write("Checking if models aren't empty...\n")
            if not all([books, publishers, authors, stores]):
                return sys.stdout.write(self.style.ERROR("[ERROR]: Some tables are still empty\n"))
            sys.stdout.write(self.style.WARNING("* CREATING RELATIONS *\n"))
            for _ in range(num_rel):
                book = choice(books)

                book.authors.add(*[choice(authors) for _ in range(randint(1, 3))])
                book.store_set.add(*[choice(stores).pk for _ in range(randint(1, 10))])
                publisher = publishers[randint(1, len(publishers)-1)]
                book.publisher = publisher
                book.save()
            sys.stdout.write(self.style.SUCCESS("** ALL DONE **\n"))
            return None

        for name in models:
            if options.get(name):
                list_of_obj = self.__list_creator(name, options.get(name))
                sys.stdout.write(self.style.WARNING(f"** SAVING DATA IN DB **\n"))
                list_of_obj[0].__class__.objects.bulk_create(list_of_obj)
                sys.stdout.write(self.style.SUCCESS(f"*** ALL GOOD DATA HAS BEEN SAVED ***\n\n"))



