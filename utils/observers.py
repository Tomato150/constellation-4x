class Observer:
    def on_notify(self, object, event):
        """
        Abstract event for the sake of the class. This gets called whenever one of it's subjects fires an event
        
        :param object: The Subject
        :param event: The Event
        """
        pass


class Subject:
    def __init__(self):
        self.__observers = []

    def add_observer(self, observer):
        """
        Adds an observer to the list. Basically the bind function :3
        
        :param observer: An observer object.
        """
        self.__observers.append(observer)

    def remove_observer(self, observer):
        """
        Removes an observer object from the on_notify list
        
        :param observer: An observer object
        """
        self.__observers.remove(observer)

    def notify(self, event):
        """
        Sends out an event to all Observers watching this bad boy
        
        :param event: The event message to be sent out
        """
        for observer in self.__observers:
            observer.on_notify(self, event)
