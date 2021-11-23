from api.models import *

def format_stafflist(stafflist):
    data_list = []
    for staff in stafflist:
        data = {}
        data["staffID"] = staff.user.pk
        data["staffName"] = staff.user.userName
        data["staffPhone"] = staff.user.userPhone
        data["staffStatus"] = staff.user.is_active
        staffstall = {}
        staffstall["stallID"] = staff.stallID.pk
        staffstall["stallName"] = staff.stallID.stallName
        staffstall["canteenName"] = staff.stallID.canteenID.canteenName
        data["staffStall"] = staffstall
        data_list.append(data)
    return data_list

def format_adminlist(adminlist):
    data_list = []
    for user in adminlist:
        data = {}
        data["adminID"] = user.pk
        data["adminName"] = user.userName
        data["adminPhone"] = user.userPhone
        data["adminStatus"] = user.is_active
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