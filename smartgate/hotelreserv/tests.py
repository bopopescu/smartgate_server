from django.test import TestCase

# Create your tests here.

def print():

    from . import condb as db

    print(db[0])

    return

