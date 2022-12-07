import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os #operating system
import random
import time
import sys
import PyPDF2
# import selenium
import pyautogui
import rotatescreen as rs
import speedtest #py -3.6 -m pip install speedtest-cli    -- py -3.6 -m pip install --user  py-notifier
# import cv2
import pygame
import pywhatkit    
from pygame.locals import * # Basic pygame imports
from PyQt5.QtWidgets import * # pip install PyQtWebEngine
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import *
import datefinder
import winsound
from pynotifier import Notification  #py-notifier
from email.message import EmailMessage
import smtplib




engine= pyttsx3.init("sapi5")
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)
# print(voices) it return voice location in windows




browser_path = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(browser_path))

webbrowser = webbrowser.get('chrome') 





def speak(audio):
    engine.say(audio)
    engine.runAndWait()
name='User'
def wishMe():
    speak("""Welcome to the Group of T L M S. I'm Hajmola!. And I am your assistant.""")   
    r=sr.Recognizer()
   
    with sr.Microphone() as source:
        speak("PLEASE TELL ME YOUR NAME :")
        print('Listening your name...')
        r.pause_threshold=0.8
        r.energy_threshold=1000   
        audio=r.listen(source)

    try:
        print("Recognizing...")    
        global name
        name=r.recognize_google(audio,language='en-in')
        speak(name)
        print("your name is : ",name)

    except Exception as e:
        speak("Hello user")        
        return "None" 

    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("good morning! Please Tell me how may i help you")
    elif hour>=12 and hour<18:
            speak("good afternoon! Please Tell me how may i help you")
    else:
        speak("Good evening! Please Tell me how may i help you") 



def takeCommand():

                r=sr.Recognizer()
                with sr.Microphone() as source:
                    print("Listening your voice........")
                    r.pause_threshold=1.2
                    r.energy_threshold=1000    
                    audio=r.listen(source)

                try:
                    print("Recognizing...")    
                    query=r.recognize_google(audio,language='en-in')
                    print("You said : ",query)

                except Exception as e:
                 
                    print("Say that again please...")
                    return "None" 

                return query 

        





def task_Execution():
    wishMe()
    speak("Thank you!") 
    while True:
        query = takeCommand().lower()
        global name       

        if 'wikipedia' in query:
            try:
                speak("Searching in wikipedia please wait")    
                query=query.replace("wikipedia", "")
                results=wikipedia.summary(query, sentences=2)
                speak("According to wikipedia")
                print(results)
                speak(results)
            except:
                print("somethimg going wrong")



        elif 'open command prompt' in query or 'cmd' in query:
            os.system("start cmd")

        
        elif 'play game' in query or 'play a game' in query:
            try:
                speak("Opening flappy game by HAJMOLA")
                # Global Variables for the game
                FPS = 32
                SCREENWIDTH = 289
                SCREENHEIGHT = 511
                SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
                GROUNDY = SCREENHEIGHT * 0.8
                GAME_SPRITES = {}
                GAME_SOUNDS = {}
                PLAYER = 'gallery/sprites/bird.png'
                BACKGROUND = 'gallery/sprites/background.png'
                PIPE = 'gallery/sprites/pipe.png'
                
                def welcomeScreen():
                    """
                    Shows welcome images on the screen
                    """

                    playerx = int(SCREENWIDTH/5)
                    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
                    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
                    messagey = int(SCREENHEIGHT*0.13)
                    basex = 0
                    while True:
                        for event in pygame.event.get():
                            # if user clicks on cross button, close the game
                            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                                pygame.quit()
                                sys.exit()

                            # If the user presses space or up key, start the game for them
                            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                                return
                            else:
                                SCREEN.blit(GAME_SPRITES['background'], (0, 0))    
                                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))    
                                SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey ))    
                                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))    
                                pygame.display.update()
                                FPSCLOCK.tick(FPS)

                def mainGame():
                    score = 0
                    playerx = int(SCREENWIDTH/5)
                    playery = int(SCREENWIDTH/2)
                    basex = 0

                    # Create 2 pipes for blitting on the screen
                    newPipe1 = getRandomPipe()
                    newPipe2 = getRandomPipe()

                    # my List of upper pipes
                    upperPipes = [
                        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
                        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},
                    ]
                    # my List of lower pipes
                    lowerPipes = [
                        {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
                        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
                    ]

                    pipeVelX = -4

                    playerVelY = -9
                    playerMaxVelY = 10
                    playerMinVelY = -8
                    playerAccY = 1

                    playerFlapAccv = -8 # velocity while flapping
                    playerFlapped = False # It is true only when the bird is flapping


                    while True:
                        for event in pygame.event.get():
                            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                                pygame.quit()
                                sys.exit()
                            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                                if playery > 0:
                                    playerVelY = playerFlapAccv
                                    playerFlapped = True
                                    GAME_SOUNDS['wing'].play()


                        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes) # This function will return true if the player is crashed
                        if crashTest:
                            return     

                        #check for score
                        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
                        for pipe in upperPipes:
                            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
                            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                                score +=1
                                print(f"Your score is {score}") 
                                GAME_SOUNDS['point'].play()


                        if playerVelY <playerMaxVelY and not playerFlapped:
                            playerVelY += playerAccY

                        if playerFlapped:
                            playerFlapped = False            
                        playerHeight = GAME_SPRITES['player'].get_height()
                        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

                        # move pipes to the left
                        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
                            upperPipe['x'] += pipeVelX
                            lowerPipe['x'] += pipeVelX

                        # Add a new pipe when the first is about to cross the leftmost part of the screen
                        if 0<upperPipes[0]['x']<5:
                            newpipe = getRandomPipe()
                            upperPipes.append(newpipe[0])
                            lowerPipes.append(newpipe[1])

                        # if the pipe is out of the screen, remove it
                        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
                            upperPipes.pop(0)
                            lowerPipes.pop(0)
                        
                        # Lets blit our sprites now
                        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
                            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
                            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

                        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                        myDigits = [int(x) for x in list(str(score))]
                        width = 0
                        for digit in myDigits:
                            width += GAME_SPRITES['numbers'][digit].get_width()
                        Xoffset = (SCREENWIDTH - width)/2

                        for digit in myDigits:
                            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
                            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
                        pygame.display.update()
                        FPSCLOCK.tick(FPS)

                def isCollide(playerx, playery, upperPipes, lowerPipes):
                    if playery> GROUNDY - 25  or playery<0:
                        GAME_SOUNDS['hit'].play()
                        return True
                    
                    for pipe in upperPipes:
                        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
                        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
                            GAME_SOUNDS['hit'].play()
                            return True

                    for pipe in lowerPipes:
                        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
                            GAME_SOUNDS['hit'].play()
                            return True

                    return False

                def getRandomPipe():
                    """
                    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
                    """
                    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
                    offset = SCREENHEIGHT/3
                    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()  - 1.2 *offset))
                    pipeX = SCREENWIDTH + 10
                    y1 = pipeHeight - y2 + offset
                    pipe = [
                        {'x': pipeX, 'y': -y1}, #upper Pipe
                        {'x': pipeX, 'y': y2} #lower Pipe
                    ]
                    return pipe






                if __name__ == "__main__":
                    # This will be the main point from where our game will start
                    pygame.init() # Initialize all pygame's modules
                    FPSCLOCK = pygame.time.Clock()
                    pygame.display.set_caption('Flappy Bird by Hajmola AI')
                    GAME_SPRITES['numbers'] = ( 
                        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
                        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
                        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
                        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
                        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
                        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
                        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
                        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
                        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
                        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
                    )

                    GAME_SPRITES['message'] =pygame.image.load('gallery/sprites/message.png').convert_alpha()
                    GAME_SPRITES['base'] =pygame.image.load('gallery/sprites/base.png').convert_alpha()
                    GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load( PIPE).convert_alpha(), 180), 
                    pygame.image.load(PIPE).convert_alpha()
                    )

                    # Game sounds
                    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
                    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
                    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
                    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
                    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

                    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
                    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

                    while True:
                        welcomeScreen() 
                        mainGame()  
            except:
                speak("Something Going Wrong!! Please try again After sometime")


        elif 'open chrome' in query :
            try:
                speak("Opening Chrome")
                code_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
                os.startfile(code_path)
            except:
                speak("Chrome Didn't Find Now i am opening my own Browser")
                class MainWindow(QMainWindow):
                    def __init__(self):
                        super(MainWindow,self).__init__()
                        self.browser=QWebEngineView()
                        self.browser.setUrl(QUrl('http://google.com'))
                        self.setCentralWidget(self.browser)
                        self.showMaximized()

                        # Hajmola's NavBar
                        navbar=QToolBar()
                        self.addToolBar(navbar)

                        home_btn=QAction('Home',self)
                        home_btn.triggered.connect(self.navigate_home)
                        navbar.addAction(home_btn)


                        back_btn=QAction('Back',self)
                        back_btn.triggered.connect(self.browser.back)
                        navbar.addAction(back_btn)

                        for_btn=QAction('Forward',self)
                        for_btn.triggered.connect(self.browser.forward)
                        navbar.addAction(for_btn)

                        rload_btn=QAction('Reload',self)
                        rload_btn.triggered.connect(self.browser.reload)
                        navbar.addAction(rload_btn)

                        self.url_bar=QLineEdit()
                        self.url_bar.returnPressed.connect(self.navigate_to_url)
                        navbar.addWidget(self.url_bar)
                        self.browser.urlChanged.connect(self.update_url)


                    def navigate_home(self):
                        self.browser.setUrl(QUrl("http://google.com"))
                    

                    def navigate_to_url(self):
                        url=self.url_bar.text()
                        self.browser.setUrl(QUrl(url))


                    def update_url(self,url1):
                        self.url_bar.setText(url1.toString())



                HajmoBrowser=QApplication(sys.argv)
                QApplication.setApplicationName('Anardana Browser')
                window=MainWindow()
                HajmoBrowser.exec_()    


        elif 'anardana browser' in query or 'browser' in query:
            try:
                speak('Anardana browser opened')
                class MainWindow(QMainWindow):
                        def __init__(self):
                            super(MainWindow,self).__init__()
                            self.browser=QWebEngineView()
                            self.browser.setUrl(QUrl('http://google.com'))
                            self.setCentralWidget(self.browser)
                            self.showMaximized()

                            # Hajmola's NavBar
                            navbar=QToolBar()
                            self.addToolBar(navbar)

                            home_btn=QAction('Home',self)
                            home_btn.triggered.connect(self.navigate_home)
                            navbar.addAction(home_btn)


                            back_btn=QAction('Back',self)
                            back_btn.triggered.connect(self.browser.back)
                            navbar.addAction(back_btn)

                            for_btn=QAction('Forward',self)
                            for_btn.triggered.connect(self.browser.forward)
                            navbar.addAction(for_btn)

                            rload_btn=QAction('Reload',self)
                            rload_btn.triggered.connect(self.browser.reload)
                            navbar.addAction(rload_btn)

                            self.url_bar=QLineEdit()
                            self.url_bar.returnPressed.connect(self.navigate_to_url)
                            navbar.addWidget(self.url_bar)
                            self.browser.urlChanged.connect(self.update_url)


                        def navigate_home(self):
                            self.browser.setUrl(QUrl("http://google.com"))
                        

                        def navigate_to_url(self):
                            url=self.url_bar.text()
                            self.browser.setUrl(QUrl(url))


                        def update_url(self,url1):
                            self.url_bar.setText(url1.toString())



                HajmoBrowser=QApplication(sys.argv)
                QApplication.setApplicationName('Anardana Browser')
                window=MainWindow()
                HajmoBrowser.exec_()  
                
            except:
                speak("Please try after sometime")
            
                
        elif 'close chrome' in query:
            speak("closing Chrome")
            os.system("taskkill /im chrome.exe /f") 

        elif 'send email' in query or 'send a mail' in query or 'send mail' in query or 'send a email' in query:
            try:
                listener = sr.Recognizer()
                engine = pyttsx3.init()


                def talk(text):
                    engine.say(text)
                    engine.runAndWait()


                def get_info():
                    try:
                        with sr.Microphone() as source:
                            print('listening...')
                            voice = listener.listen(source)
                            info = listener.recognize_google(voice,language='en-in')
                            print(info)
                            return info.lower()
                    except:
                        pass


                def send_email(receiver, subject, message):
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    # Make sure to give app access in your Google account
                    server.login('hajmolaemail@gmail.com', 'hajmola"123')
                    email = EmailMessage()
                    email['From'] = 'Sender_Email'
                    email['To'] = receiver
                    email['Subject'] = subject
                    email.set_content(message)
                    server.send_message(email)


                email_list = {
                    'sushant': 'mr.sushant.shandilya@gmail.com',
                    'manish': 'mani10soccer@gmail.com',
                    'songs': 'ssongs.space@gmail.com',
                    'tejas': 'ktejas558@gmail.com',
                    'lucky': 'lakshitlksht@gmail.com',
                    'naresh gill':'drnareshkumarigill@gmail.com',
                    'pankaj malik':'srlecturercomputer@gmail.com',
                    
                }


                def get_email_info():
                    talk('To Whom you want to send email')
                    name1 = get_info()
                    receiver = email_list[name1]
                    print(receiver)
                    talk('What is the subject of your email?')
                    subject = get_info()
                    talk('Tell me the text in your email')
                    message = get_info()
                    send_email(receiver, subject, message)
                    talk(r'Hey {}. Your email is sent'.format(name))
                    talk('Do you want to send more email?')
                    send_more = get_info()
                    if 'yes' in send_more:
                        get_email_info()


                get_email_info()
            except:
                speak(r"Dear {}! Something going wrong please try again".format(name))

        elif 'audiobook' in query or 'read pdf' in query or 'about hajmola' in query:
            try:
                speaker=pyttsx3.init()
                pathB=input("Enter location of pdf : ")
                book=open(pathB,'rb')
                pdfReader=PyPDF2.PdfFileReader(book)
                totalPages=pdfReader.numPages
                print("Total Pages are :- ",totalPages) 
                startingPageNum=int(input("Enter page number where you want to start : "))

                for i in range(startingPageNum,totalPages):
                    page=pdfReader.getPage(startingPageNum)
                    textpdf=page.extractText()
                    speaker.say(textpdf)
                    speaker.runAndWait()
            except:
                print(r"{} You may entered incorrect credentials. Please try again".format(name))
                speak(r"{} You may entered incorrect credentials. Please try again".format(name))


        elif 'open youtube' in query:
            try:
                speak("Youtube opening please wait")
                webbrowser.open("youtube.com")
            except:
                speak("I am unable to open youtube ")    

        elif 'change my name' in query or 'change name' in query:
            speak("You can change your name in just few seconds")
            r=sr.Recognizer()
            with sr.Microphone() as source:
                speak("PLEASE TELL ME YOUR NAME :")
                print('Listening your name...')
                r.pause_threshold=1.2
                r.energy_threshold=1000    
                audio=r.listen(source)

            try:
                
                print("Recognizing...")
                name=r.recognize_google(audio,language='en-in')
                print("your name is : ", name)
                speak(r"{} your name is updated".format(name))
                speak(name)
                               
            except Exception as e:
                speak("Hello ")        
                return "None" 
            hour=int(datetime.datetime.now().hour)
            if hour>=0 and hour<12:
                speak("good morning! Please Tell me how may i help you")
            elif hour>=12 and hour<18:
                    speak("good afternoon! Please Tell me how may i help you")
            else:
                speak("Good evening! Please Tell me how may i help you")
        
        
        
        elif 'notification' in query:
            try:
                strh=int(input("Enter hour in interger : "))
                strm=int(input("Enter minutes in interger : "))
                print(strh)
                print(strm)
                r=sr.Recognizer()
                with sr.Microphone() as source:
                    speak("Speak Now!! I am listening your description........ ")
                    print("Speak Now!! I am listening your description........ ")
                    r.pause_threshold=1.2
                    r.energy_threshold=1000    
                    audio=r.listen(source)

                try:
                    print("Recognizing...")    
                    desc=r.recognize_google(audio,language='en-in')
                    print("You said : ",desc)

                except Exception as e:
                    print(e)
                    print("Say that again please...")
                    return "None" 

                    
                while True:
                    if strh == datetime.datetime.now().hour:
                        if strm==datetime.datetime.now().minute:
                            Notification(
                                title='Reminder',
                                description=desc,
                                duration=10
                            ).send()    
            except:
                print("Something going wrong")


        elif 'on specific time' in query or 'given time' in query:
            try:            
                numbe=input("Enter a number with country code or group link : ")
                time.sleep(2)
                r=sr.Recognizer()
                with sr.Microphone() as source:
                    speak("Speak Now!! I am listening your message........ ")
                    print("Speak Now!! I am listening your message........ ")
                    r.pause_threshold=1.2
                    r.energy_threshold=1000    
                    audio=r.listen(source)

                try:
                    print("Recognizing...")    
                    mssg=r.recognize_google(audio,language='en-in')
                    print("You said : ",mssg)

                except Exception as e:
                    print(e)
                    print("Say that again please...")
                    return "None" 
                t1=int(input("Enter time in hour :"))
                m1=int(input("Enter time n minutes : "))
                pywhatkit.sendwhatmsg(numbe,mssg,t1,m1)
            except:
                speak("Please try again!")

        
        
        elif 'whatsapp message' in query or 'message on whatsApp' in query or 'open whatsapp' in query:   
            try:
                times=int(input("Enter times :- "))
                time.sleep(2)
                webbrowser.open("https://web.whatsapp.com/")
                r=sr.Recognizer()
                with sr.Microphone() as source:
                    speak("Speak Now!! I am listening your message........ ")
                    print("Speak Now!! I am listening your message........ ")
                    r.pause_threshold=1.2
                    r.energy_threshold=1000    
                    audio=r.listen(source)

                try:
                    print("Recognizing...")    
                    msgwhats=r.recognize_google(audio,language='en-in')
                    print("You said : ",msgwhats)

                except Exception as e:
                    print(e)
                    print("Say that again please...")
                    return "None" 
                time.sleep(30)

                for i in range(times):
                    pyautogui.write(msgwhats,interval=0.1)
                    pyautogui.press("enter")
                    print(i)
            except:
                speak("Please try again")
        
       


        elif 'add' in query or 'sum' in query or 'addition' in query or 'some' in query:
            try:
                speak("Please speak numbers for addition")
                listener=sr.Recognizer()
                try:
                    with sr.Microphone() as source:
                        print("listening first number")
                        speak("listening first number")
                        voice=listener.listen(source)
                        print('recognizing..')
                        number1=listener.recognize_google(voice,language='en-in')
                        print(number1)
                        x=int(number1)
                        

                except:
                    pass
                try:
                    with sr.Microphone() as source:
                        print("listening second number")
                        speak("listening second number")
                        voice=listener.listen(source)
                        print('recognizing..')
                        number2=listener.recognize_google(voice,language='en-in')
                        print(number2)
                        x1=int(number2)
                        
                except:
                    pass
                
            
                sum1=x+x1
                speak(r"Addition of two number is {}".format(sum1))
                print(r"Addition of two number is {}".format(sum1))
            except:
                print(r'Sorry {}! there is some connection issue'.format(name))
                speak(r'Sorry {}! there is some connection issue'.format(name))



        elif 'subtract' in query or 'abstract' in query or 'minus' in query or 'subtraction' in query or '-' in query:
            try:
                speak("Please speak numbers for substraction")
                listener=sr.Recognizer()
                try:
                    with sr.Microphone() as source:
                        print("listening first number")
                        speak("listening first number")
                        voice=listener.listen(source)
                        print('recognizing..')
                        number1=listener.recognize_google(voice,language='en-in')
                        print(number1)
                        x=int(number1)
                        

                except:
                    pass
                try:
                    with sr.Microphone() as source:
                        print("listening second number")
                        speak("listening second number")
                        voice=listener.listen(source)
                        print('recognizing..')
                        number2=listener.recognize_google(voice,language='en-in')
                        print(number2)
                        x1=int(number2)
                        
                except:
                    pass
            
                sub1=x-x1
                speak(r"Substaction of two number is {}".format(sub1))
                print(r"Substaction of two number is {}".format(sub1))
            except:
                print(r'Sorry {}! there is some connection issue'.format(name))
                speak(r'Sorry {}! there is some connection issue'.format(name))


        
        elif 'multiply' in query or 'mul' in query or 'multiplication' in query or '*' in query:
            try:
                speak("Please speak numbers for multiplication")
                listener=sr.Recognizer()
                try:
                    with sr.Microphone() as source:
                        print("listening first number")
                        speak("listening first number")
                        voice=listener.listen(source)
                        print('recognizing..')
                        number1=listener.recognize_google(voice,language='en-in')
                        print(number1)
                        x=int(number1)
                        

                except:
                    pass
                try:
                    with sr.Microphone() as source:
                        print("listening second number")
                        speak("listening second number")
                        voice=listener.listen(source)
                        print('recognizing..')
                        number2=listener.recognize_google(voice,language='en-in')
                        print(number2)
                        x1=int(number2)
                        
                except:
                    pass

                
                mul1=x*x1
                speak(r"Multiplication of two number is {}".format(mul1))
                print(r"Multiplication of two number is {}".format(mul1))
            except:
                print(r'Sorry {}! there is some connection issue'.format(name))
                speak(r'Sorry {}! there is some connection issue'.format(name))




        elif 'divide' in query or 'div' in query or 'division' in query or '/' in query:
            try:
                speak("Please speak numbers for divide")
                listener=sr.Recognizer()
                try:
                    with sr.Microphone() as source:
                        print("listening first number")
                        speak("listening first number")
                        voice=listener.listen(source)
                        print('recognizing..')
                        number1=listener.recognize_google(voice,language='en-in')
                        print(number1)
                        x=int(number1)
                        

                except:
                    pass
                try:
                    with sr.Microphone() as source:
                        print("listening second number")
                        speak("listening second number")
                        voice=listener.listen(source)
                        print('recognizing..')
                        number2=listener.recognize_google(voice,language='en-in')
                        print(number2)
                        x1=int(number2)
                        
                except:
                    pass

                
                mul1=x/x1
                speak(r"Divide of two number is {}".format(mul1))
                print(r"Divide of two number is {}".format(mul1))
            except:
                print(r'Sorry {}! there is some connection issue'.format(name))
                speak(r'Sorry {}! there is some connection issue'.format(name))




        elif 'thank you' in query or 'thanks' in query or 'thankyou' in query:
            speak(r"Welcome {}! i am happy to help you. Thanks for choosing Hajmola!!".format(name))    




        elif "shutdown" in query or 'power off' in query or 'power of' in query:
            try:
                speak("System will shutdown within 10 seconds")
                os.system("shutdown /s /t 10")
                for i in range(5,0,-1):
                    speak(i)
                    time.sleep(1)
            except:
                speak("Unable to shutdown ")
        
        elif "restart" in query:
            try:
                speak("System will restart within 10 seconds")
                os.system("shutdown /r /t 10")
                for i in range(5,0,-1):
                    speak(i)
                    time.sleep(1)
            except:
                speak("unable to Restart Something went Wrong")



        elif 'open my website' in query or 'open our website' in query:
            speak(" Opening our website please wait") 
            try:
                webbrowser.open("ssongs.space")
            except:
                speak("Not Able to open Website")

        elif 'open facebook' in query:   
            speak("Opening Facebook")
            try:
                webbrowser.open("facebook.com") 
            except:
                speak("Not Able to open facebook")


        elif 'open instagram' in query:   
            speak("Opening instagram")
            try:    
                webbrowser.open("instagram.com") 
            except:
                speak("Not Able to open Instagram")


        elif 'open stack overflow' in query:
            speak("opening stackOverFlow") 
            try:
                webbrowser.open("stackoverflow.com")
            except:
                speak("Not Able to open stackoverflow.com")


        elif 'open w3schools' in query:         
            speak("opening w3schools") 
            try:
                webbrowser.open("w3schools.com")
            except:
                speak("Not Able to open w3schools.com")


        elif 'open google' in query:
            speak("opening Google")
            try:
                webbrowser.open("google.com") 
            except:
                speak("Not Able to open google.com")


        elif 'change song' in query:
            try:
                music_dir= "C:\\songs"
                songs=os.listdir(music_dir)
        
                song=random.choice(songs)
                os.startfile(os.path.join(music_dir,song))
            except Exception as e:
                music_dir= "D:\\songs"
                songs=os.listdir(music_dir)
        
                song=random.choice(songs)
                os.startfile(os.path.join(music_dir,song))
            except:
                speak("Sorry! Please keep songs folder in C or D drive. Now i am opening a website for playing songs")
                print("Sorry! Please keep songs folder in C or D drive example C:\\songs or D:\\songs")
                webbrowser.open("ssongs.space")

        elif 'play song' in query:
            try:
                music_dir= ('C:\\songs')
                songs=os.listdir(music_dir)
            
                song=random.choice(songs)
                os.startfile(os.path.join(music_dir,song))
            except Exception as e:
                music_dir= "D:\\songs"
                songs=os.listdir(music_dir)
        
                song=random.choice(songs)
                os.startfile(os.path.join(music_dir,song))
            except:
                speak("Sorry! Please keep songs folder in C or D drive. Now i am opening a website for playing songs")
                print("Sorry! Please keep songs folder in C or D drive example C:\\songs or D:\\songs")
                webbrowser.open('ssongs.space')


        elif 'asal mein' in query or 'favourite song' in query:
            try:
                speak("playing Pagal Gurnam Bhullar your favourite song")  
                fav= "C:\\songs\\Pagal Gurnam Bhullar (SongsMp3.Com).mp3"
                os.startfile(os.path.join(fav))
            except Exception as e:
                fav= "D:\\songs\\Pagal Gurnam Bhullar (SongsMp3.Com).mp3"
                os.startfile(os.path.join(fav))
            except:
                speak("Sorry! Please keep songs folder in C or D drive")
                print("Sorry! Please keep songs folder in C or D drive example C:\\songs or D:\\songs")

        
        elif "your name" in query:
            speak("My name is Hajmola.. Hajmola is developed by T. L. M. S. for Government Polytechnic sonipat Project")
            print("My name is Hajmola.. Hajmola is developed by T. L. M. S. for Government Polytechnic sonipat Project")

        elif 'how are you' in query:
            speak(r"I'm fine! But please! don't Plug out cable from switch board HAHHAHAHAHHA  And.......... How are you {}!".format(name))
            print(r"I'm fine! But please! don't Plug out cable from switch board  hahahha And How are you {}!".format(name))
        
        elif 'i am fine' in query or "am good" in query or 'i am excellent' in query or "am also good" in query or 'also fine' in query:
            speak(r"Sound great {}! its good to hear".format(name))
        
        elif 'not fine' in query or "not good" in query or 'tired' in query or 'not much fine' in query or "not much good" in query or "not felling well" in query :
            speak("bad to hear!!.. For good feelling!. you can play game!.. JUST SAY \n PLAY GAME")

        elif 'introduction' in query or 'yourself' in query:
            speak(r"""HEllO! {} I am Hajmola!. Your virtual assistance. And Always ready to serve you. CODED BY T. L. M. S group""".format(name))    

        elif 'tlms' in query or 't l m s' in query or 'plms' in query or 'clms' in query or 'tms' in query or 'tlm' in query or 'group' in query or 't l m' in query:
            print("TLMS is a short form of developers name T for tejas L for lakshit M for Manish and S for Sushant")
            speak("TLMS is a short form of developers name T for tejas L for lakshit M for Manish and S for Sushant")
            
        
    

        elif 'time' in query:
            try:
                strTime=datetime.datetime.now().strftime("%H : %M : %S")
                print(strTime)
                speak(f"the time is {strTime}")
            except:
                speak('Please try again')

        elif 'code' in query:
            try:
                code_path="C:\\Users\\susha\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                os.startfile(code_path)
            except:
                speak('Sorry VS Code not found. Now i am opening online code editor')
                webbrowser.open('https://www.programiz.com/python-programming/online-compiler/')

        elif 'run python' in query:
            try:
                py_path="C:\\Users\\susha\\AppData\\Local\\Programs\\Python\\Python36\\python.exe"
                os.startfile(py_path)    
            except:
                speak('Python Not found')
                webbrowser.open("https://www.w3schools.com/python/trypython.asp?filename=demo_variables_global4")
        
        elif 'show me even number' in query:
            try:
                speak("I am showing Even numbers")
                for i in range(2,21,2): # range 
                    print(i)
            except:
                speak("Something went Wrong")
        
        elif 'even number' in query:
            try:
                speak("I am speaking Even numbers")
                for i in range(2,21,2):
                    speak(i)
            except:
                speak("Something went Wrong")

        elif 'odd number' in query:
            try:
                for i in range(1,20,2):
                    speak(i)
            except:
                speak("Something went Wrong")

        elif "screenshot" in query:
            try:
                im = pyautogui.screenshot()
                im.save(r'C:\\abcd.png')
                im.save(r'C:\\abcd1.png')
                strTime=datetime.datetime.now().strftime("%A %d %B %Y %I%M%p")
                print(strTime)
                a= "C://"+ strTime
                im.save(r"{}.png".format(a))
                speak("ScreenShot Done!")
            except:
                speak("Something went Wrong")  

        elif 'audionotes' in query or 'audio notes' in query or 'audio note' in query:
            try:
                strTime=datetime.datetime.now().strftime("%A %d %B %Y %I%M%p")
                print(strTime)
                a= "C://"+ strTime
                b=a +'.txt'
                listener=sr.Recognizer()
                with sr.Microphone() as source:
                    print("listening... please speak your notes")
                    speak("listening... please speak your notes")
                    voice=listener.listen(source)
                    print('recognizing..')
                    mssg1=listener.recognize_google(voice,language='en-in')
                    print(mssg1)
                with open(b,'w') as f:
                    f.write(mssg1) 
                    speak("Audio notes saved on C drive")
            except:
                speak(r"{} Something went wrong please try again".format(name))
            


        elif "rotate screen" in query:
            try:
                screen=rs.get_primary_display()
                for i in range(10):
                    time.sleep(1)
                    screen.rotate_to(i*90 % 360)  
            except:
                speak("Sorry! Please Try Again")

        elif "speed test" in query:
            try:
                speak("We are checking current maximum network DOWNLOAD AND UPLOADING speed...  \n please wait!.............................")
                print("processing....")
                speed=speedtest.Speedtest()
                # speak("We are checking current maximum network DOWNLOAD AND UPLOADING speed...  \n please wait!.............................")
                a=speed.download()
                b=a/1000000
                a1=speed.upload()
                b1=a1/1000000
                print('Done')
                print("Maximum Downloading Speed is {0:.2f} MbPS".format(b))
                speak("Maximum Downloading Speed is {0:.2f} MbPS".format(b))
                print("Maximum Uploading Speed is {0:.2f} MbPS".format(b1))
                speak("Maximum Uploading Speed is {0:.2f} MbPS".format(b1))
            except:
                speak("you can check internet speed from here!")
                webbrowser.open('https://www.speedtest.net/')

        elif 'how you know my name' in query:
            speak(r"your name is {}. i know your name because you told me".format(name))


        elif 'tell my name' in query or 'my name' in query:
            speak(r'your name is {}'.format(name))
            print(r'your name is {}'.format(name))

        
       
        elif 'what are you doing' in query or 'what do you do' in query:
            speak('i am your persnal assistant and.......i am here to server you! Please tell me how can i help you')


        elif 'sleep' in query:
            speak(r"Dear {}! I'm in sleep mode... For Starting Me please Say Hajmola".format(name))
            break

        elif 'exit' in query:
            sys.exit()    
    
        elif query in query:
            print(query)
            print("Not Found") 

        




if __name__ == "__main__":
    
    speak("For starting me please say wake up Hajmola")
    while True:
        activate = takeCommand().lower()
        if 'hajmola' in activate or "wake up" in activate or "hey" in activate:
            task_Execution()

        elif 'exit' in activate:
            sys.exit()

