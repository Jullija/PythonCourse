import tkinter as tk
from tkinter import ttk
import paho.mqtt.client as mqtt
import speech_recognition as sr
import pyttsx3 as tts


myName = ""
client = ""
addedLines = 0
lineCounter = 0

BROKER = "localhost"
SUBSCRIPTION_TOPIC = "msg/spk" 
PUBLICATION_TOPIC = "msg/mic"



def send(topic, payload):
    global client
    client.publish(topic, payload, retain=True)


def changeText(text, maxWidth=70):
    words = text.split()
    allLines = []
    currLine = []

    for word in words:
        if len(' '.join(currLine + [word])) <= maxWidth:
            currLine.append(word)
        else:
            allLines.append(' '.join(currLine))
            currLine = [word]

    if currLine:
        allLines.append(' '.join(currLine))

    return allLines



def addMessageOnCanvas(sentText, param="e", knownUser=False, knownSender=None):
    global lineCounter
    global myName
    global addedLines
    if addedLines == 5 or lineCounter >= 5:
        canvas.delete("all")
        addedLines = 0
        lineCounter = 0
        textY = 50 + lineCounter * 35
    else:
        textY = 50 + lineCounter * 35 
        addedLines += 1


    if knownSender:
        clientName = knownSender
    else:
        clientName = myName

    canvasWidth = canvas.winfo_width()

    if knownUser:
        textX = 50
    else:
        textX = canvasWidth - 50

    
    textToShow = changeText("[" + clientName + "]: " + sentText)

    for line in textToShow:
        textY = 50 + lineCounter * 35 
        canvas.create_text(textX, textY, text=line, fill='black', anchor=param)
        lineCounter += 1



def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    arr = payload.split(':', 1)
    if (len(arr) != 2):
        sender = "Unknown"
        message = "".join(arr)
    else:
        sender,message = arr
        sender = sender.replace(" ", "")
    



def init_speaker():
    global engine
    engine = tts.init()
    engine.setProperty('volume', 0.7)
    engine.setProperty('rate', 190)


    

def speakNow(text, sender):
    engine.say("Wiadomość od " + sender + ": " + text)
    engine.runAndWait()


def init_broker():
    global client
    global myName
    client = mqtt.Client("Julia")
    myName = client._client_id.decode('utf-8')
    client.on_message = on_message
    client.connect(BROKER)
    client.loop_start()
    client.subscribe([(SUBSCRIPTION_TOPIC, 0)])

def sendMessage():
    global myName
    text = writeHere.get('1.0', tk.END).strip()

    send(PUBLICATION_TOPIC, text)
    addMessageOnCanvas(text,"w",True,myName)
    writeHere.delete('1.0', tk.END)


def speechToText():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language='pl_PL')
        send(PUBLICATION_TOPIC, text)
        addMessageOnCanvas(text,"w",True,myName)
        speakNow(text, myName)
    except sr.UnknownValueError:
        print('nie rozumiem')
    except sr.RequestError as e:
        print('error:', e)


def removePlaceholder(event=None):
    if writeHere.get('1.0', tk.END).strip() == 'Wpisz wiadomość...':
        writeHere.delete('1.0', tk.END)
        writeHere.config(fg="black")


#bottom layer with buttons
bottom = tk.Tk()
bottom.title("Voice communicator")

bottom.geometry('700x500')
bottom.configure(bg='#ffd1ee')
bottom.resizable(width=True, height=False)


#canvas
canvasFrame = tk.Frame(bottom, bg='#ffd1ee')
canvasFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

canvas = tk.Canvas(canvasFrame, bg='#ffffff', highlightthickness=0)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


#place for write
writeHereFrame = tk.Frame(bottom, bg="#ffd1ee")
writeHereFrame.pack(fill=tk.X, padx=50, pady=10)

writeHere = tk.Text(writeHereFrame, background='white', width=20, height=2.5, borderwidth=0, wrap=tk.WORD, highlightthickness=0)
writeHere.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)

writeHere.bind('<FocusIn>', removePlaceholder)

writeHere.insert('1.0', 'Wpisz wiadomość...')
writeHere.config(fg='#777777')


#buttons
sendButton = tk.Button(writeHereFrame, text="Send", command=sendMessage, width=7, pady=8, borderwidth=0, highlightthickness=0)
sendButton.pack(side=tk.LEFT, padx=5, pady=5)

buttonFrame = tk.Frame(bottom, bg = '#ffd1ee')
buttonFrame.pack(padx=20, pady=10)

speaker = tk.Button(buttonFrame, text="Speak", command=speechToText, width=10, height=6, relief=tk.RAISED, bd = 0, highlightthickness=0)
speaker.pack(side=tk.TOP, padx=5)



init_broker()
init_speaker()

bottom.mainloop()
client.loop_stop()