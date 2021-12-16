from api.models import *
from THUeat.settings import BASE_URL

def format_stafflist(stafflist):
    data_list = []
    for staff in stafflist:
        data = {}
        data["staffID"] = staff.staffID
        data["staffValidName"] = staff.staffName
        data["staffName"] = staff.user.userName
        data["staffPhone"] = staff.user.userPhone
        data["staffStatus"] = staff.user.is_active
        data["stallID"] = staff.stallID.pk
        data["stallName"] = staff.stallID.stallName
        data["stallFloor"] = staff.stallID.stallFloor
        data["canteenName"] = staff.stallID.canteenID.canteenName
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
        data["userImage"] = BASE_URL + student.userImage.url
        data["userEmail"] = student.userEmail
        data["userStatus"] = user.is_active
        data_list.append(data)
    return data_list

def format_student(student):
    data = {}
    user = student.user
    data["userName"] = user.userName
    data["userImage"] = BASE_URL + student.userImage.url
    data["userEmail"] = student.userEmail
    data["userStatus"] = user.is_active
    return data

import datetime
def format_admin_statistic():
    data = {}
    student_list = User.objects.exclude(is_staff=True).exclude(is_active=False)
    all_user_number = student_list.count()
    today_user_number = student_list.filter(last_login__gte=datetime.date.today()).count()
    login_rate = round(today_user_number/all_user_number*100,2)
    all_staff_number = Staff.objects.all().count()
    all_stall_number = Stall.objects.all().count()
    data["userNumber"] = all_user_number
    data["userLoginRate"] = login_rate
    data["staffNumber"] = all_staff_number
    data["stallNumber"] = all_stall_number
    return data

def format_notice_list(notice_list):
    datalist = []
    for notice in notice_list:
        data = {}
        data["noticeID"] = notice.pk
        data["noticeTitle"] = notice.noticeTitle
        data["noticeWords"] = notice.noticeWords
        data["noticeImage"] = BASE_URL + notice.noticeImage.url
        datalist.append(data)
    return datalist

def format_canteen():
    datalist = []
    canteen_list = Canteen.objects.all()
    for canteen in canteen_list:
        data = {}
        data["canteenID"] = canteen.canteenID
        data["canteenName"] = canteen.canteenName
        floor_list = []
        canteen_floors  = []
        for floor in canteen.canteenFloor:
            if floor == "0":
                floor_list.append(-1)
            else:
                floor_list.append(int(floor))
        stall_list = Stall.objects.filter(canteenID=canteen.canteenID)
        for floor in floor_list:
            stall_floor_data = {}
            stall_floor_data["stallFloor"] = floor
            stall_floor_data["stalls"] = format_stall_by_floor(stall_list,floor)
            canteen_floors.append((stall_floor_data))
        data["canteenFloors"] = canteen_floors
        datalist.append(data)

    return datalist

def format_stall_by_floor(stall_list,floor):
    data_list = []
    for stall in stall_list.filter(stallFloor=floor):
        data = {}
        data["stallName"] = stall.stallName
        data["stallID"] = stall.stallID
        data_list.append(data)
    return data_list

def format_canteen_name():
    datalist = []
    canteen_list = Canteen.objects.all()
    for canteen in canteen_list:
        data = {}
        data["canteenID"] = canteen.canteenID
        data["canteenName"] = canteen.canteenName
        floor_list = []
        for floor in canteen.canteenFloor:
            if floor=="0":
                floor_list.append(-1)
            else:
                floor_list.append(int(floor))
        data["canteenFloor"] = floor_list
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

def review_tags_decode(tags):
    if tags:
        return tags.split("/")
    else:
        return []

def format_review_list(review_list):
    data_list = []
    for review in review_list:
        data = {}
        data["userName"] = review.userID.userName
        data["userImage"] = BASE_URL + Student.objects.get(user=review.userID).userImage.url
        data["reviewID"] = review.reviewID
        data["reviewDateTime"] = review.reviewDateTime
        data["rate"] = review.rate
        data["reviewComment"] = review.reviewComment
        data["reviewImages"] = [BASE_URL + image.reviewImages.url for image in ReviewImage.objects.filter(reviewID=review.reviewID)]
        data["reviewTags"] = review_tags_decode(review.reviewTags)
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

def operation_time_encode(time):
    session = time.split('/')
    session_data_list = []
    start = []
    end = []
    for each in session:
        if "早餐" in each:
            start_time = each.split('-')[1]
            end_time = each.split('-')[2]
            session_data = 'B'+'-'+start_time+'-'+end_time
            session_data_list.append(session_data)
            start.append(int(start_time.replace(':','')))
            end.append(int(end_time.replace(':','')))
        elif "午餐" in each:
            start_time = each.split('-')[1]
            end_time = each.split('-')[2]
            session_data = 'L' + '-' + start_time + '-' + end_time
            session_data_list.append(session_data)
            start.append(int(start_time.replace(':', '')))
            end.append(int(end_time.replace(':', '')))
        elif "晚餐" in each:
            start_time = each.split('-')[1]
            end_time = each.split('-')[2]
            session_data = 'D' + '-' + start_time + '-' + end_time
            session_data_list.append(session_data)
            start.append(int(start_time.replace(':', '')))
            end.append(int(end_time.replace(':', '')))
        elif "宵夜" in each:
            start_time = each.split('-')[1]
            end_time = each.split('-')[2]
            session_data = 'S' + '-' + start_time + '-' + end_time
            session_data_list.append(session_data)
            start.append(int(start_time.replace(':', '')))
            end.append(int(end_time.replace(':', '')))
        elif "自定义" in each:
            start_time = each.split('-')[1]
            end_time = each.split('-')[2]
            start.append(int(start_time.replace(':', '')))
            end.append(int(end_time.replace(':', '')))
            session_data = 'C' + '-' + start_time + '-' + end_time
            session_data_list = [session_data]
            break
    session_data = '/'.join(session_data_list)
    earliest_start_time = min(start)
    latest_end_time = max(end)
    return session_data,earliest_start_time,latest_end_time

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

def format_mystall(stall):
    data = {}
    canteen = Canteen.objects.get(canteenID=stall.canteenID.pk)
    data["stallName"] = stall.stallName
    data["stallFloor"] = stall.stallFloor
    data["stallDescribe"] = stall.stallDescribe
    data["canteenName"] = canteen.canteenName
    data["stallStatus"] = stall.is_active
    data["stallImages"] = [BASE_URL + stallimage.stallImage.url for stallimage in StallImage.objects.filter(stallID=stall.stallID)]
    data["stallRate"] = stall.stallRate
    data["stallRateNumber"] = stall.stallRateNum
    data["canteenRate"] = calculate_canteen_rate(canteen)
    data["bestDishName"] = get_best_dish_name(stall)
    data["stallOperationtime"] = operation_time_decode(stall.stallOperationtime)
    return data

def calculate_canteen_rate(canteen):
    stall_list = Stall.objects.filter(canteenID=canteen.canteenID)
    rate = round(stall_list.exclude(stallRate=0).aggregate(models.Avg('stallRate'))["stallRate__avg"],1)
    return rate

def get_best_dish_name(stall):
    dish_list = Dish.objects.filter(stallID=stall.stallID)
    if dish_list:
        best_dish = dish_list.order_by("-dishLikes")[0]
        return best_dish.dishName
    else:
        return ""

def dish_available_time_encode(time_list):
    session_list = []
    for session in time_list:
        if "早餐" in session:
            session_list.append("早餐")
        if "午餐" in session:
            session_list.append("午餐")
        if "晚餐" in session:
            session_list.append("晚餐")
        if "宵夜" in session:
            session_list.append("宵夜")
        if "自定义" in session:
            session_list = ["自定义"]
    session_data = ",".join(session_list)
    return session_data

def compare_dish_time_stall_time(dish,stall):
    dish_time = dish_available_time_decode(dish.dishAvailableTime)
    stall_time = stall_operation_time_session_decode(stall.stallOperationtime)
    if "自定义" in stall_time:
        dish.dishAvailableTime = "自定义"
        dish.save()
        return
    new_dish_time = []
    for each in dish_time:
        if each in stall_time:
            new_dish_time.append(each)
    dish.dishAvailableTime = dish_available_time_encode(new_dish_time)
    dish.save()

def dish_available_time_decode(time):
    if time:
        time_list = time.split(',')
        return time_list
    else:
        return []

def stall_operation_time_session_decode(time):
    session = time.split('/')
    operation_time_list = []
    for each in session:
        if "B" in each:
            operation_time_list.append("早餐")
        elif "L" in each:
            operation_time_list.append("午餐")
        elif "D" in each:
            operation_time_list.append("晚餐")
        elif "S" in each:
            operation_time_list.append("宵夜")
        elif "C" in each:
            operation_time_list = ["自定义"]
            break
    return operation_time_list

def format_dish_list(dish_list):
    data_list = []
    for dish in dish_list:
        data = {}
        data["dishID"] = dish.dishID
        data["dishName"] = dish.dishName
        data["dishIntro"] = dish.dishDescribe
        data["dishPrice"] = '{0:.2f}'.format(dish.dishPrice)
        image_list = DishImage.objects.filter(dishID=dish.pk)
        data["dishImages"] = [BASE_URL + image.dishImage.url for image in image_list]
        data["dishLikes"] = dish.dishLikes
        data["dishAvailableTime"] = dish_available_time_decode(dish.dishAvailableTime)
        data["dishStatus"] = dish.is_active
        data["stallOperationtime"] = stall_operation_time_session_decode(dish.stallID.stallOperationtime)
        data_list.append(data)
    return data_list

def format_dish(dish):
    data = {}
    data["dishName"] = dish.dishName
    data["dishIntro"] = dish.dishDescribe
    data["dishPrice"] = '{0:.2f}'.format(dish.dishPrice)
    image_list = DishImage.objects.filter(dishID=dish.pk)
    data["dishImages"] = [BASE_URL + image.dishImage.url for image in image_list]
    data["dishLikes"] = dish.dishLikes
    data["dishAvailableTime"] = dish_available_time_decode(dish.dishAvailableTime)
    data["dishStatus"] = dish.is_active
    data["stallOperationtime"] = stall_operation_time_session_decode(dish.stallID.stallOperationtime)
    dishreview_list = DishReview.objects.filter(dishID=dish.dishID)
    data["reviews"] = format_dishreview_list(dishreview_list)
    return data

def format_dishreview_list(dishreview_list):
    data_list = []
    for dishreview in dishreview_list:
        review = dishreview.reviewID
        data = {}
        data["userName"] = review.userID.userName
        data["userImage"] = BASE_URL + Student.objects.get(user=review.userID).userImage.url
        data["reviewID"] = review.reviewID
        data["reviewDateTime"] = review.reviewDateTime
        data["rate"] = review.rate
        data["reviewComment"] = review.reviewComment
        data["reviewImages"] = [BASE_URL + image.reviewImages.url for image in ReviewImage.objects.filter(reviewID=review.reviewID)]
        data["reviewTags"] = review_tags_decode(review.reviewTags)
        data["reviewLikes"] = review.reviewLikes
        data["replyDateTime"] = ""
        data["replyComment"] = ""
        if review.reply:
                data["replyDateTime"] = ReplyByStaff.objects.get(parent_reviewID=review.reviewID).replyDateTime
                data["replyComment"] = ReplyByStaff.objects.get(parent_reviewID=review.reviewID).replyContent
        data_list.append(data)
    return data_list