from django.shortcuts import render
from django.contrib import messages
from users.models import UserRegistrationModel,UserImagePredictinModel
from .utility.AlgorithmExecutions import KNNclassifier

# Create your views here.

def AdminLoginCheck(request):
    if request.method == 'POST':
        usrid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')
        print("User ID is = ", usrid)
        if usrid == 'admin' and pswd == 'admin':
            return render(request, 'admins/AdminHome.html')
        elif usrid == 'Admin' and pswd == 'Admin':
            return render(request, 'admins/AdminHome.html')
        else:
            messages.success(request, 'Please Check Your Login Details')
    return render(request, 'AdminLogin.html', {})


def AdminHome(request):
    return render(request, 'admins/AdminHome.html')


def ViewRegisteredUsers(request):
    data = UserRegistrationModel.objects.all()
    return render(request, 'admins/RegisteredUsers.html', {'data': data})


def AdminActivaUsers(request):
    if request.method == 'GET':
        id = request.GET.get('uid')
        status = 'activated'
        print("PID = ", id, status)
        UserRegistrationModel.objects.filter(id=id).update(status=status)
        data = UserRegistrationModel.objects.all()
        return render(request, 'admins/RegisteredUsers.html', {'data': data})

def AdminStressDetected(request):
    data = UserImagePredictinModel.objects.all()
    return render(request, 'admins/AllUsersStressView.html', {'data': data})

def AdminKNNResults(request):
    obj = KNNclassifier()
    df, accuracy, classificationerror, sensitivity, Specificity, fsp, precision = obj.getKnnResults()
    df.rename(
        columns={'Target': 'Target', 'ECG(mV)': 'Time pressure', 'EMG(mV)': 'Interruption', 'Foot GSR(mV)': 'Stress',
                 'Hand GSR(mV)': 'Physical Demand', 'HR(bpm)': 'Performance', 'RESP(mV)': 'Frustration', },
        inplace=True)
    data = df.to_html()
    return render(request, 'admins/AdminKnnResults.html',
                  {'data': data, 'accuracy': accuracy, 'classificationerror': classificationerror,
                   'sensitivity': sensitivity, "Specificity": Specificity, 'fsp': fsp, 'precision': precision})
