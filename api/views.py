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
from django.core.mail import send_mail
import threading
from THUeat.settings import BASE_URL
from apiprivate.permissions import *

# Create your views here.

def get_user_by_request_token(request):
    authorization = request.META.get('HTTP_AUTHORIZATION', '')  # get authorization from request header
    token = re.match('Token (.*)', authorization)  # find token in authorization
    if token:
        token = token.group(1)

    user = Token.objects.get(key=token).user  # get user by using token
    if user.is_superuser or user.is_admin or user.is_staff:
        return False
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

def data_is_incomplete(request,*args):
    for param in args:
        try:
            request.data[param]
        except:
            data = {
                "code":400,
                "message":"Incomplete data"
            }
            return Response(data)
    return False

incomplete_info = {
                "code":400,
                "message":"???????????????"
                }

@api_view(['POST'])
def user_register(request):
    if request.method=='POST':
        data = {}                                   # response data
        if data_is_incomplete(request,"userName","password","userEmail","userPhone"):
            return Response(incomplete_info)
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
                student = studentserializer.save()                                        # save studentserializer (save student to database)
                content = 'This is your verification number:'+student.verificationNumber    # create email content
                arg = (                                                                     # send_mail args
                    "THU-EAT Verification",
                    content,
                    settings.EMAIL_HOST_USER,
                    [student.userEmail],
                    True
                )
                t1 = threading.Thread(target=send_mail,args=arg)                            # multithreading send verification number to email
                t1.start()
                data['code'] = 200                                              # successful message
                data['message'] = 'successful operation'
            else:
                data['code'] = 400
                data['message'] = "?????????????????????"    # error userEmail exists
        else:
            data['code'] = 400
            messages = ""
            if User.objects.filter(userName=request.data["userName"]).exists(): # error userName exists
                messages += "??????????????????"
            if Student.objects.filter(userEmail=request.data["userEmail"]).exists():    # error userEmail exist
                messages += "?????????????????????"
            data['message'] = messages
        return Response(data)

@api_view(['POST'])
def user_verification(request):
    data = {}
    if request.method=='POST':
        if data_is_incomplete(request,"userName","verificationNumber"):
            return Response(incomplete_info)
        try:
            user = User.objects.get(userName=request.data["userName"])
            number = request.data["verificationNumber"]
            if number == '0':
                data["code"] = 400
                data["message"] = "???????????????"
                return Response(data)
            student = Student.objects.get(user=user.pk)
            verification = student.verificationNumber
            if number==verification:                        # check key in number with verification number
                user.is_active = True
                user.save()
                student.verificationNumber = 0
                student.save()
                data["code"] = 200
                data["message"] = "successful operation"
                token = Token.objects.get(user=user).key  # find user in Token model and get its token
                data['data'] = {
                    "token": token,
                }
            else:
                data["code"] = 400
                data["message"] = "???????????????"
                return Response(data)
        except:
            data["code"] = 404
            data["message"] = '???????????????'
    return Response(data)

@api_view(['POST'])
def user_login(request):
    data = {}
    if request.method=='POST':
        if data_is_incomplete(request,"userName","password"):
            return Response(incomplete_info)
        userName = request.data['userName']                     # get userName
        password = request.data['password']                     # get password
        try:
            user = User.objects.get_by_natural_key(userName)    # get user by using userName
            if user.is_admin or user.is_superuser or user.is_staff:
                data['code'] = 400
                data['message'] = '??????????????????'
                return Response(data)
            if not user.is_active:
                data['code'] = 400
                data['message'] = '???????????????'
                return Response(data)
            if user.check_password(password):                   # check password
                user.save()
                data['code'] = 200
                data['message'] = 'successful operation'
                data['data'] = {
                    "token": Token.objects.get(user_id=user.id).key  # get token by using user_id
                }
            else:
                data['code'] = 404
                data['message'] = '????????????'
        except:
            data['code'] = 404
            data['message'] = '???????????????'
        return Response(data)

@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsNormalUser])
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
            "userImage": BASE_URL + student.userImage.url,
            "userPhone": user.userPhone
        }
        review_list = Review.objects.filter(userID=user.pk)         # find user review
        myReviews = []
        for review in review_list:
            myReviews.append(format_myreview(review))               # add review to myReviews
        data["data"]["myReviews"] = myReviews

        return Response(data)
    elif request.method=='POST':                                    # update user details
        if data_is_incomplete(request,"userName","userPhone"):
            return Response(incomplete_info)
        user = get_user_by_request_token(request)                   # get user by token
        student = get_student_by_user(user)                         # get student
        user_data = {
            "userName": request.data["userName"],
            "userPhone": request.data["userPhone"]
        }
        userserializer = UpdateUserSerializer(user, data=user_data)  # create serializer
        if request.data["userImage"]:
            student_data = {
                "user": user.pk,
                "userEmail": request.data["userEmail"],
                "userImage": request.data["userImage"]
            }
            studentserializer = UpdateStudentSerializer(student, data=student_data)
        else:
            student_data = {
                "user": user.pk,
                "userEmail": request.data["userEmail"]
            }
            studentserializer = UpdateStudentEmailSerializer(student, data=student_data)
        if (userserializer.is_valid())&(studentserializer.is_valid()):  # check serializer (check data)
            userserializer.save()                    # save serializer (update data)
            studentserializer.save()
            data['code'] = 200
            data['message'] = 'successful operation'
        else:
            data['code'] = 400
            messages = ""
            if User.objects.filter(userName=request.data["userName"]).exclude(userName=user.userName).exists():  # error userName exists
                messages += "??????????????????"
            if Student.objects.filter(userEmail=request.data["userEmail"]).exclude(userEmail=student.userEmail).exists():  # error userEmail exist
                messages += "?????????????????????"
            data['message'] = messages
        return Response(data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsNormalUser])
def user_password(request):
    data = {}
    user = get_user_by_request_token(request)               # get user by token
    if data_is_incomplete(request, "password"):
        return Response(incomplete_info)
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
            data['message'] = '???????????????'
        return Response(data)

@api_view(["GET"])
def navigations(request):
    data = {}
    if request.method=='GET':
        canteen_list = Canteen.objects.all()
        data["code"] = 200
        data["message"] = "successful operation"
        data["data"] = format_navigations_canteen_list(canteen_list)
    return Response(data)


@api_view(["GET"])
def navigations_stall(request,stallID):
    data = {}
    if request.method=='GET':
        dish_list = Dish.objects.filter(stallID=stallID, is_active=True)  # find dishes
        data["code"] = 200
        data["message"] = "successful operation"
        data["data"] = format_navigations_dish_list(dish_list)
    return Response(data)

@api_view(["GET"])
def canteens(request,canteenID):
    data = {}
    if request.method=='GET':
        canteen = Canteen.objects.get(canteenID=canteenID)
        data["code"] = 200
        data["message"] = "successful operation"
        data["data"] = format_canteen(canteen)
        try:
            canteen = Canteen.objects.get(canteenID=canteenID)
            data["code"] = 200
            data["message"] = "successful operation"
            data["data"] = format_canteen(canteen)
        except:
            data["code"] = 404
            data["message"] = "???????????????"
    return Response(data)

@api_view(["GET"])
def recommendstall(request):
    data = {}
    if request.method=='GET':
        stall_list = Stall.objects.all().exclude(is_active=False).exclude(stallRate=0)     # get all stall
        try:
            ratings = request.query_params["ratings"]                                      # try get ratings in url
            if ratings=="True":
                stall_list = Stall.objects.order_by("-stallRate")\
                    .exclude(is_active=False).exclude(stallRate=0)                         # sort stall list by ratings
        except:
            pass
        try:
            numbers = int(request.query_params["numbers"])                                 # try get numbers in url
            stall_list = stall_list[:numbers]                                    # filter stall list to specific number
        except:
            pass
        data["code"] = 200
        data["message"] = "successful operation"
        data["data"] = format_recommend_stall_list(stall_list)              # format stall list to some specific format
    return Response(data)

@api_view(["GET"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def stalls(request, stallID):
    data = {}
    if request.method=='GET':    
        try:
            user = get_user_by_request_token(request)     # get user by token
            if not user:
                data["code"] = 400
                data["message"] = "???????????????"
                return Response(data)
            login = True
        except:
            user = 0
            login = False
        try:
            stall = Stall.objects.get(stallID=stallID)
            if stall.is_active:
                data["code"] = 200
                data["message"] = "successful operation"
                data["data"] = format_stall(stall, user, login)
            else:
                data["code"] = 400
                data["message"] = "???????????????"
        except:
            data["code"] = 404
            data["message"] = "???????????????"
    return Response(data)

def review_tags_encode(tags_list):
    tags = "/".join(tags_list)
    return tags

@api_view(["POST","GET","DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsNormalUser])
def reviews(request):
    data = {}
    user = get_user_by_request_token(request)               # get user by token
    if request.method=='POST':
        if data_is_incomplete(request,"reviewComment","reviewTags","rate"):
            return Response(incomplete_info)
        try:                                                # find stallID in url
            stallID = request.query_params["stallID"]
        except:
            data["code"] = 404
            data["message"] = "???????????????"
            return Response(data)
        # review_tags = dict((request.data).lists())["reviewTags"]
        if request.data["reviewComment"]=="undefined" or request.data["reviewComment"]=="":
            comment = "?????????????????????????????????"
        else:
            comment = request.data["reviewComment"]
        review_data = {
            "reviewComment":comment,
            "reviewTags":request.data["reviewTags"],
            "rate":request.data["rate"],
            "userID":user.pk,
            "stallID":stallID
        }
        reviewserializer = CreateReviewSerializer(data=review_data)     # create reviewserializer
        if (reviewserializer.is_valid())&(check_dish_is_valid(request.data["dishID"])):
            review = reviewserializer.save()                            # save serializer to create primary key
            stall = Stall.objects.get(stallID=stallID)
            if stall.stallRate:
                stall.stallRate = Review.objects.filter(stallID=stallID).aggregate(models.Avg('rate'))["rate__avg"]
                stall.stallRate = round(stall.stallRate,1)
            else:
                stall.stallRate = request.data["rate"]
            stall.stallRateNum = Review.objects.filter(stallID=stallID).count()
            stall.save()
            image_list = dict((request.data).lists())['reviewImages']
            if request.data["reviewImages"]:
                for image in image_list:
                    reviewimages_data = {
                        "reviewID": review.pk,
                        "reviewImages": image
                    }
                    imageserializer = CreateReviewImagesSerializer(data=reviewimages_data)
                    if imageserializer.is_valid():
                        imageserializer.save()
            dish_list = dict((request.data).lists())['dishID']
            if request.data["dishID"]:
                for each in dish_list:                         # for each dish,create serializer and save
                    dishreview_data = {
                        "reviewID":review.pk,
                        "dishID":each
                    }
                    serializer = DishReviewSerializer(data=dishreview_data)
                    if serializer.is_valid():
                        serializer.save()
            data["code"] = 200
            data["message"] = 'successful operation'
        else:
            data["code"] = 404
            data["message"] = '???????????????'
    elif request.method=='GET':
        try:                                                # find stallID in url
            stallID = request.query_params["stallID"]
        except:
            data["code"] = 404
            data["message"] = "???????????????"
            return Response(data)

        review_list = Review.objects.filter(userID=user.pk, stallID=stallID)  # find reviews
        if review_list:
            data["code"] = 200
            data["message"] = "successful operation"
            response_data = []
            for review in review_list:
                response_data.append(format_review(review))  # add review to response data
            data["data"] = response_data
        else:
            data["code"] = 404
            data["message"] = "???????????????"

    return Response(data)

@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsNormalUser])
def deletereviews(request,reviewID):
    data = {}
    user = get_user_by_request_token(request)  # get user by token
    if request.method=='DELETE':
        try:
            review = Review.objects.get(reviewID=reviewID)
            if review.userID.pk == user.pk:
                review.delete()
                data["code"] = 200
                data["message"] = "successful operation"
            else:
                data["code"] = 400
                data["message"] = "????????????"
        except Review.DoesNotExist:
            data["code"] = 404
            data["message"] = "???????????????"
    return Response(data)

@api_view(["POST","DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsNormalUser])
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
            data["message"] = "????????????????????????"
        else:
            serializer = LikeReviewSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save()
                review = Review.objects.get(reviewID=reviewID)
                if review.reviewLikes:
                    review.reviewLikes = LikeReview.objects.filter(reviewID=reviewID).count()
                else:
                    review.reviewLikes = 1
                review.save()
                data["code"] = 200
                data["message"] = "successful operation"
            else:
                data["code"] = 404
                data["message"] = "???????????????"
    elif request.method=="DELETE":
        likereview = LikeReview.objects.filter(userID=user.pk, reviewID=reviewID)
        if likereview:
            likereview.delete()
            review = Review.objects.get(reviewID=reviewID)
            review.reviewLikes = LikeReview.objects.filter(reviewID=reviewID).count()
            review.save()
            data["code"] = 200
            data["message"] = "successful operation"
        else:
            data["code"] = 404
            data["message"] = "???????????????????????????"
    return Response(data)

@api_view(["POST","DELETE","GET"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def dishes(request,dishID):
    data = {}
    if request.method=="POST":
        try:
            user = get_user_by_request_token(request)  # get user by token
            if not user:
                data["code"] = 400
                data["message"] = "???????????????"
                return Response(data)
        except:
            data["code"] = 400
            data["message"] = "????????????"
            return Response(data)
        if not user.is_active:
            data["code"] = 400
            data["message"] = "???????????????"
            return Response(data)
        request_data = {
            "userID": user.pk,
            "dishID": int(dishID)
        }
        if LikeDish.objects.filter(userID=user.pk,dishID=dishID).exists():
            data["code"] = 400
            data["message"] = "????????????????????????"
        else:
            serializer = LikeDishSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save()
                dish = Dish.objects.get(dishID=dishID)
                if dish.dishLikes:
                    dish.dishLikes = LikeDish.objects.filter(dishID=dishID).count()
                else:
                    dish.dishLikes = 1
                dish.save()
                data["code"] = 200
                data["message"] = "successful operation"
            else:
                data = serializer.errors
    elif request.method=="DELETE":
        try:
            user = get_user_by_request_token(request)  # get user by token
        except:
            data["code"] = 400
            data["message"] = "????????????"
            return Response(data)
        likedish = LikeDish.objects.filter(userID=user.pk,dishID=dishID)
        if likedish:
            likedish.delete()
            dish = Dish.objects.get(dishID=dishID)
            dish.dishLikes = LikeDish.objects.filter(dishID=dishID).count()
            dish.save()
            data["code"] = 200
            data["message"] = "successful operation"
        else:
            data["code"] = 404
            data["message"] = "???????????????????????????"
    elif request.method=="GET":
        try:
            user = get_user_by_request_token(request)  # get user by token
            login = True
        except:
            user = 0
            login = False

        try:
            dish = Dish.objects.get(dishID=dishID)
            if dish.is_active:
                data["code"] = 200
                data["message"] = "successful operation"
                data["data"] = format_dish(dish, user, login)
            else:
                data["code"] = 400
                data["message"] = "???????????????"
        except:
            data["code"] = 404
            data["message"] = "???????????????"
    return Response(data)

@api_view(["GET"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def recommenddish(request):
    data = {}

    if request.method=="GET":
        try:
            user = get_user_by_request_token(request)  # get user by token
            login = True
        except:
            user = 0
            login = False
        try:
            likes = request.query_params["likes"]
            if likes=="True":
                likes = True
            else:
                likes = False
        except:
            likes = False
        try:
            numbers = int(request.query_params["numbers"])
            if likes:
                dish_list = Dish.objects.order_by("-dishLikes").exclude(is_active=False).exclude(dishLikes=0)[:numbers]
            else:
                dish_list = Dish.objects.all().exclude(is_active=False).exclude(dishLikes=0)[:numbers]
        except:
            if likes:
                dish_list = Dish.objects.order_by("-dishLikes").exclude(is_active=False).exclude(dishLikes=0)
            else:
                dish_list = Dish.objects.all().exclude(is_active=False).exclude(dishLikes=0)
        messages = []
        for dish in dish_list:
            messages.append(format_recommend_dish(dish,user,login))
        data["code"] = 200
        data["message"] = "successful operation"
        data["data"] = messages

    return Response(data)

@api_view(["GET"])
def getnotice(request):
    data = {}
    if request.method=="GET":
        notice_list = Notice.objects.all()
        data["code"] = 200
        data["message"] = "successful operation"
        data["data"] = format_notice_list(notice_list)
    return Response(data)