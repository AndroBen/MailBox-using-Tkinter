from tkinter import *
from tkinter import messagebox
from ttkwidgets.autocomplete import AutocompleteEntry
from smtplib import SMTP
import email
import imaplib
import os
import html2text
from email import policy
import speech_recognition as sr

listener=sr.Recognizer()
window = Tk()
window.title("LOGIN")
window.iconbitmap("mailicon.ico")
mail=SMTP("smtp.gmail.com",587)
mail.starttls()
rmail=imaplib.IMAP4_SSL("imap.gmail.com")
i=0

def submit():
    global mail
    mail.login(user.get(),passwd.get())
    global rmail
    rmail.login(user.get(),passwd.get())
    rmail.select('inbox')
    status,data=rmail.search(None,'ALL')#search(key,value,mail)eg key="From",value="google@gmail.com"
    global rmail_id
    rmail_id=[]
    for block in data:
        rmail_id+=block.split()
    rmail_id.reverse()
    rmail_id=rmail_id[0:]
    b1=Button(window,text="Send Mail",bg="#285D68",fg="white",font=("Ropa Sans",14,"bold"),borderwidth=0,command=sendmail)
    b2=Button(window,text="Receive Mail",bg="#285D68",fg="white",font=("Ropa Sans",13,"bold"),borderwidth=0,command=receivemail)
    b1.place(x=600,y=530,width = 120,height = 50)
    b2.place(x=800,y=530,width = 120,height = 50)
    
def sendmail():
    global top
    top=Toplevel(window)
    top.geometry("1000x600")
    top.title("SEND MAIL")
    top.iconbitmap("mailicon.ico")
    global to
    to=StringVar()
    global message
    message=StringVar()
    canva=Canvas(top,width=1000,height=600)
    canva.pack(fill="both",expand=True)
    global bg_img
    bg_img = PhotoImage(file = "bg.png")
    canva.create_image(0,0,image=bg_img,anchor="nw")
    canva.create_text(250,50,text="SEND MAIL",font=("Ropa Sans",18,"bold"),fill="white")
    canva.create_text(100,200,text="To",font=("Ropa Sans",14,"bold"),fill="white")
    s1 = Entry(top,bd = 0,bg = "#cfeded",highlightthickness = 0,textvariable=to,width=55,font=("Ropa Sans",14,"bold"))
    ew1=canva.create_window(150,200,anchor="nw",window=s1)
    canva.create_text(100,260,text="Message",font=("Ropa Sans",14,"bold"),fill="white")
    s2 = Text(top,bd = 0,bg = "#cfeded",highlightthickness = 0,width=40,height=15,font=("Ropa Sans",12))
    ew2=canva.create_window(150,250,anchor="nw",window=s2)
    global send_img
    send_img=PhotoImage(file=f"sent.png")
    global talk_img
    talk_img=PhotoImage(file=f"talkb.png")
    b1=Button(top,image=send_img,width=180,height=30,bd=0,command=lambda:send(s2.get(1.0,END)))
    b2=Button(top,image=talk_img,width=100,height=100,text="talk",bd=0,borderwidth=0,bg="#1d2f3f",command=lambda:talk(s2))
    ew3=canva.create_window(150,550,anchor="nw",window=b1)
    ew4=canva.create_window(550,290,anchor="nw",window=b2)
    
def talk(s2):
    try:
        with sr.Microphone() as source:
            print("listening")
            voice=listener.listen(source)
            command=listener.recognize_google(voice)
            print(command)
            s2.insert(1.0,command)
    except Exception:
        print("Error")

def send(message):
   global to
   global user
   global mail
   print(to.get())
   print(user.get())
   print(message)
   if(mail.sendmail(user.get(),to.get(),message)):
       
       messagebox.showinfo("success","sent successfully")
   else:
       top.destroy()
def receivemail():
    global back
    back=Toplevel(window)
    back.geometry("1000x600")
    back.title("receive mail")
    back.iconbitmap("mailicon.ico")
    global frm
    frm=StringVar()
    global subject
    subject=StringVar()
    global content
    content=StringVar()
    canva=Canvas(back,width=1000,height=600)
    canva.pack(fill="both",expand=True)
    global bg_img
    bg_img = PhotoImage(file = "bg.png")
    canva.create_image(0,0,image=bg_img,anchor="nw")
    canva.create_text(250,40,text="RECEIVE MAIL",font=("Ropa Sans",18,"bold"),fill="white")
    canva.create_text(100,100,text="From",font=("Ropa Sans",14,"bold"),fill="white")
    global f1
    f1 = Entry(back,bd = 0,bg = "#cfeded",highlightthickness = 0,textvariable=frm,width=55,font=("Ropa Sans",13,"bold"))
    w1=canva.create_window(150,100,anchor="nw",window=f1)
    canva.create_text(100,160,text="Subject",font=("Ropa Sans",14,"bold"),fill="white")
    global f2
    f2 = Text(back,bd = 0,bg = "#cfeded",highlightthickness = 0,width=75,height=5,font=("Ropa Sans",12))
    w2=canva.create_window(150,150,anchor="nw",window=f2)
    canva.create_text(100,270,text="Content",font=("Ropa Sans",14,"bold"),fill="white")
    global f3
    f3 = Text(back,bd = 0,bg = "#cfeded",highlightthickness = 0,width=75,height=15,font=("Ropa Sans",12))
    w3=canva.create_window(150,260,anchor="nw",window=f3)
    global recv_img
    recv_img=PhotoImage(file=f"righ.png")
    global left_img
    left_img=PhotoImage(file=f"left.png")
    
    b5=Button(back,image=recv_img,width=100,height=60,bd=0,borderwidth=0,bg="black",command=lambda:receiv("n"))
    b6=Button(back,image=left_img,width=100,height=60,bd=0,borderwidth=0,bg="black",command=lambda:receiv("b"))
    ew3=canva.create_window(450,533,anchor="nw",window=b5)
    ew4=canva.create_window(150,533,anchor="nw",window=b6)

def receiv(direction):
    global i
    global rmail_id
    if direction=="n":
        i=i+1
        m=rmail_id[i]
        
    if direction=="b":
        i=i-1
        m=rmail_id[i]
    h=html2text.HTML2Text()
    h.ignore_links=True
    status,mdata=rmail.fetch(m,'(RFC822)')
    for response_part in mdata:
        if isinstance(response_part,tuple):
            message=email.message_from_bytes(response_part[1],policy=policy.SMTP)
            fromm=message['From']
            subject=message['Subject']
            if message.is_multipart():
                content=''
                for part in message.get_payload():
                    if part.get_content_type()=='text/plain':
                        content+=part.get_payload()
                    if part.get_content_type() == "text/html":
                        a=part.get_payload()
                        text=a.replace("b'","")
                        
                        text=h.handle(f'''{text}''')
                        text=text.replace("\\r\\n","")
                        text=text.replace("'","")
                        content+=text
            
            else:
                content=message.get_payload(decode=True)
            global f1
            global f2
            global f3
            f1.delete(0,END)
            f2.delete(1.0,END)
            f3.delete(1.0,END)
            f1.insert(0,fromm)
            f2.insert(1.0,subject)
            f3.insert(1.0,content)
            print(f'From:{fromm}')
            
            print(f'Subject:{subject}')
            print(f'Content:{content}')



window.geometry("1000x600")
window.configure(bg = "#FFFFFF")
canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 600,
    width = 1000,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"background.png")
background = canvas.create_image(
    487.5, 300.0,
    image=background_img)
global user
user=StringVar()
global passwd
passwd=StringVar()
entry0_img = PhotoImage(file = f"img_textBox0.png")
entry0_bg = canvas.create_image(
    780.0, 199.5,
    image = entry0_img)
entry0 = Entry(
    bd=0,
    bg = "#cfeded",
    highlightthickness = 0,
    textvariable=user
    )

entry0.place(
    x = 656.0, y = 176,
    width = 248.0,
    height = 45)

entry1_img = PhotoImage(file = f"img_textBox1.png")
entry1_bg = canvas.create_image(
    780.0, 315.5,
    image = entry1_img)

entry1 = Entry(show="*",
    bd = 0,
    bg = "#c1e8e5",
    highlightthickness = 0,
    textvariable=passwd)

entry1.place(
    x = 656.0, y = 292,
    width = 248.0,
    height = 45)

img0 = PhotoImage(file = f"img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = submit,
    relief = "flat")

b0.place(
    x = 678, y = 430,
    width = 196,
    height = 72)

window.resizable(False, False)
window.mainloop()
