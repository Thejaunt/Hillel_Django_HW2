from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand


from faker import Faker


class Command(BaseCommand):
    help = "** Command Helps To Create Dummy Users **"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.users = get_user_model().objects.all()
        self.new_usernames = list()

    def __create_user(self):
        fake = Faker()
        dummy_user = fake.simple_profile()
        name = dummy_user.get("username")

        #  Checking if the username already exists, creates new fake instance if it does
        if any((name == user.username) for user in self.users) or name in self.new_usernames:
            dummy_user = self.__create_user()

        self.new_usernames.append(dummy_user.get("username"))
        return dummy_user

    def add_arguments(self, parser):
        parser.add_argument("users", type=int, choices=range(1, 11), help="Amount of new users to be created")

    def handle(self, *args, **options):
        fake = Faker()
        user = get_user_model()
        list_of_users: list = list()
        for i in range(1, options.get("users") + 1):
            #  Just in case - fk stands for fake
            fk_user = self.__create_user()
            list_of_users.append(
                user(
                    username=fk_user.get("username"), email=fk_user.get("mail"), password=make_password(fake.password())
                )
            )
        user.objects.bulk_create(list_of_users)
