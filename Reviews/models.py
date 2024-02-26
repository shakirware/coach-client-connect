from django.db import models
from Users.models import Coach, User

class Review(models.Model):
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.author.username} for {self.coach}"
