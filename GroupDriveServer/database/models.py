from mongoengine import Document
from mongoengine.fields import (
    StringField,
    ReferenceField,
    ListField,
    FloatField,
    DateTimeField,
    BooleanField,
    IntField,
)
from datetime import datetime as dt
from mongoengine.errors import DoesNotExist
from json import dumps


class User(Document):
    googleID = StringField()
    photoURL = StringField()
    name = StringField(required=True)
    # preferences = DictField(required=True)


class Trip(Document):
    tripID = IntField()
    title = StringField()
    creator = ReferenceField("User")
    meetingPoint = StringField(required=True)
    meetingPointWazeUrl = StringField(required=True)
    description = StringField(required=True)
    participants = ListField(ReferenceField("User"))
    dateTime = DateTimeField(required=True)
    isTripToday = BooleanField(required=True, default=False)

    def updateTrip(self):
        if self.dateTime.date() == dt.today().date():
            self.isTripToday = True
            self.save()

    def isUserJoined(self, user):
        for p in self.participants:
            if p == user:
                return True
        return False

    def addUser(self, user):
        self.participants.append(user)
        self.save()

    def getParticipantsCoordinates(self):
        coordinates = []
        for p in self.participants:
            try:
                c = UserLiveGPSCoordinates.objects().get(user=p)
            except DoesNotExist:
                continue
            coordinates += [c]
        return dumps(coordinates)


class UserLiveGPSCoordinates(Document):

    user = ReferenceField("User")
    trip = ReferenceField("Trip")
    longitude = FloatField(required=True)
    latitude = FloatField(required=True)

    def isValid(self):
        joinedTrip = self.trip.isUserJoined(self.user)
        isTripToday = self.trip.isTripToday
        return joinedTrip and isTripToday
