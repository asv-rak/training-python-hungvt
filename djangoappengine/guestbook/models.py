from google.appengine.ext import ndb
from google.appengine.api import taskqueue
from google.appengine.api import memcache
from google.appengine.datastore.datastore_query import Cursor

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'
FETCH_MAX = 2

# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.

class Greeting(ndb.Model):
    '''Models an individual Guestbook entry.'''
    author = ndb.UserProperty()
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
    last_update = ndb.DateTimeProperty(auto_now_add=True)
    updated_by = ndb.UserProperty()


    def get_greetings_object(self, guestbook_name):
        guestbook_obj = Guestbook(guestbook_name)
        greeting_object = Greeting(parent=guestbook_obj.guestbook_key())
        return greeting_object


    def convert_item_to_dict(self):
        data = self.to_dict()
        keys = data.keys()
        result = {}
        for item in keys:
            result[item] = str(data[item])
        result['id'] = str(self.key.id())
        return result


class Guestbook(ndb.Model):
    name = DEFAULT_GUESTBOOK_NAME


    def __init__(self, guesbook_name):
        self.name = guesbook_name

    def get_page(self, cursor_fetch_num=FETCH_MAX, str_cursor=None):
        if cursor_fetch_num <= 0:
            greetings = None
            next_cursor = None
            more = None
        try:
            guestbook_key = self.guestbook_key()
            cursor = Cursor(urlsafe=str_cursor)
            query = Greeting.query(ancestor=guestbook_key).order(-Greeting.date)
            (greetings, next_cursor, more) = query.fetch_page(cursor_fetch_num, start_cursor=cursor)
        except:
            greetings = None
            next_cursor = None
            more = None
        return greetings, next_cursor, more


    def get_lastest_greeting(self, number_of_greeting=10):
        greetings = memcache.get(self.name)
        if greetings is None:
            greetings_query = Greeting.query(ancestor=self.guestbook_key()).order(-Greeting.date)
            greetings = greetings_query.fetch(number_of_greeting)
            memcache.add(self.name, greetings, 600)
            return greetings
        else:
            return greetings


    def guestbook_key(self):
        '''Constructs a Datastore key for a Guestbook entity with guestbook_name.'''
        return ndb.Key('Guestbook', self.name)


    @ndb.transactional
    def put_greeting(self, content, author, user, title):
        greeting = Greeting().get_greetings_object(self.name)
        greeting.content = content
        greeting.author = author
        cache_result = None

        if greeting.put():
            cache_result = memcache.delete(self.name)
            if user:
                taskqueue.add(
                    method='GET',
                    url='/mail',
                    params={'title': title, 'author': author})
            return cache_result
        return cache_result


    # def sendmail(self, user, title, author):
    #     if user:
    #         taskqueue.add(
    #             method='GET',
    #             url='/mail',
    #             params={'title': title, 'author': author})


    @staticmethod
    def get_default_name():
        return DEFAULT_GUESTBOOK_NAME

    @ndb.transactional
    def delete_message(self, author, user, is_superuser, id):
        author_name = ndb.Key('Guestbook', self.name, Greeting, int(id)).get().author
        if (author == author_name):
            ndb.Key('Guestbook', self.name, Greeting, int(id)).delete()
            return memcache.delete(self.name)

        # if author == user:
        #     greetings = Greeting.query(ancestor=self.guestbook_key()).order(-Greeting.date).fetch(10)
        #     for greeting in greetings:
        #         ndb.Key('Guestbook', int(id)).delete()

    @ndb.transactional
    def update_greeting_by_id(self, author, user, is_superuser, id, greeting_content):
        obj = ndb.Key('Guestbook', self.name, Greeting, int(id)).get()
        obj.content = greeting_content
        obj.updated_by = author
        cache_result = None
        if (obj.author == author):
            if obj.put():
                return memcache.delete(self.name)
        return cache_result


    def get_item_by_id(self, id):
        obj = ndb.Key('Guestbook', self.name, Greeting, int(id)).get()
        return obj


    def convert_list_to_dict(self, list):
        greetings = list
        result_list = []
        for greeting_item in greetings:
            result_list.append(greeting_item.convert_item_to_dict())
        return result_list

    def get_all_greetings(self):
        greetings = Greeting.query(ancestor=self.guestbook_key()).order(-Greeting.date).fetch()
        return greetings