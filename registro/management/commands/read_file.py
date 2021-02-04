from django.core.management.base import BaseCommand, CommandError
from registro.utils import scrapfile

class Command(BaseCommand):
	help = 'Closes the specified poll for voting'

	def handle(self, *args, **options):
		scrapfile()
		# print(response.text[6:])