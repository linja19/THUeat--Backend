from .models import *

def format_review(review):
    image_list = ReviewImage.objects.filter(reviewID=review.pk)
    dishreview_list = DishReview.objects.filter(reviewID=review.pk)
    data = {}
    data["reviewID"] = review.reviewID
    data["reviewDateTime"] = review.reviewDateTime
    data["reviewComment"] = review.reviewComment
    data["reviewImages"] = [image.reviewImages.url for image in image_list]
    data["reviewTags"] = review.reviewTags
    data["reviewLikes"] = review.reviewLikes
    data["reply"] = review.reply
    dishes = []
    for dishreview in dishreview_list:
        dish = Dish.objects.get(dishID=dishreview.dishID.pk)
        dishes.append({
            "dishID":dish.dishID,
            "dishName":dish.dishName,
        })
    data["dishes"] = dishes

    return data

def format_myreview(review):
    image_list = ReviewImage.objects.filter(reviewID=review.pk)
    dishreview_list = DishReview.objects.filter(reviewID=review.pk)
    data = {}
    data["stallID"] = review.stallID.pk
    data["stallName"] = Stall.objects.get(stallID=review.stallID.pk).stallName
    data["reviewID"] = review.reviewID
    data["reviewDateTime"] = review.reviewDateTime
    data["reviewComment"] = review.reviewComment
    data["reviewImages"] = [image.reviewImages.url for image in image_list]
    data["reviewTags"] = review.reviewTags
    data["reviewLikes"] = review.reviewLikes
    data["reply"] = review.reply
    dishes = []
    for dishreview in dishreview_list:
        dish = Dish.objects.get(dishID=dishreview.dishID.pk)
        dishes.append({
            "dishID": dish.dishID,
            "dishName": dish.dishName,
        })
    data["dishes"] = dishes

    return data

def format_myratings(ratings):
    data = {}
    data["stallID"] = ratings.stallID.pk
    data["stallName"] = Stall.objects.get(stallID=ratings.stallID.pk).stallName
    data["myRate"] = ratings.stallRate
    return data

def format_dish(dish,user,login):
    data = {}
    data["dishName"] = dish.dishName
    data["dishIntro"] = dish.dishDescribe
    data["dishPrice"] = dish.dishPrice
    data["dishImage"] = dish.dishImage.url
    data["dishLikes"] = dish.dishLikes
    data["dishAvailableTime"] = dish.dishAvailableTime
    if login:
        if LikeDish.objects.filter(userID=user.pk, dishID=dish.dishID).exists():
            data["myDishLike"] = True
        else:
            data["myDishLike"] = False
    else:
        data["myDishLike"] = None
    dishreviews = []
    dishreview_list = DishReview.objects.filter(dishID=dish.dishID)
    for dishreview in dishreview_list:
        dishreviews.append(format_dish_review(dishreview,user,login))
    data["reviews"] = dishreviews
    return data

def format_dish_review(dishreview,user,login):
    data = {}
    data["userName"] = dishreview.reviewID.userID.userName
    data["userImage"] = Student.objects.get(user=dishreview.reviewID.userID.pk).userImage.url
    data["reviewID"] = dishreview.reviewID.pk
    data["reviewDateTime"] = dishreview.reviewID.reviewDateTime
    data["reviewImages"] = [reviewimage.reviewImages.url for reviewimage in ReviewImage.objects.filter(reviewID=dishreview.reviewID.pk)]
    data["reviewComment"] = dishreview.reviewID.reviewComment
    data["reviewTags"] = dishreview.reviewID.reviewTags
    data["reviewLikes"] = dishreview.reviewID.reviewLikes

    if login:
        if LikeReview.objects.filter(userID=user.pk,reviewID=dishreview.reviewID.pk).exists():
            data["myReviewLike"] = True
        else:
            data["myReviewLike"] = False
    else:
        data["myReviewLike"] = None

    data["reply"] = dishreview.reviewID.reply
    if dishreview.reviewID.reply:
        reply = ReplyByStaff.objects.get(parent_reviewID=dishreview.reviewID.pk)
        data["replyDateTime"] = reply.replyDateTime
        data["replyComment"] = reply.replyContent
    return data