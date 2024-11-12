from django.core.management.base import BaseCommand
from hotelapp.models import Room

class Command(BaseCommand):
    help = 'Create rooms for the hotel'

    def handle(self, *args, **kwargs):
        Room.objects.all().delete()  # Optional: Clear existing rooms

        room_number = 1
        for floor in range(1, 4):  # 3 floors
            for i in range(4):  # 4 rooms per floor
                bedrooms = 2 if i < 2 else 1  # First 2 rooms have 2 bedrooms, next 2 have 1 bedroom
                Room.objects.create(
                    number=room_number,
                    floor=floor,
                    bedrooms=bedrooms,
                    is_available=True
                )
                room_number += 1

        self.stdout.write(self.style.SUCCESS('Successfully created rooms')) 