from django.contrib.auth.models import User,Group
from django.core.management.base import BaseCommand 

groups = ['pib_admin','pib_officer','pib_user']

class Command(BaseCommand):
    help = 'create groups'

    def handle(self, *args, **kwargs):
        try:
            for group in groups:
                group_obj = Group.objects.get_or_create(name=group)
            print("Groups created successfully")

        except Exception as e:
            print("error occured while creating groups --> "+str(e))