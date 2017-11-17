from django.test import TestCase

# Create your tests here.

from bootcamp.settings import *

if __name__ == '__main__':
    print(PROJECT_DIR.child('templates'))
    print(STATIC_ROOT)
    print(STATICFILES_DIRS)
    print(BASE_DIR)