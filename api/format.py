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