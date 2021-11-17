from django.contrib import admin
# from .models import User
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Canteen)
admin.site.register(Stall)
admin.site.register(StallImage)
admin.site.register(Dish)
admin.site.register(Review)
admin.site.register(ReviewImage)
admin.site.register(DishReview)
admin.site.register(LikeReview)
admin.site.register(LikeDish)
admin.site.register(UserStall)
admin.site.register(Ratings)
admin.site.register(Student)
admin.site.register(Notice)
admin.site.register(ReplyByStaff)