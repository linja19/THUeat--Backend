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
    data["userNumber"] = all_user_number
    data["userLoginRate"] = login_rate
    return data