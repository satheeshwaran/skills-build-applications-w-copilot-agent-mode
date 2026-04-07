from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.db import transaction

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        with transaction.atomic():
            # Clear existing data
            Leaderboard.objects.all().delete()
            Activity.objects.all().delete()
            Workout.objects.all().delete()
            User.objects.all().delete()
            Team.objects.all().delete()

            # Create teams
            marvel = Team.objects.create(name='Marvel', description='Marvel superheroes')
            dc = Team.objects.create(name='DC', description='DC superheroes')

            # Create users
            users = [
                User.objects.create(name='Spider-Man', email='spiderman@marvel.com', team=marvel),
                User.objects.create(name='Iron Man', email='ironman@marvel.com', team=marvel),
                User.objects.create(name='Captain America', email='cap@marvel.com', team=marvel),
                User.objects.create(name='Batman', email='batman@dc.com', team=dc),
                User.objects.create(name='Superman', email='superman@dc.com', team=dc),
                User.objects.create(name='Wonder Woman', email='wonderwoman@dc.com', team=dc),
            ]

            # Create activities
            Activity.objects.create(user=users[0], type='Running', duration=30, date='2026-04-01')
            Activity.objects.create(user=users[1], type='Cycling', duration=45, date='2026-04-02')
            Activity.objects.create(user=users[3], type='Swimming', duration=60, date='2026-04-03')

            # Create workouts
            w1 = Workout.objects.create(name='Strength Training', description='Full body workout')
            w2 = Workout.objects.create(name='Cardio Blast', description='High intensity cardio')
            w1.suggested_for.set([users[0], users[1], users[2]])
            w2.suggested_for.set([users[3], users[4], users[5]])

            # Create leaderboard
            Leaderboard.objects.create(user=users[0], score=100, rank=1)
            Leaderboard.objects.create(user=users[1], score=90, rank=2)
            Leaderboard.objects.create(user=users[3], score=95, rank=1)

            self.stdout.write(self.style.SUCCESS('Database populated with test data.'))
