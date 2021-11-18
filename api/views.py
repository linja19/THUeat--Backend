from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.parsers import JSONParser
from .models import User, Token
from .serializer import *
from .format import *
import re

# Create your views here.

def get_user_by_request_token(request):
    authorization = request.META.get('HTTP_AUTHORIZATION', '')  # get authorization from request header
    token = re.match('Token (.*)', authorization)  # find token in authorization
    if token:
        token = token.group(1)

    user = Token.objects.get(key=token).user  # get user by using token
    return user

def get_student_by_user(user):
    user_pk = user.pk                               # get user primary key
    student = Student.objects.get(user=user_pk)     # get student by using user primary key
    return student

def check_email_is_valid(email):
    if Student.objects.filter(userEmail=email).exists():    # check email is exist
        return False
    else:
        return True

def check_dish_is_valid(dish_list):                     # check a dish is existed or not
    count = 1
    for dish in dish_list:
        if not Dish.objects.filter(dishID=dish).exists():
            return False
    return count

@api_view(['GET'])
def userlist(request):                              # check all user
    users = User.objects.all()                      # get all user from user model
    serializer = UserRegisterSerializer(users,many=True)    # serialize User model to UserSerializer
    return Response(serializer.data)

@api_view(['POST'])
def user_register(request):
    if request.method=='POST':
        data = {}                                   # response data
        user_data = {                               # userName,password in User model
            "userName":request.data["userName"],
            "password":request.data["password"]
        }
        userserializer = UserRegisterSerializer(data=user_data) # create userserializer with user_data
        if (userserializer.is_valid())&(check_email_is_valid(request.data["userEmail"])):    # check userserializer is_valid (check user_data), check email is exist
            user = userserializer.save()                # save userserializer (save user to database)
                                                        # create user first as studentserializer need linked to user to create
            student_data = {                            # userEmail in Student model
                "user": user.pk,
                "userEmail": request.data["userEmail"]
            }
            studentserializer = StudentRegisterSerializer(data=student_data)    # create studentserializer with student data
            if studentserializer.is_valid():                                    # check studentserializer is_valid
                studentserializer.save()                                        # save studentserializer (save student to database)
                data['code'] = 200                                              # successful message
                data['message'] = 'successful operation'
                token = Token.objects.get(user=user).key                        # find user in Token model and get its token
                data['data'] = {
                        "token":token,
                    }
            else:
                data['code'] = 400
                data['message'] = "user with this userEmail already exists."    # error userEmail exists
        else:
            data['code'] = 400
            messages = []
            if User.objects.filter(userName=request.data["userName"]).exists(): # error userName exists
                messages.append("用户名已存在")
            if Student.objects.filter(userEmail=request.data["userEmail"]).exists():    # error userEmail exist
                messages.append("用户邮箱已存在")
            data['message'] = messages
        return Response(data)

@api_view(['POST'])
def user_login(request):
    data = {}
    if request.method=='POST':
        userName = request.data['userName']                     # get userName
        password = request.data['password']                     # get password
        try:
            user = User.objects.get_by_natural_key(userName)    # get user by using userName
            if user.check_password(password):                   # check password
                data['code'] = 200
                data['message'] = 'successful operation'
                data['data'] = {
                    "token": Token.objects.get(user_id=user.id).key  # get token by using user_id
                }
            else:
                data['code'] = 404
                data['message'] = '密码错误'
        except:
            data['code'] = 404
            data['message'] = '用户不存在'
        return Response(data)

@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_details(request):
    data = {}
    if request.method=='GET':
        user = get_user_by_request_token(request)                    # get user by using token
        student = get_student_by_user(user)                          # get student
        data['code'] = 200
        data['message'] = 'successful operation'
        data['data'] = {
            "userName": user.userName,
            "userEmail": student.userEmail,
            "userImage": student.userImage.url,
            "userPhone": user.userPhone
        }
        review_list = Review.objects.filter(userID=user.pk)         # find user review
        myReviews = []
        for review in review_list:
            myReviews.append(format_myreview(review))               # add review to myReviews
        data["data"]["myReviews"] = myReviews
        ratings_list = Ratings.objects.filter(userID=user.pk)       # find user ratings
        myRatings = []
        for ratings in ratings_list:
            myRatings.append(format_myratings(ratings))             # add ratings to myRatings
        data["data"]["myRatings"] = myRatings

        return Response(data)
    elif request.method=='POST':                                    # update user details
        user = get_user_by_request_token(request)                   # get user by token
        student = get_student_by_user(user)                         # get student
        user_data = {
            "userName": request.data["userName"],
            "userPhone": request.data["userPhone"]
        }
        student_data = {
            "user": user.pk,
            "userEmail": request.data["userEmail"],
            # "userImage": request.data["userImage"]
        }
        userserializer = UpdateUserSerializer(user,data=user_data)  # create serializer
        studentserializer = UpdateStudentSerializer(student,data=student_data)
        if (userserializer.is_valid())&(studentserializer.is_valid()):  # check serializer (check data)
            userserializer.save()                    # save serializer (update data)
            studentserializer.save()
            data['code'] = 200
            data['message'] = 'successful operation'
        else:
            data['code'] = 400
            messages = []
            for key, value in userserializer.errors.items():    # get error from serializer
                messages.append(value[0])
            for key, value in studentserializer.errors.items():
                messages.append(value[0])
            data['message'] = messages
        return Response(data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_password(request):
    data = {}
    user = get_user_by_request_token(request)               # get user by token
    user_data = {
        "password": request.data["password"]
    }
    if request.method=='POST':
        serializer = UpdateUserPasswordSerializer(user,data=user_data)      # create serializer
        if (serializer.is_valid())&(user.check_password(request.data['oldPassword'])):      # check old password
            serializer.save()                    # save serializer (update password)
            data['code'] = 200
            data['message'] = 'successful operation'
        else:
            data['code'] = 400
            data['message'] = '旧密码错误'
        return Response(data)


@api_view(["POST","GET","DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def reviews(request):
    data = {}
    user = get_user_by_request_token(request)               # get user by token
    if request.method=='POST':
        try:                                                # find stallID in url
            stallID = request.query_params["stallID"]
        except:
            data["code"] = 404
            data["messages"] = "stallID not found"
            return Response(data)
        review_data = {
            "reviewComment":request.data["reviewComment"],
            "reviewTags":request.data["reviewTags"],
            "userID":user.pk,
            "stallID":stallID
        }
        reviewserializer = CreateReviewSerializer(data=review_data)     # create reviewserializer
        if (reviewserializer.is_valid())&(check_dish_is_valid(request.data["dishID"])):
            review = reviewserializer.save()                            # save serializer to create primary key
            for each in request.data["reviewImages"]:                   # for each image,create serializer and save
                reviewimages_data = {
                    "reviewID":review.pk,
                    "reviewImages":each
                }
                imageserializer = CreateReviewImagesSerializer(data=reviewimages_data)
                if imageserializer.is_valid():
                    imageserializer.save()
            for each in request.data["dishID"]:                         # for each dish,create serializer and save
                dishreview_data = {
                    "reviewID":review.pk,
                    "dishID":each
                }
                serializer = DishReviewSerializer(data=dishreview_data)
                if serializer.is_valid():
                    serializer.save()
            data["code"] = 200
            data["messages"] = 'successful operation'
        else:
            data["code"] = 404
            data["messages"] = 'dish not exists'
    elif request.method=='GET':
        try:                                                # find stallID in url
            stallID = request.query_params["stallID"]
        except:
            data["code"] = 404
            data["messages"] = "stallID not found"
            return Response(data)

        review_list = Review.objects.filter(userID=user.pk, stallID=stallID)  # find reviews
        if review_list:
            data["code"] = 200
            data["messages"] = "successful operation"
            response_data = []
            for review in review_list:
                response_data.append(format_review(review))  # add review to response data
            data["data"] = response_data
        else:
            data["code"] = 404
            data["messages"] = "review not found"

    elif request.method=='DELETE':
        try:                                                # find reviewID in url
            reviewID = request.query_params["reviewID"]
        except:
            data["code"] = 404
            data["messages"] = "reviewID not found"
            return Response(data)
        try:
            Review.objects.get(reviewID=reviewID).delete()
            data["code"] = 200
            data["messages"] = "successful operation"
        except Review.DoesNotExist:
            data["code"] = 404
            data["messages"] = "review not exist"
        else:
            data["code"] = 400
            data["messages"] = "unsuccessful"
    return Response(data)

@api_view(["POST","DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def reviewslike(request,reviewID):
    data = {}
    user = get_user_by_request_token(request)  # get user by token
    request_data = {
        "userID":user.pk,
        "reviewID":int(reviewID)
    }
    if request.method=="POST":
        if LikeReview.objects.filter(userID=user.pk,reviewID=reviewID).exists():
            data["code"] = 400
            data["messages"] = "User already like this review"
        else:
            serializer = LikeReviewSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save()
                review = Review.objects.get(reviewID=reviewID)
                if review.reviewLikes:
                    review.reviewLikes += 1
                else:
                    review.reviewLikes = 1
                review.save()
                data["code"] = 200
                data["messages"] = "successful operation"
            else:
                data["code"] = 404
                data["messages"] = "review not found"
    elif request.method=="DELETE":
        likereview = LikeReview.objects.filter(userID=user.pk, reviewID=reviewID)
        if likereview:
            likereview.delete()
            review = Review.objects.get(reviewID=reviewID)
            review.reviewLikes -= 1
            review.save()
            data["code"] = 200
            data["messages"] = "successful operation"
        else:
            data["code"] = 404
            data["messages"] = "user hasn't like this review"
    return Response(data)

@api_view(["POST","DELETE","GET"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def dishes(request,dishID):
    data = {}
    if request.method=="POST":
        try:
            user = get_user_by_request_token(request)  # get user by token
        except:
            data["code"] = 400
            data["messages"] = "Token not provided"
            return Response(data)
        request_data = {
            "userID": user.pk,
            "dishID": int(dishID)
        }
        if LikeDish.objects.filter(userID=user.pk,dishID=dishID).exists():
            data["code"] = 400
            data["messages"] = "user already like this dish"
        else:
            serializer = LikeDishSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save()
                dish = Dish.objects.get(dishID=dishID)
                if dish.dishLikes:
                    dish.dishLikes += 1
                else:
                    dish.dishLikes = 1
                dish.save()
                data["code"] = 200
                data["messages"] = "successful operation"
            else:
                data = serializer.errors
    elif request.method=="DELETE":
        try:
            user = get_user_by_request_token(request)  # get user by token
        except:
            data["code"] = 400
            data["messages"] = "Token not provided"
            return Response(data)
        likedish = LikeDish.objects.filter(userID=user.pk,dishID=dishID)
        if likedish:
            likedish.delete()
            dish = Dish.objects.get(dishID=dishID)
            dish.dishLikes -= 1
            dish.save()
            data["code"] = 200
            data["messages"] = "successful operation"
        else:
            data["code"] = 404
            data["messages"] = "user hasn't like this dish"
    elif request.method=="GET":
        try:
            user = get_user_by_request_token(request)  # get user by token
            login = True
        except:
            user = 0
            login = False

        try:
            dish = Dish.objects.get(dishID=dishID)
            data["code"] = 200
            messages = format_dish(dish, user, login)
            data["messages"] = messages
        except:
            data["code"] = 404
            data["messages"] = "dish not found"
    return Response(data)