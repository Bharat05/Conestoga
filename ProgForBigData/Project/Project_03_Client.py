#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Course : PROG8420 – Programming for Big Data
Project : NLP - FAQ Chatbot
Members : Avi Lall, Charu Palkar, Bharat Thakur 

Date : 16-DEC-2020

Description : Using Google's DialogFlow to implement FAQ chatbot

"""
import threading, queue

from tkinter import *
import tkinter as tk

import os
import dialogflow_v2 as dialogflow
from google.api_core.exceptions import InvalidArgument

class Application(tk.Frame):

    def __init__(self, master=None,title='Not Set',s_hand=-1,s_num=-1):
        if s_hand == -1 or s_num == -1 :
            raise RuntimeError('Bad arguments for object!')
            
        super().__init__(master)
        self.master = master
        #self.grid(column=0,row=0, sticky=(N,W,E,S) )
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.pack(pady = 10, padx = 10)
        self.master.title(title)
        self.create_widgets()
        self.s_fd = s_hand
        self.s_id = s_num
        self.r_qu = queue.Queue(maxsize=128)

    def create_widgets(self):       
        # Create var to read entry box
        self.e_txt = tk.StringVar()
        #Quit button
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")
        # Frame for Field & Button
        self.frame = tk.Frame(self)
        # Label
        tk.Label(self.frame, text="Please enter -> ").pack(side="left")
        # Text Input field
        self.e_fld = tk.Entry(self.frame,textvariable = self.e_txt)
        self.e_fld.bind("<Return>",lambda e:self.send_request())
        self.e_fld.pack(side="left")
       
        # Text Send Button
        self.send = tk.Button(self.frame, text="Send", fg="red",
                              command=self.send_request)
        self.send.pack(side="left")
        
        self.frame.pack(side='bottom')
        
        self.frame1 = tk.Frame(self)
        # Text Box for results
        self.tx = tk.Text(self.frame1, height = 40 , width = 40 )
        self.tx.pack(side="left", fill="y")
        sb = tk.Scrollbar(self.frame1, orient="vertical")
        sb.config(command=self.tx.yview)
        sb.pack(side="left", fill="y")            
        self.tx.config(yscrollcommand=sb.set)
        
        self.frame1.pack(side='top')
        
    # DialogFlow response writer event handler
    def write_response(self):
        q_hd = self.r_qu.get()
        try:
            r_hd = self.s_fd.detect_intent(session=self.s_id, query_input=q_hd)
        except InvalidArgument:
            raise
        
        self.tx.insert(tk.END,'Agent : ' + r_hd.query_result.fulfillment_text + '\n')
        self.tx.see(tk.END)
        
    # Current count event handler
    def send_request(self):
        # Fetch request from test box
        e_str = self.e_txt.get()
        if len(e_str) > 0 :
            self.tx.insert(tk.END,'You(' + os.path.basename(self.s_id) + ') : ' + e_str + '\n')
            self.tx.see(tk.END)
            self.e_txt.set("") 
            # Create request and send to engine
            in_str = dialogflow.types.TextInput(text=e_str, language_code=DIALOGFLOW_LANGUAGE_CODE)
            self.r_qu.put(dialogflow.types.QueryInput(text=in_str))
        pass
        
  
#Main program
# Setup connection to engine
# defining parameters
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/dev/Desktop/Conestoga/PROG8420 Big Data Prog/Assignments/Project/BigDataProgConestoga-Project/../faq-chatbot_private_key.json"
DIALOGFLOW_PROJECT_ID = 'faq-chatbot-hvho'
DIALOGFLOW_LANGUAGE_CODE = 'en'
SESSION_ID = '1'

s_fd = dialogflow.SessionsClient()
s_id = s_fd.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
#4. Build and display menu
root = tk.Tk()
app = Application(master=root,title='TOYOTA - FAQ CHAT',s_hand = s_fd, s_num = s_id)

r_thr = threading.Thread(target=app.write_response)
r_thr.start()

app.mainloop()