from google.appengine.ext import ndb

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    '''Constructs a Datastore key for a Guestbook entity with guestbook_name.'''
    return ndb.Key('Guestbook', guestbook_name)

class Greeting(ndb.Model):
    '''Models an individual Guestbook entry.'''
    author = ndb.UserProperty()
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

    # def get_10_latest_message(self, guestbook_name):
    #     greetings_query = Greeting.query(ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
    #     greetings = greetings_query.fetch(10)
    #     return greetings

    def get_greetings_object(self, guestbook_name):
        greeting_object = Greeting(parent=guestbook_key(guestbook_name))
        return greeting_object

    def add_new(self, guestbook_name, content, author):
        greeting = self.get_greetings_object(guestbook_name)
        greeting.content = content
        greeting.author = author
        greeting.put()

class Guestbook(ndb.Model):
    def get_lastest_greeting(self, guestbook_name,
                             number_of_greeting=10):
        greetings_query = Greeting.query(ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(number_of_greeting)

        return greetings