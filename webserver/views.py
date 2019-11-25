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

# Create your views here.
# @csrf_exempt
def pp(request, seat_info):
    if request.method == "POST":
        print('난 포스트')
    else:
        print('난 갯')

    context = {
        'aa' : seat_info,
    }
    return JsonResponse(context)


# @csrf_exempt
def pink_light(request, seat_info):
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

    # trains = Train.objects.all()

    # notifications = Notification.objects.all()
    
    # context = {
    #     'pink_light' : train,
    #     'trains' : trains,
    #     'notifications': notifications,
    # }
    # return render(request,'webserver/index.html', context)


# @csrf_exempt 
def station_status(request, station):
    print('뿜뿜뿜')

    if request.method == "POST":
        print('난 포스트')
    else:
        print('난 갯')

    print(station)
    api_url = 'http://swopenapi.seoul.go.kr/api/subway'
    key = config('SUBWAY_REAL_TIME')
    station_status = requests.get(f'{api_url}/{key}/json/realtimeStationArrival/0/5/{station}').json()
    print(station_status)
    data = station_status['realtimeArrivalList']
    print(len(data))
    t_no = data[0].get('btrainNo')
    t_no = "00" + t_no
    print(t_no)


    btrainNo = []
    trainLineNm = []
    arvlMsg2 = []
    empty_seat = []

    for i in range(len(data)):
        btrainNo.append(data[i].get('btrainNo'))
        trainLineNm.append(data[i].get('trainLineNm'))
        arvlMsg2.append(data[i].get('arvlMsg2'))
        empty_seat.append(i+1)

    context = {
        'btrainNo' : btrainNo,
        'trainLineNm' : trainLineNm,
        'arvlMsg2' : arvlMsg2,
        'empty_seat' : empty_seat,
    }
    return JsonResponse(context)


def station_info(request, train_name):
    print(train_name)
    context = {
        '상행' : [
            {
                '001002': [{
                    'slot_no' : '004',
                    'seat_no' : '01',
                    'empty' : False
                }, {
                    'slot_no' : '004',
                    'seat_no' : '02',                    
                    'empty' : False
                }, {
                    'slot_no' : '004',
                    'seat_no' : '03',                    
                    'empty' : False
                }, {
                    'slot_no' : '005',
                    'seat_no' : '01',                    
                    'empty' : False
                }, {
                    'slot_no' : '005',
                    'seat_no' : '02',                    
                    'empty' : False
                }, {
                    'slot_no' : '005',
                    'seat_no' : '03',                    
                    'empty' : True
                }, {
                    'slot_no' : '006',
                    'seat_no' : '01',                    
                    'empty' : False
                }, {
                    'slot_no' : '006',
                    'seat_no' : '02',                    
                    'empty' : False
                }, {
                    'slot_no' : '006',
                    'seat_no' : '03',                    
                    'empty' : True
                }
                ]
            },
            {
                '001003': [{
                    'slot_no' : '004',
                    'seat_no' : '01',
                    'empty' : True
                }, {
                    'slot_no' : '004',
                    'seat_no' : '02',
                    'empty' : True
                }, {
                    'slot_no' : '005',
                    'seat_no' : '01',                    
                    'empty' : True
                }, {
                    'slot_no' : '005',
                    'seat_no' : '01',                    
                    'empty' : True
                }, {
                    'slot_no' : '005',
                    'seat_no' : '02',                    
                    'empty' : True
                }, {
                    'slot_no' : '005',
                    'seat_no' : '03',                    
                    'empty' : True
                }, {
                    'slot_no' : '006',
                    'seat_no' : '01',                    
                    'empty' : False
                }, {
                    'slot_no' : '006',
                    'seat_no' : '02',                    
                    'empty' : False
                }, {
                    'slot_no' : '006',
                    'seat_no' : '03',                    
                    'empty' : False
                }
                ]
            }
        ],
        '하행' : [
            {
                '001004': [{
                    'slot_no' : '004',
                    'seat_no' : '01',
                    'empty' : False
                }, {
                    'slot_no' : '004',
                    'seat_no' : '02',                    
                    'empty' : True
                }, {
                    'slot_no' : '004',
                    'seat_no' : '03',                    
                    'empty' : True
                }, {
                    'slot_no' : '005',
                    'seat_no' : '01',                    
                    'empty' : True
                }, {
                    'slot_no' : '005',
                    'seat_no' : '02',                    
                    'empty' : True
                }, {
                    'slot_no' : '005',
                    'seat_no' : '03',                    
                    'empty' : False
                }, {
                    'slot_no' : '006',
                    'seat_no' : '01',                    
                    'empty' : True
                }, {
                    'slot_no' : '006',
                    'seat_no' : '02',                    
                    'empty' : True
                }, {
                    'slot_no' : '006',
                    'seat_no' : '03',                    
                    'empty' : True
                }
                ]
            },
            {
                '001005': [{
                    'slot_no' : '004',
                    'seat_no' : '01',
                    'empty' : False
                }, {
                    'slot_no' : '004',
                    'seat_no' : '02',
                    'empty' : False
                }, {
                    'slot_no' : '004',
                    'seat_no' : '03',                    
                    'empty' : True
                }, {
                    'slot_no' : '005',
                    'seat_no' : '01',                    
                    'empty' : False
                }, {
                    'slot_no' : '005',
                    'seat_no' : '02',                    
                    'empty' : False
                }, {
                    'slot_no' : '005',
                    'seat_no' : '03',                    
                    'empty' : True
                }, {
                    'slot_no' : '006',
                    'seat_no' : '01',                    
                    'empty' : True
                }, {
                    'slot_no' : '006',
                    'seat_no' : '02',                    
                    'empty' : True
                }, {
                    'slot_no' : '006',
                    'seat_no' : '03',                    
                    'empty' : True
                
                }]
            }
        ],

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
