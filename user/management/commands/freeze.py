from django.core.management.base import BaseCommand
import subprocess

class Command(BaseCommand):
    help = 'Create a requirements.txt file using pip freeze.'

    def handle(self, *args, **kwargs):
        try:
            subprocess.check_call(["pip", "freeze", ">", "requirements.txt"], shell=True)
            self.stdout.write(self.style.SUCCESS('Successfully created requirements.txt'))
        except subprocess.CalledProcessError:
            self.stderr.write(self.style.ERROR('Failed to create requirements.txt'))
