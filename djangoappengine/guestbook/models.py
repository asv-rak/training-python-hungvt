from google.appengine.ext import ndb
from google.appengine.api import taskqueue

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.

class Greeting(ndb.Model):
    '''Models an individual Guestbook entry.'''
    author = ndb.UserProperty()
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

    def get_greetings_object(self, guestbook_name):
        guestbook_obj = Guestbook()
        greeting_object = Greeting(parent=guestbook_obj.guestbook_key(guestbook_name))
        return greeting_object

class Guestbook(ndb.Model):
    def get_lastest_greeting(self, guestbook_name,
                             number_of_greeting=10):
        greetings_query = Greeting.query(ancestor=self.guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(number_of_greeting)

        return greetings

    def guestbook_key(self, guestbook_name=DEFAULT_GUESTBOOK_NAME):
        '''Constructs a Datastore key for a Guestbook entity with guestbook_name.'''
        return ndb.Key('Guestbook', guestbook_name)

    def put_greeting(self, guestbook_name, content, author):
        greeting = Greeting().get_greetings_object(guestbook_name)
        greeting.content = content
        greeting.author = author
        greeting.put()

    def sendmail(self, title, author):
        taskqueue.add(
            method='GET',
            url='/mail',
            params={'title': title, 'author': author})

    @staticmethod
    def get_default_name():
        return DEFAULT_GUESTBOOK_NAME