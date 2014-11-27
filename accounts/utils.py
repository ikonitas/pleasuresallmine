import itertools
import string
import random
from django.contrib.auth.models import User

def generate_username(first_name=None, last_name=None):
    """
    Create a unique user id given a first and last name.
    First, we try simple concatenation of first and last name.
    If that doesn't work, we add random numbers to the name
    """

    valid_id = False
    test_name = (first_name + '_' + last_name).lower().replace(" ", "")[:30]
    while valid_id is False:
        try:
            User.objects.get(username=test_name)
            test_name = '%s_%s' % (test_name, str(random.randrange(1, 9999)))
            test_name = test_name[:30]
        except User.DoesNotExist:
            valid_id = True
    return(test_name)


initial_consonants = (set(string.ascii_lowercase) - set('aeiou')
                      # remove those easily confused with others
                      - set('qxc')
                      # add some crunchy clusters
                      | set(['bl', 'br', 'cl', 'cr', 'dr', 'fl',
                             'fr', 'gl', 'gr', 'pl', 'pr', 'sk',
                             'sl', 'sm', 'sn', 'sp', 'st', 'str',
                             'sw', 'tr'])
                      )

final_consonants = (set(string.ascii_lowercase) - set('aeiou')
                    # confusable
                    - set('qxcsj')
                    # crunchy clusters
                    | set(['ct', 'ft', 'mp', 'nd', 'ng', 'nk', 'nt',
                           'pt', 'sk', 'sp', 'ss', 'st'])
                    )

vowels = 'aeiou' # we'll keep this simple

# each syllable is consonant-vowel-consonant "pronounceable"
syllables = map(''.join, itertools.product(initial_consonants,
                                           vowels,
                                           final_consonants))

# you could throw in number combinations, maybe capitalized versions...

def gibberish(wordcount, wordlist=syllables):
    return random.sample(wordlist, wordcount)

def get_pronounceable_password(wordcount=2, digitcount=2):
    numbermax = 10 ** digitcount
    password = ''.join(gibberish(wordcount))
    if digitcount >= 1:
        password += str(int(random.random()*numbermax))
    return password
