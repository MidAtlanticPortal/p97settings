from ConfigParser import RawConfigParser
import string

# Note: CONFIG_FILE is an implicit requirement. 
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

class Command(BaseCommand):
    help = '''Generates a secret key for use in production.

Warning: This reads, parses, and writes the .ini file. It will not preserve 
comments or ordering.'''

    def generate_secret(self):
        chars = string.ascii_lowercase + string.digits + '!@#$%^&*()'
        return get_random_string(50, chars)

    def handle(self, *args, **options):
        cfg = RawConfigParser()
        cfg.optionxform = str
        cfg.read(settings.CONFIG_FILE)
        
        if not cfg.has_section('APP'):
            cfg.add_section('APP')

        cfg.set('APP', 'SECRET_KEY', self.generate_secret())
        cfg.write(open(settings.CONFIG_FILE, 'w'))
        
        self.stdout.write('Successfully updated SECRET_KEY in %s' % settings.CONFIG_FILE)
