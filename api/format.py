from .models import *
from THUeat.settings import BASE_URL

def format_navigations_canteen_list(canteen_list):
    datalist = []
    for canteen in canteen_list:
        data = {}
        data["canteenID"] = canteen.canteenID
        data["canteenName"] = canteen.canteenName
        data["canteenType"] = canteen.canteenType
        datalist.append(data)
    return datalist

def format_navigations_dish_list(dish_list):  
    datalist = []
    for dish in dish_list:
        data = {}
        data["dishID"] = dish.dishID
        data["dishName"] = dish.dishName
        datalist.append(data)
    return datalist

def format_canteen(canteen):
    data = {}
    data["canteenName"] = canteen.canteenName
    data["canteenPhone"] = canteen.canteenPhone
    data["canteenAddress"] = canteen.canteenAddress
    data["canteenIntro"] = canteen.canteenIntro
    data["canteenImage"] = BASE_URL + canteen.canteenImage.url
    data["canteenType"] = canteen.canteenType
    data["canteenOperationTime"] = canteen.canteenOperationTime
    stall_list = Stall.objects.filter(canteenID=canteen.pk, is_active=True)
    data["canteenRate"] = round(stall_list.exclude(stallRate=0).aggregate(models.Avg('stallRate'))["stallRate__avg"],1)
    stalls = []
    for stall in stall_list:
        stall_dic = {}
        stall_dic["stallID"] = stall.stallID
        stall_dic["stallRate"] = stall.stallRate
        stall_dic["stallRateNumber"] = stall.stallRateNum
        stall_dic["stallImages"] = ""
        image_list = StallImage.objects.filter(stallID=stall.pk)
        try:
            stall_dic["stallImages"] = BASE_URL + image_list[0].stallImage.url
        except:
            pass
        stall_dic["stallName"] = stall.stallName
        review_list = Review.objects.filter(stallID=stall.pk)
        reviews = []
        for review in review_list:
            reviews.append(
                {
                    "likes":review.reviewLikes,
                    "comment":review.reviewComment
                }
            )            
        bestreview = sorted(reviews,key=lambda x:x['likes'],reverse=True)
        if bestreview:
            stall_dic["stallBestComment"] = bestreview[0]["comment"]
        else:
            stall_dic["stallBestComment"] = ""
        stalls.append(stall_dic)
    data["stalls"] = stalls
    return data

def format_recommend_stall_list(stall_list):    
    datalist = []
    for stall in stall_list:
        data = {}
        data["stallID"] = stall.stallID
        data["stallRate"] = stall.stallRate
        data["stallRateNumber"] = stall.stallRateNum
        image_list = StallImage.objects.filter(stallID=stall.pk)
        data["stallImages"] = ""
        try:
            data["stallImages"] = BASE_URL + image_list[0].stallImage.url
        except:
            pass
        data["stallName"] = stall.stallName
        data["canteenName"] = stall.canteenID.canteenName
        review_list = Review.objects.filter(stallID=stall.pk)
        reviews = []
        for review in review_list:
            reviews.append(
                {
                    "likes":review.reviewLikes,
                    "comment":review.reviewComment
                }
            )            
        bestreview = sorted(reviews,key=lambda x:x['likes'],reverse=True)
        if bestreview:
            data["stallBestComment"] = bestreview[0]["comment"]
        else:
            data["stallBestComment"] = ""        
        datalist.append(data)
    return datalist

def dish_available_time_decode(time):
    time_list = time.split(',')
    return time_list

def format_stall_dish(dish,user,login):
    data = {}
    data["dishID"] = dish.dishID
    data["dishName"] = dish.dishName
    data["dishImages"] = ""
    image_list = DishImage.objects.filter(dishID=dish.pk)
    try:
        data["dishImages"] = BASE_URL + image_list[0].dishImage.url
    except:
        pass
    data["dishPrice"] = '{0:.2f}'.format(dish.dishPrice)
    data["dishLikes"] = dish.dishLikes
    if login:
        if LikeDish.objects.filter(userID=user.pk, dishID=dish.pk).exists():
            data["myDishLike"] = True
        else:
            data["myDishLike"] = False
    else:
        data["myDishLike"] = None
    data["dishAvailableTime"] = dish_available_time_decode(dish.dishAvailableTime)
    dishreviews = []
    dishreview_list = DishReview.objects.filter(dishID=dish.pk)
    for dishreview in dishreview_list:
        dishreviews.append(
            {
                "likes":dishreview.reviewID.reviewLikes,
                "comment":dishreview.reviewID.reviewComment
            }
        )
    bestreview = sorted(dishreviews,key=lambda x:x['likes'],reverse=True)
    if bestreview:
        bestreview = bestreview[0]["comment"]
    else:
        bestreview = ""
    data["dishBestComment"] = bestreview
    return data

def format_stall_review(review,user,login):
    data = {}
    data["userName"] = review.userID.userName
    data["userImage"] = BASE_URL + Student.objects.get(user=review.userID.pk).userImage.url
    data["reviewID"] = review.reviewID
    data["reviewDateTime"] = review.reviewDateTime
    data["rate"] = review.rate
    data["reviewImages"] = [BASE_URL + reviewimage.reviewImages.url for reviewimage in ReviewImage.objects.filter(reviewID=review.pk)]
    data["reviewComment"] = review.reviewComment
    data["reviewTags"] = review_tags_decode(review.reviewTags)
    data["reviewLikes"] = review.reviewLikes
    if login:
        if LikeReview.objects.filter(userID=user.pk,reviewID=review.pk).exists():
            data["myReviewLike"] = True
        else:
            data["myReviewLike"] = False
    else:
        data["myReviewLike"] = None
    data["reply"] = review.reply
    data["replyDateTime"] = ""
    data["replyComment"] = ""
    if review.reply:
        reply = ReplyByStaff.objects.get(parent_reviewID=review.pk)
        data["replyDateTime"] = reply.replyDateTime
        data["replyComment"] = reply.replyContent
    dishreview_list = DishReview.objects.filter(reviewID=review.pk)
    dishes = []
    for dishreview in dishreview_list:
        dish = Dish.objects.get(dishID=dishreview.dishID.pk)
        dishes.append({
            "dishID": dish.dishID,
            "dishName": dish.dishName,
        })
    data["dishes"] = dishes    
    return data    

def operation_time_decode(time):
    session = time.split('/')
    operation_time_list = []
    for each in session:
        if "B" in each:
            session_data = {}
            start_time = each.split('-')[1]
            end_time = each.split('-')[2]
            session_data["name"] = "早餐"
            session_data["startTime"] = start_time
            session_data["endTime"] = end_time
            operation_time_list.append(session_data)
        elif "L" in each:
            session_data = {}
            start_time = each.split('-')[1]
            end_time = each.split('-')[2]
            session_data["name"] = "午餐"
            session_data["startTime"] = start_time
            session_data["endTime"] = end_time
            operation_time_list.append(session_data)
        elif "D" in each:
            session_data = {}
            start_time = each.split('-')[1]
            end_time = each.split('-')[2]
            session_data["name"] = "晚餐"
            session_data["startTime"] = start_time
            session_data["endTime"] = end_time
            operation_time_list.append(session_data)
        elif "S" in each:
            session_data = {}
            start_time = each.split('-')[1]
            end_time = each.split('-')[2]
            session_data["name"] = "宵夜"
            session_data["startTime"] = start_time
            session_data["endTime"] = end_time
            operation_time_list.append(session_data)
        elif "C" in each:
            session_data = {}
            start_time = each.split('-')[1]
            end_time = each.split('-')[2]
            session_data["name"] = "自定义"
            session_data["startTime"] = start_time
            session_data["endTime"] = end_time
            operation_time_list = [session_data]
            break
    return operation_time_list

def format_stall(stall, user, login):
    data = {}
    data["stallName"] = stall.stallName
    data["stallFloor"] = stall.stallFloor
    data["stallDescribe"] = stall.stallDescribe
    image_list = StallImage.objects.filter(stallID=stall.pk)
    data["stallImages"] = [BASE_URL + image.stallImage.url for image in image_list]
    data["stallRate"] = stall.stallRate
    data["stallRateNumber"] = stall.stallRateNum
    data["stallOperationtime"] = operation_time_decode(stall.stallOperationtime)
    dishes = []
    dish_list = Dish.objects.filter(stallID=stall.pk, is_active=True)  # find dishes
    for dish in dish_list:
        dishes.append(format_stall_dish(dish,user,login))
    data["dishes"] = dishes
    reviews = []
    review_list = Review.objects.filter(stallID=stall.pk)
    for review in review_list:
        reviews.append(format_stall_review(review,user,login))
    data["reviews"] = reviews
    return data




def format_review(review):
    image_list = ReviewImage.objects.filter(reviewID=review.pk)
    dishreview_list = DishReview.objects.filter(reviewID=review.pk)
    data = {}
    data["reviewID"] = review.reviewID
    data["reviewDateTime"] = review.reviewDateTime
    data["reviewComment"] = review.reviewComment
    data["reviewImages"] = [BASE_URL + image.reviewImages.url for image in image_list]
    data["reviewTags"] = review_tags_decode(review.reviewTags)
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
    data["rate"] = review.rate
    data["reviewComment"] = review.reviewComment
    data["reviewImages"] = [BASE_URL + image.reviewImages.url for image in image_list]
    data["reviewTags"] = review_tags_decode(review.reviewTags)
    data["reviewLikes"] = review.reviewLikes
    data["reply"] = review.reply
    data["replyDateTime"] = ""
    data["replyComment"] = ""
    dishes = []
    if review.reply:
        reply = ReplyByStaff.objects.get(parent_reviewID=review.pk)
        data["replyDateTime"] = reply.replyDateTime
        data["replyComment"] = reply.replyContent
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
    data["dishPrice"] = '{0:.2f}'.format(dish.dishPrice)
    image_list = DishImage.objects.filter(dishID=dish.pk)
    data["dishImages"] = [BASE_URL + image.dishImage.url for image in image_list]
    data["dishLikes"] = dish.dishLikes
    data["dishAvailableTime"] = dish_available_time_decode(dish.dishAvailableTime)
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

def review_tags_decode(tags):
    if tags:
        return tags.split(",")
    else:
        return []

def format_dish_review(dishreview,user,login):
    data = {}
    data["userName"] = dishreview.reviewID.userID.userName
    data["userImage"] = BASE_URL + Student.objects.get(user=dishreview.reviewID.userID.pk).userImage.url
    data["reviewID"] = dishreview.reviewID.pk
    data["reviewDateTime"] = dishreview.reviewID.reviewDateTime
    data["rate"] = dishreview.reviewID.rate
    data["reviewImages"] = [BASE_URL + reviewimage.reviewImages.url for reviewimage in ReviewImage.objects.filter(reviewID=dishreview.reviewID.pk)]
    data["reviewComment"] = dishreview.reviewID.reviewComment
    data["reviewTags"] = review_tags_decode(dishreview.reviewID.reviewTags)
    data["reviewLikes"] = dishreview.reviewID.reviewLikes

    if login:
        if LikeReview.objects.filter(userID=user.pk,reviewID=dishreview.reviewID.pk).exists():
            data["myReviewLike"] = True
        else:
            data["myReviewLike"] = False
    else:
        data["myReviewLike"] = None

    data["reply"] = dishreview.reviewID.reply
    data["replyDateTime"] = ""
    data["replyComment"] = ""
    if dishreview.reviewID.reply:
        reply = ReplyByStaff.objects.get(parent_reviewID=dishreview.reviewID.pk)
        data["replyDateTime"] = reply.replyDateTime
        data["replyComment"] = reply.replyContent
    return data

def format_recommend_dish(dish,user,login):
    data = {}
    data["dishID"] = dish.dishID
    data["dishName"] = dish.dishName
    # data["dishIntro"] = dish.dishDescribe
    data["dishPrice"] = '{0:.2f}'.format(dish.dishPrice)
    image_list = DishImage.objects.filter(dishID=dish.pk)
    data["dishImages"] = ""
    try:
        data["dishImages"] = BASE_URL + image_list[0].dishImage.url
    except:
        pass
    data["dishLikes"] = dish.dishLikes
    data["dishAvailableTime"] = dish_available_time_decode(dish.dishAvailableTime)
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
        dishreviews.append(
            {
                "likes":dishreview.reviewID.reviewLikes,
                "comment":dishreview.reviewID.reviewComment
            }
        )
    bestreview = sorted(dishreviews,key=lambda x:x['likes'],reverse=True)
    if bestreview:
        bestreview = bestreview[0]["comment"]
    else:
        bestreview = ""
    data["dishBestComment"] = bestreview
    data["stallID"] = dish.stallID.pk
    data["stallName"] = dish.stallID.stallName
    data["canteenName"] = dish.stallID.canteenID.canteenName
    return data

def format_notice_list(notice_list):
    datalist = []
    for notice in notice_list:
        data = {}
        data["noticeTitle"] = notice.noticeTitle
        data["noticeWords"] = notice.noticeWords
        data["noticeImage"] = BASE_URL + notice.noticeImage.url
        datalist.append(data)
    return datalist