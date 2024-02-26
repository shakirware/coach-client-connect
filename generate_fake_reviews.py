from faker import Faker
import random
from Reviews.models import Review
from Users.models import Coach

fake = Faker()

# Get all coach objects
coaches = Coach.objects.all()

for coach in coaches:
    print(f"Processing coach: {coach.user.username}")

    # Generate 0 to 5 fake reviews for each coach
    for _ in range(random.randint(5, 10)):  # Each coach gets 0 to 5 reviews
        rating = random.randint(1, 5)  # Random rating between 1 and 5
        comment = fake.paragraph()  # Random comment text
        print(f"Creating review for coach: {coach.user.username}, Rating: {rating}")

        # Create a fake review
        Review.objects.create(coach=coach, rating=rating, comment=comment)

