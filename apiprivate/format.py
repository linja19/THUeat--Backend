from api.models import *

def format_stafflist(stafflist):
    data_list = []
    for staff in stafflist:
        data = {}
        data["staffID"] = staff.staffID
        data["staffValidName"] = staff.staffName
        data["staffName"] = staff.user.userName
        data["staffPhone"] = staff.user.userPhone
        data["staffStatus"] = staff.user.is_active
        staffstall = {}
        staffstall["stallID"] = staff.stallID.pk
        staffstall["stallName"] = staff.stallID.stallName
        staffstall["stallFloor"] = staff.stallID.stallFloor
        staffstall["canteenName"] = staff.stallID.canteenID.canteenName
        data["staffStall"] = staffstall
        data_list.append(data)
    return data_list

def format_adminlist(adminlist):
    data_list = []
    for admin in adminlist:
        data = {}
        data["adminID"] = admin.adminID
        data["adminValidName"] = admin.adminName
        data["adminName"] = admin.user.userName
        data["adminPhone"] = admin.user.userPhone
        data["adminStatus"] = admin.user.is_active
        data_list.append(data)
    return data_list

def format_student_list(student_list):
    data_list = []
    for student in student_list:
        data = {}
        user = student.user
        data["userID"] = user.pk
        data["userName"] = user.userName
        data["userImage"] = student.userImage.url
        data["userEmail"] = student.userEmail
        data["userStatus"] = user.is_active
        data_list.append(data)
    return data_list

def format_student(student):
    data = {}
    user = student.user
    data["userName"] = user.userName
    data["userImage"] = student.userImage.url
    data["userEmail"] = student.userEmail
    data["userStatus"] = user.is_active
    return data

import datetime
def format_admin_statistic():
    data = {}
    all_user_number = User.objects.all().count()
    today_user_number = User.objects.filter(last_login__gte=datetime.date.today()).count()
    login_rate = round(today_user_number/all_user_number*100,2)
    all_admin_number = Admin.objects.all().count()
    all_stall_number = Stall.objects.all().count()
    data["userNumber"] = all_user_number
    data["userLoginRate"] = login_rate
    data["adminNumber"] = all_admin_number
    data["stallNumber"] = all_stall_number
    return data

def format_notice_list(notice_list):
    datalist = []
    for notice in notice_list:
        data = {}
        data["noticeTitle"] = notice.noticeTitle
        data["noticeWords"] = notice.noticeWords
        data["noticeImage"] = notice.noticeImage.url
        datalist.append(data)
    return datalist

def format_canteen():
    datalist = []
    canteen_list = Canteen.objects.all()
    for canteen in canteen_list:
        data = {}
        data["canteenID"] = canteen.canteenID
        data["canteenName"] = canteen.canteenName
        data["canteenPhone"] = canteen.canteenPhone
        data["canteenAddress"] = canteen.canteenAddress
        data["canteenIntro"] = canteen.canteenIntro
        data["canteenImage"] = canteen.canteenImage.url
        data["canteenType"] = canteen.canteenType
        data["canteenOperationtime"] = canteen.canteenOperationTime
        datalist.append(data)
    return datalist

def format_canteen_name():
    datalist = []
    canteen_list = Canteen.objects.all()
    for canteen in canteen_list:
        data = {}
        data["canteenID"] = canteen.canteenID
        data["canteenName"] = canteen.canteenName
        data["canteenType"] = canteen.canteenType
        datalist.append(data)
    return datalist

def format_stall_list(stall_list):
    datalist = []
    for stall in stall_list:
        data = {}
        data["stallID"] = stall.stallID
        data["stallName"] = stall.stallName
        data["stallFloor"] = stall.stallFloor
        data["canteenName"] = stall.canteenID.canteenName
        data["stallStatus"] = stall.is_active
        datalist.append(data)
    return datalist

def format_review_list(review_list):
    data_list = []
    for review in review_list:
        data = {}
        data["userName"] = review.userID.userName
        data["userImage"] = Student.objects.get(user=review.userID).userImage.url
        data["reviewID"] = review.reviewID
        data["reviewDateTime"] = review.reviewDateTime
        data["rate"] = review.rate
        data["reviewComment"] = review.reviewComment
        data["reviewImages"] = [image.url for image in ReviewImage.objects.filter(reviewID=review.reviewID)]
        data["reviewTags"] = review.reviewTags
        data["reviewLikes"] = review.reviewLikes
        data["replyDateTime"] = ""
        data["replyComment"] = ""
        if review.reply:
                data["replyDateTime"] = ReplyByStaff.objects.get(parent_reviewID=review.reviewID).replyDateTime
                data["replyComment"] = ReplyByStaff.objects.get(parent_reviewID=review.reviewID).replyContent
        dishes = []
        for dishreview in DishReview.objects.filter(reviewID=review.reviewID):
            dish_data = {}
            dish_data["dishID"] = dishreview.dishID.pk
            dish_data["dishName"] = dishreview.dishID.dishName
            dishes.append(dish_data)
        data["dishes"] = dishes
        data_list.append(data)
    return data_list