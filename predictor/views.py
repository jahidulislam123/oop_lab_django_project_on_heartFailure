from django.shortcuts import render,redirect
from sklearn import linear_model
from .forms import Parameters
from .regressor import LogitRegression
import pandas as pd
import numpy as np
from . import regressor
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression 
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login 
from django.contrib.auth.decorators import login_required
from .models import HeartData,DoctorHospital
from django.core.mail import send_mail
# Create your views here.



def index(request): #Directs the user to home page . Different for authenticated and non authenticated users.
    if request.user.is_authenticated:
        if request.method=='POST':
    
            form=Parameters(request.POST)
            if form.is_valid():
                age=form.cleaned_data['age']
                sex=form.cleaned_data['sex']
                cp=form.cleaned_data['cp']
                trestbps=form.cleaned_data['trestbps']
                chol=form.cleaned_data['chol']
                fbs=form.cleaned_data['fbs']
                restcg=form.cleaned_data['restcg']
                thalach=form.cleaned_data['thalach']
                exang=form.cleaned_data['exang']
                oldpeak=form.cleaned_data['oldpeak']
                slope=form.cleaned_data['slope']
                ca=form.cleaned_data['ca']
                thal=form.cleaned_data['thal']


                X,Y=regressor.find() 
                X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 1/3, random_state = 0 )
                #model = LogitRegression(learning_rate=0.01 , iterations=1000)
                model = LogitRegression(learning_rate=0.0001 , iterations=1000)
                model.fit(X_train, Y_train)
                output , output1 = model.predict(np.array([age,sex,cp,trestbps,chol,fbs,restcg,thalach,exang,oldpeak,slope,ca,thal]).reshape(1,-1))
                danger = 'high' if output == 1 else 'low'
                output1=output1[0]
                saved_data = HeartData(age=age ,  # Saving to database
                sex = sex,
                cp = cp,
                trestbps = trestbps,
                chol = chol,
                fbs = fbs,
                restcg = restcg , 
                thalach = thalach , 
                exang = exang,
                oldpeak = oldpeak,
                slope = slope,
                ca = ca,
                thal = thal,
                owner = request.user,
                probability = output1
                )  #Saved the authenticated users data in the database.
                saved_data.save()
                return render(request , 'output2.html',{'output1':output1 , 'danger':danger})


        form = Parameters()
        return render(request , 'user.html', {'form':form})
    return render(request , 'index.html')



def contact(request): #Diplays contact page . Sends email to HDPS using SMTP.
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        title = request.POST.get('title1')
        message = request.POST.get('message')
        
        send_mail(title , message+'\n'+'From : '+name+'\n'+'Email : '+email ,from_email=email, recipient_list=['focusus1@gmail.com']) #Sends mail to HDPS
    return render(request , 'contact.html')

def about(request): #Displays about us page.
    return render(request , 'about.html')

# Login and Logout





def signin(request): # For the user to sign in.
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.warning(request,'Invalid Credentials')
            return redirect('signin')

        
    else:
        return render(request,'signin.html')


def signup(request): #For the user to resister or sign up.

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        
        if User.objects.filter(username=username).exists():
            messages.info(request,'Username taken')
            return redirect('signup')
        elif User.objects.filter(email=email).exists():
            messages.info(request,'Email taken')
            return redirect('signup')
        else:
            user = User.objects.create_user(username=username, password=password,email=email,first_name = first_name,last_name=last_name)
            
            user.save()
            
            messages.success(request,f"User {username} created!")
            return redirect('signin')
        #return redirect('/')
    else:   
        return render(request,'signup.html')


def signout(request): # In order to logout from the website
    auth.logout(request)
    return redirect('/')


# End login