import uuid
import pytz
from dateutil import parser
from datetime import datetime, timedelta

from django.utils import timezone
from django.contrib.gis.geos import GEOSGeometry
from api.helpers import get_address_from_latlng

from users.models import User
from feedback.models import Feedback, FeedbackCategory
from activities.models import Activity, Location
from reports.models import Report, ReportCategory
from friends.models import Group
from friendship.models import Friend, FriendshipRequest

class Generator:
    def create_test_user(self, name=None, email=None, password=None):

        first_name = name.split(' ')[0] if name else str(uuid.uuid4())[:10]
        last_name = name.split(' ')[1] if name and len(name.split(' ') > 1) else str(uuid.uuid4())[:15]

        email = email if email else first_name + "@example.com"

        password = password if password else str(uuid.uuid4())[:8]

        user = User.objects.create_user(name=first_name + ' ' + last_name,
                                             email=email,
                                             password=password,
                                             is_active=True)
        return user

    def create_feedback(self, subject=None, details=None, category=None, user=None):
        if not category:
            category = FeedbackCategory.objects.all().order_by('?')[0]

        if not user:
            user = self.create_test_user()

        data = {
            'subject': subject if subject else str(uuid.uuid4())[:15],
            'details': details if details else str(uuid.uuid4()),
            'category': category,
            'user': user
        }

        feedback = Feedback.objects.create(**data)

        return feedback

    def create_activity(self, creator=None, name=None, start_date=None, end_date=None, nsfw=False, alcohol=False, handicap=False,
                        minimum_age=0, maximum_age=65, groups=[], price=None, duration=None):
        created_by = self.create_test_user() if not creator else creator
        name = name if name else str(uuid.uuid4())[:24]
        description = str(uuid.uuid4())

        latitude = 41.757595
        longitude = -111.834331
        address = get_address_from_latlng(latitude, longitude)
        point = GEOSGeometry('POINT(%s %s)' % (longitude, latitude), srid=4326)

        location, created = Location.objects.get_or_create(address=address,
                                                           latitude=latitude,
                                                           longitude=longitude,
                                                           point=point)

        activity = Activity(
            name=name,
            description=description,
            created_by=created_by,
            minimum_age=minimum_age,
            maximum_age=maximum_age,
            handicap_friendly=handicap,
            is_nsfw=nsfw,
            alcohol_present=alcohol,
            price=price,
            duration=duration
        )
        activity.location = location
        activity.save()


        return activity

    def create_report(self, user=None, activity=None, category=None):
        activity = activity if activity else self.create_activity()
        user = user if user else self.create_test_user()
        category = category if category else ReportCategory.objects.all().order_by('?')[0]

        report = Report.objects.create(activity=activity,
                                       reporter=user,
                                       category=category,
                                       detail=str(uuid.uuid4()))

        return report

    def create_friend_group(self, user=None, name=None, friend=None, friends=0):
        user = user if user else self.create_test_user()
        name = str(uuid.uuid4())[:12]

        group = Group.objects.create(creator=user, name=name)

        if friend:
            group.friends.add(friend)

        if friends > 0:
            for i in range(friends):
                f = self.create_test_user()
                group.friends.add(f)

        return group

    def create_friend(self, user=None, friend=None):
        user = user if user else self.create_test_user()
        friend = friend if friend else self.create_test_user()

        friend_request = self.create_friend_request(user, friend)
        friend_request.accept()


    def create_friend_request(self, user=None, friend=None):
        user = user if user else self.create_test_user()
        friend = friend if friend else self.create_test_user()

        friend_request = Friend.objects.add_friend(
            user,
            friend
        )

        return friend_request