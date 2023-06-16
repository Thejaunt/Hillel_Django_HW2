from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "** Brutally Annihilates Users By IDs  **"

    def add_arguments(self, parser):
        parser.add_argument("user_id", type=int, nargs="*", help="Users IDs To Be Deleted")

    def handle(self, *args, **options):
        user = get_user_model()
        ids_list: list = options.get("user_id")

        #  Checking that there is no superuser to be deleted
        superuser_objs = user.objects.filter(is_superuser=1)
        super_ids_list: list[int] = [obj.pk for obj in superuser_objs]
        if any((super_id in ids_list) for super_id in super_ids_list):
            return self.stdout.write(self.style.ERROR(f"[Error] Cannot delete superuser(s) id: {super_ids_list}"))

        user_list = user.objects.filter(pk__in=ids_list)
        if not user_list:
            return self.stdout.write(self.style.WARNING("[WARNING] No ids to delete. Entered ids don't exist"))

        del_ids = [obj.pk for obj in user_list]
        user_list.delete()
        return self.stdout.write(self.style.SUCCESS(f"[SUCCESS] {len(del_ids)} id(s) deleted - id(s): {del_ids}"))
