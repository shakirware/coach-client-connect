from Users.models import Coach, User
from faker import Faker

fake = Faker()

# Create a number of fake coaches
for _ in range(10):  # Adjust the number as needed
    user = User.objects.create_user(username=fake.user_name(), password="password")
    Coach.objects.create(
        user=user,
        full_name=fake.name(),
        qualifications=",".join(fake.words(nb=5)),
        experience=fake.text(),
        specializations="Streetlifting",
        bio=fake.text(),
        rates=f"{fake.random_number(digits=2)} per hour",
        languages=",".join(fake.words(nb=2)),
        availability="Weekdays",
        location=fake.city(),
        awards=fake.sentence()
    )

for _ in range(10):  # Adjust the number as needed
    user = User.objects.create_user(username=fake.user_name(), password="password")
    Coach.objects.create(
        user=user,
        full_name=fake.name(),
        qualifications=",".join(fake.words(nb=5)),
        experience=fake.text(),
        specializations="Powerlifting",
        bio=fake.text(),
        rates=f"{fake.random_number(digits=2)} per hour",
        languages=",".join(fake.words(nb=2)),
        availability="Weekdays",
        location=fake.city(),
        awards=fake.sentence()
    )