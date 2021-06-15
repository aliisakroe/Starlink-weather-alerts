'''Implements the observer pattern
'''

class Event(object):
    def __init__(self, *args, **kwargs):
        pass

class Observable(object):
    def __init__(self):
        #holds callback methods
        self.callbacks = []

    def subscribe(self, callback):
        '''Other classes can provide their methods
        to call when an Event is fired
        '''
        self.callbacks.append(callback)

    def fire(self, event, **attrs):
        '''Will trigger registered callback methods
        '''
        e = event(attrs.items())
        e.source = self
        for fn in self.callbacks:
            fn(e)