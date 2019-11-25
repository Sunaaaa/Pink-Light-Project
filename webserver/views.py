from django.shortcuts import render, redirect, get_object_or_404
from .models import Train, Notification
from django import forms
from .forms import TrainForm
from django.http import JsonResponse
from django.db.models import Count
import requests
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from decouple import config
import json


# Create your views here.
# @csrf_exempt
def pink_light(request, seat_info):
    if request.method == "POST":
        print('POST')

        train_no = seat_info[:6]
        slot_no = seat_info[6:9]
        seat_no = seat_info[9:]

        # 임산부석 상태 변경
        train = Train.objects.get(train_no=train_no, slot_no=slot_no, seat_no=seat_no)
        if train.empty :
            train.empty = False
        else :
            train.empty = True
        train.save()

        # 열차 정보 & 알림 가져오기
        status = ""
        if train.empty:
            status = "이용 완료"
        else : 
            status = "이용 중"
        content = f'{ train.train_no } 번 열차 {train.slot_no} 번째 칸 {train.seat_no} 번 임산부석 {status}'
        print(content)

        notify = Notification.objects.create(content=content)

    return redirect('webserver:index')

# @csrf_exempt 
def station_status(request, station):
    print('뿜뿜뿜')

    api_url = 'http://swopenapi.seoul.go.kr/api/subway'
    key = config('SUBWAY_REAL_TIME')
    station_status = requests.get(f'{api_url}/{key}/json/realtimeStationArrival/0/5/{station}').json()
    data = station_status['realtimeArrivalList']
    print(len(data))

    trainLineNm = []

    for i in range(0,4,2):
        trainLineNm.append(data[i].get('trainLineNm'))

    empty_dict = []
    t_up = Train.objects.filter(train_no="001001")
    t_down = Train.objects.filter(train_no="001002")

    for t in t_up:
        empty_dict.append(t.empty)

    empty_seat_status_up = sum(empty_dict)

    empty_dict = []
    for t in t_down:
        empty_dict.append(t.empty)

    empty_seat_status_down = sum(empty_dict)

    empty_seat_status = {
        'up' : empty_seat_status_up,
        'down' : empty_seat_status_down
    }

    context = {
        'empty_seat_status' : empty_seat_status,
        'trainLineNm' : trainLineNm,

    }
    return JsonResponse(context)

# @csrf_exempt 
def station_status_detail(request, station):
    print('뿜뿜뿜')
    up_train1_no = "001001"
    up_train2_no = "001003"
    down_train1_no = "001002"
    down_train2_no = "001004"
    t_up_1 = Train.objects.filter(train_no=up_train1_no)
    t_up_2 = Train.objects.filter(train_no=up_train2_no)
    t_down_1 = Train.objects.filter(train_no=down_train1_no)
    t_down_2 = Train.objects.filter(train_no=down_train2_no)

    empty_up_1 = []
    for t in t_up_1:
        empty_up_1.append(t.empty)
    
    print('=====')

    empty_up_2 = []
    for t in t_up_2:
        empty_up_2.append(t.empty)
    
    print('=====')

    empty_down_1 = []
    for t in t_down_1:
        empty_down_1.append(t.empty)
    
    print('=====')

    empty_down_2 = []
    for t in t_down_2:
        empty_down_2.append(t.empty)

    print('=====')

    empty_seat_status = {
        'up' : {
            # 'trains' : [up_train1_no, up_train2_no]
            'total' : [len(t_up_1), len(t_up_2)],
            'empty' : [sum(empty_up_1), sum(empty_up_2)],
        },
        'down' : {
            # 'trains' : [down_train1_no, down_train2_no]
            'total' : [len(t_down_1), len(t_down_2)],
            'empty' : [sum(empty_down_1), sum(empty_down_2)]
        },
    }

    api_url = 'http://swopenapi.seoul.go.kr/api/subway'
    key = config('SUBWAY_REAL_TIME')
    station_status = requests.get(f'{api_url}/{key}/json/realtimeStationArrival/0/5/{station}').json()
    data = station_status['realtimeArrivalList']
    print(len(data))

    btrainNo = []
    trainLineNm = []
    arvlMsg2 = []
    
    mmy_trains = []
    for i in range(len(data)):
        btrainNo.append(data[i].get('btrainNo'))
        trainLineNm.append(data[i].get('trainLineNm'))
        arvlMsg2.append(data[i].get('arvlMsg2'))
        mmy_trains.append([data[i].get('btrainNo'), data[i].get('trainLineNm'), data[i].get('arvlMsg2')])



    context = {
        'trains' : mmy_trains,
        # 'btrainNo' : btrainNo,
        # 'trainLineNm' : trainLineNm,
        # 'arvlMsg2' : arvlMsg2,
        'empty_seat_status' : empty_seat_status,        
    }
    return JsonResponse(context)


def index(request):
    trains = Train.objects.all()
    # tt = Train.objects.values('train_no').annotate(total=Count('train_no'))
    train_list = list(Train.objects.filter().values('train_no').order_by('train_no').distinct())
    print(type(train_list))
    print(train_list)


    train_no_list = []
    t_list = []
    for train in train_list:
        print(train.get('train_no'))
        train_no = train.get('train_no')
        train_no_list.append(train_no)

        my_train = Train.objects.filter(train_no=train_no)
        t_list.append(list(my_train))


    notifications = Notification.objects.all()

    context = {
        'train_no_list' : train_no_list,
        'tt' : t_list,
        'trains' : trains,
        'notifications': notifications,
    }
    return render(request, 'webserver/index.html', context)


def new(request):

    if request.method == "POST":
        form = TrainForm(request.POST)
        print("뿜뿜")
        if form.is_valid():

            train_no = form.cleaned_data.get('train_no')
            print(train_no)
            slot_no = form.cleaned_data.get('slot_no')
            seat_no = form.cleaned_data.get('seat_no')
            train = Train.objects.create(train_no=train_no, slot_no=slot_no, seat_no=seat_no, empty="False")
        
        return redirect('webserver:index')
    else:
        form = TrainForm()

    context = {
        'form' : form ,
    }

    return render(request, 'webserver/form.html', context)

def train_detail(request, train_no):
    print(train_no)
    trains = Train.objects.filter(train_no=train_no)
    print(trains[0])

    context = {
        'trains' : trains,
    }
    return render(request, 'webserver/train_detail.html', context)

def detail(request, train_pk):
    train = get_object_or_404(Train, pk=train_pk)
    context = {
        'train' : train,
    }
    return render(request, 'webserver/detail.html', context)


def edit(request, train_pk):
    train = get_object_or_404(Train, pk=train_pk)
    if request.method == "POST":
        form = TrainForm(request.POST, instance=train)
        print("뿜뿜")
        if form.is_valid():
            train = form.save()
            return redirect('webserver:detail', train_pk)
        
    else:
        form = TrainForm(instance=train)

    context = {
        'form' : form ,
    }

    return render(request, 'webserver/form.html', context)

def delete(request):
    pass

def delete_notification(request, notification_pk):
    if request.method == "POST":
        noti = Notification.objects.get(pk=notification_pk)
        noti.delete()

    return redirect('webserver:index')
