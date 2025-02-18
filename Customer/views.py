from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
import os
import subprocess
import wolframalpha
import pyttsx3
import tkinter
import json
import operator
import datetime
import speech_recognition as sr
import time
from django.db import transaction


def takeCommand():
    r = sr.Recognizer()     
    with sr.Microphone() as source:         
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
  
    try:
        print("Recognizing...")   
        query = r.recognize_google(audio, language ='en-in')
        print(f"User said: {query}\n")
  
    except Exception as e:
        print(e)   
        print("Unable to Recognize your voice.") 
        return "None"
    redirect('query')     
    return query


def speak(audio):
	engine = pyttsx3.init('sapi5')
	voices = engine.getProperty('voices')
	engine.setProperty('voice', voices[1].id)
	engine.say(audio)
	engine.runAndWait()

def query(request):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("speak what you want to do in gmail login, compose, inbox, logout, send")
        print("Listening...")            
        r.pause_threshold = 1
        audio = r.listen(source)
        print("Recognizing...")   
        n1 = r.recognize_google(audio, language ='en-in')
        
        print("You said : {}".format(n1))
            
        if n1 == "logout":
            return redirect("user_logout")
        elif n1 == "inbox":
            return redirect("inbox")
        elif n1 == "send":
            return redirect("sent")
        elif n1 == "compose":
            return redirect("compose")        
        elif n1 == "login":
            return redirect("user_login")
        else:
            speak("voice doesnot recognize please try again")
            return redirect('query')
        
    

def user_login(request):
    if request.session.has_key('username'):  
        return redirect('query')
    else:
        speak("Welcome")
        time.sleep(3)
        speak("Please Login Using Your name")
        r = sr.Recognizer()
        with sr.Microphone() as source:

            speak("speak")
            print("Listening...")            
            r.pause_threshold = 1
            audio = r.listen(source)
            print("Recognizing...")   
            
            name = r.recognize_google(audio, language ='en-in')	
        
            print("You said : {}".format(name))
            data=customer.objects.filter(name=name)
            if data.exists():            
                user = data.first()
                request.session['username'] = user.name
                request.session['user_id'] = user.id
                speak("you are Login successfully")
                return render (request, 'login.html')

            else:
                speak('Invalid username')
    return render (request, 'login.html')

def user_logout(request):
    if 'username' in request.session:
        del request.session['username']
        speak("You have logged out Successfully")        
    return render (request, 'login.html')

def compose(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = customer.objects.get(id=user_id)
        
        speak("Please enter your username for send email")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            speak("speak")
            print("Listening...")
            r.pause_threshold = 2
            audio = r.listen(source)
            print("Recognizing...")
            try: 
                sender_name = r.recognize_google(audio, language ='en-in')
                speak("your sender name is " + sender_name )                               				
            except:
                speak("Sorry! Voice Does not recognize please try again")
                return redirect('compose')

        speak("Please enter your receiver name for send email")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            speak("speak")
            print("Listening...")
            r.pause_threshold = 2
            audio = r.listen(source)
            print("Recognizing...")
            try: 
                receiver_name = r.recognize_google(audio, language ='en-in')
                speak("your receiver name is " + receiver_name )                               				
            except:
                speak("Sorry! Voice Does not recognize please try again")
                return redirect('compose')

        speak("Please enter your subject for the email")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            speak("speak")
            print("Listening...")
            r.pause_threshold = 2
            audio = r.listen(source)
            print("Recognizing...")
            try: 
                subject = r.recognize_google(audio, language ='en-in')
                speak("your subject is " + subject )                               				
            except:
                speak("Sorry! Voice Does not recognize please try again")
                return redirect('compose')

        speak("Please enter your body for the email")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            speak("speak")
            print("Listening...")
            r.pause_threshold = 2
            audio = r.listen(source)
            print("Recognizing...")
            try: 
                body = r.recognize_google(audio, language ='en-in')
                speak("your body  is " + body )                               				
            except:
                speak("Sorry! Voice Does not recognize please try again")
                return redirect('compose')       

        try:
            sender_email = customer.objects.filter(name=sender_name).values('email_id').get()['email_id']
            receiver_email = customer.objects.filter(name=receiver_name).values('email_id').get()['email_id']
            
            with transaction.atomic():
                sender_mail = SenderMail.objects.create(send_Id=user, sender=sender_email, receiver=receiver_email, subject=subject, body=body)
                receiver_mail = ReceiverMail.objects.create(inbox_Id=user, sender=sender_email, receiver=receiver_email, subject=subject, body=body)
                
                if sender_mail and receiver_mail:
                    speak("Mail send successfully")
                    return render(request, 'compose.html')
                else:
                    speak('Failed to send message!')
                    return redirect('query')
                    
        except customer.DoesNotExist:
            speak('Sender or receiver email does not exist in our database! please try again')  
            return redirect('compose') # Redirect to clear the form after successful submission          
    else:
        speak('User not logged in!')
        return redirect('login')  # Redirect to login page if user is not logged in
    
    return render(request, 'compose.html')

def inbox(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']

        inbox_messages = ReceiverMail.objects.filter(inbox_Id=user_id).order_by('-id')
        mail_ids = inbox_messages.values_list('id', flat=True)
        mail_count = len(mail_ids)
        count = str(mail_count)

        if mail_count >= 1:
            speak('you have totally ' + count + ' mails')
            speak("which mail do you want to read")        
            try:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    speak("speak")
                    print("Listening...")            
                    r.pause_threshold = 1
                    audio = r.listen(source)
                    print("Recognizing...")

                    n = r.recognize_google(audio, language ='en-in')

                    print("You said : {}".format(n))

                    num = int(n)
                    print(num)
                    num1 = num%10
                    print(num1)
                    num1-=1
                    print(num1)
                    id = int(mail_ids[num1])                   
                    return redirect('view_mail_inbox',id)
            except:  
                speak("Sorry could not recognize what you said")  
                return redirect('query')  
        else:
            speak('You have totaly '+ count+' mails')
            return redirect('query')      
        return render(request, 'inbox.html', {'inbox_messages': inbox_messages})
    else:
        # Handle case when user is not logged in
        return redirect('login')

def sent(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        sent_messages = SenderMail.objects.filter(send_Id=user_id).order_by('-id')

        mails = sent_messages.values_list('id', flat=True)
        mailcount = len(mails)
        count = str(mailcount)

        if mailcount >= 1:
            speak('you have totally ' + count + ' mails')
            speak("which mail do you want to read")
        else:
            speak('you have ' + count + 'mails')
            return redirect('query')

        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                speak("speak")
                print("Listening...")            
                r.pause_threshold = 1
                audio = r.listen(source)
                print("Recognizing...")   
                n = r.recognize_google(audio, language ='en-in')
                print("You said : {}".format(n))

                numm = int(n)
                print(numm)
                num2 = numm%10
                print(num2)
                num2-=1
                print(num2)
                id = int(mails[num2])                
                
                return redirect('view_mail_sent',id)
        except Exception as e:
            print(e)  
            speak("Sorry could not recognize what you said")  
            return redirect('query')        
        return render(request, 'sent.html', {'sent_messages': sent_messages})
    else:
        # Handle case when user is not logged in
        return redirect('login')

def view_mail_inbox(request,id):
    inbox_message=ReceiverMail.objects.get(id=id)
    context={
        'inbox_message':inbox_message
    }
    try:
        speak('subject of the mail is' + inbox_message.subject)
        speak('sender email id is'+inbox_message.sender)
        speak('content of the mail is:'+inbox_message.body)
    except:
        speak("sorry! unable to read mail")
        return redirect('query')
    return render(request,'view_mail.html',context)

def view_mail_sent(request,id):
    sent_message=SenderMail.objects.get(id=id)
    context={
        'sent_message':sent_message
    }

    try:
        speak('subject of the mail is' + sent_message.subject)
        speak('sender email id is'+sent_message.sender)
        speak('content of the mail is:'+sent_message.body)
        return render(request,'view_mail_sent.html',context)

    except:
        speak("sorry! unable to read mail")        
        return redirect('query')
    return render(request,'view_mail_sent.html',context)


