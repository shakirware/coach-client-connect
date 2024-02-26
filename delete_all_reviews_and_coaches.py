from Users.models import Coach
from Reviews.models import Review

# Retrieve all coach profiles
coaches = Coach.objects.all()

# Iterate through coach profiles and delete each one along with their reviews
for coach in coaches:
    # Delete associated reviews
    reviews = Review.objects.filter(coach=coach)
    reviews.delete()

    # Delete the coach profile
    coach.delete()

print("All coach profiles and their associated reviews have been deleted.")

