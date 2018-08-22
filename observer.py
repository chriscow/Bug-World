

class Publisher():
    def __init__(self, events):
        # maps event names to subscribers
        # str -> dict
        self.events = { event : dict()
            for event in events }

    def get_subscribers(self, event):
        return self.events[event]

    def register(self, event, who, callback=None):
        """
        Clients can register for event notification. If callback is None,
        the publisher will attempt to call a function on the subscriber
        named the same as the event string.

        :param event: (string) Name of the event
        :param who: (class instance) Unique object instance receiving the event
        :param callback: (function) Optional function to be called when fired
        """
        if callback == None:
            callback = getattr(who, event)

        self.get_subscribers(event)[who] = callback

    def unregister(self, event, who):
        del self.get_subscribers(event)[who]

    def dispatch(self, event, *args):
        for subscriber, callback in self.get_subscribers(event).items():
            callback(*args)