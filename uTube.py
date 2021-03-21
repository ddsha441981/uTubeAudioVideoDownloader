import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from pytube import*
from pytube import Playlist
from PIL import Image, ImageTk
import PIL.Image
import requests
import io

class Youtube_app:
    # ==================Main Window GUI Start=========================
    def __init__(self,root):
        self.root = root
        self.root.title('uTube Video Downloader | by Deendayal Kumawat')
        self.root.geometry('500x430+300+50')
        self.root.resizable(width=False,height=False)
        self.root.config(bg = 'white')
        self.root.iconbitmap('icon/youtube.ico')        
    
        lbl_header = Label(self.root,text='uTube Video Downloader',font=('times new roman ',15,'bold'),bg='#262626',fg='white')
        lbl_header.pack(side=TOP,fill='x')

        lbl_url = Label(self.root,text='Video Url',font=('times new roman',15),bg='white')
        lbl_url.place(x=10,y=60)

        # Video Url
        self.var_url = StringVar()
        text_url = Entry(self.root,font=('times new roman',13),bg='lightyellow',textvariable=self.var_url)
        text_url.place(x=140,y=50,height=40,width = 350)

        lbl_file_type = Label(self.root,text='File Type',font=('times new roman',15),bg='white')
        lbl_file_type.place(x=10,y=110)

        #Radio Button

        self.var_fileType = StringVar()
        self.var_fileType.set('Video')

        video_radio = Radiobutton(self.root,text='Video',variable=self.var_fileType,value='Video',font=('times new roman',15),bg='white',activebackground='white')
        video_radio.place(x=120,y=110)
        audio_radio = Radiobutton(self.root,text='Audio',variable=self.var_fileType,value='Audio',font=('times new roman',15),bg='white',activebackground='white')
        audio_radio.place(x=220,y=110)

        # Search Button
        btn_search = Button(self.root,text='Search',command=self.search,font=('times new roman',15,'bold'),bg='green',fg='white').place(x=370,y=110,height=30,width=120)

        # Frame
        frame1 = Frame(self.root,bd=2,relief=RIDGE,bg='lightyellow')
        frame1.place(x=10,y=150,width=480,height=180)
        # Video Title
        self.video_title = Label(frame1,text='Video Title Here',font=('times new roman ',12,'bold'),bg='lightgrey',anchor='w')
        self.video_title.place(x=0,y=0,relwidth=1)
        # Video Image
        self.video_image = Label(frame1,text='Video \nImage',font=('times new roman ',15,'bold'),bg='lightgrey',relief=RIDGE,bd=2)
        self.video_image.place(x=5,y=30,width=180,height=140)
        # Video Description Label
        lbl_desc = Label(frame1,text='Video Description',font=('times new roman ',12,'bold'),bg='lightyellow').place(x=190,y=30)
        # Video Description Text
        self.video_desc = Text(frame1,font=('times new roman ',9),bg='lightgray')
        self.video_desc.place(x=190,y=60,width=280,height=110)

        #  Total Size
        self.lbl_Video_size = Label(self.root,text='Total Size: 0.00 MB',font=('times new roman ',13),bg='white')
        self.lbl_Video_size.place(x=10,y=335)

        # Downloading Percentage
        self.lbl_Video_download = Label(self.root,text='Downloading: 0.00 %',font=('times new roman ',13),bg='white')
        self.lbl_Video_download.place(x=165,y=335)

        # Clear and Download Button
        btn_clear = Button(self.root,text='Clear',command=self.clear,font=('times new roman',13,'bold'),bg='Red',fg='white').place(x=330,y=335,height=25,width=70)
        self.btn_download = Button(self.root,text='Download',command=self.download,state=DISABLED,font=('times new roman',13,'bold'),bg='Green',fg='white')
        self.btn_download.place(x=405,y=335,height=25,width=85)

        # Progressbar
        self.prog = ttk.Progressbar(self.root,orient=HORIZONTAL,length=590,mode='determinate')
        self.prog.place(x=10,y=370,width=480,height=25)

        # Error Message
        self.lbl_error_msg = Label(self.root,text='',font=('times new roman ',13),bg='white')
        self.lbl_error_msg.place(x=0,y=400,relwidth=1)
        
    # =============================Making Directory====================================
    if os.path.exists('Audios')==False:
        os.mkdir('Audios')
    if os.path.exists('Videos')==False:
        os.mkdir('Videos')

        
    # =============================Methods==============================================
    
    # ===================Search Methods=======================================
    def search(self):
        if self.var_url.get() =='':
            self.lbl_error_msg.config(text='Enter video URL first...',fg='red')
        else:
            yt = YouTube(self.var_url.get())
            # yt = YouTube(Playlist.video_urls)
            # Set title
            self.video_title.config(text=yt.title)
            
            # ===============Convert Image Url Into Image==============
            # get image from server
            response = requests.get(yt.thumbnail_url)
            img_Byte = io.BytesIO(response.content)
            self.img = PIL.Image.open(img_Byte)
            self.img = self.img.resize((180,140),PIL.Image.ANTIALIAS)
            self.img = ImageTk.PhotoImage(self.img)
            
            # pass the image on the GUI Label
            self.video_image.config(image=self.img)
            # ===============Convert Image Url Into Image End==============  
        
            # ===============set description==============
            self.video_desc.delete('1.0',END)
            self.video_desc.insert(END,yt.description[:800])
            # ===============set description End==============
            
            # ===============Fetch File Video or Audio==============

            if self.var_fileType.get()=='Video':
                select_File = yt.streams.filter(progressive=True).first()
            
            if self.var_fileType.get()=='Audio':
                select_File = yt.streams.filter(only_audio=True).first()
            # ===============Fetch File Video or Audio End==============  
            
            # ===============Get File Size In Bytes==============
            self.size_inBytes =  select_File.filesize
            max_size = self.size_inBytes/1024000
            self.mb = str(round(max_size,2))+'MB'
            self.lbl_Video_size.config(text='Total Size:'+self.mb)
            # Download Button Highlight
            self.btn_download.config(state=NORMAL)
    # ===============Search Method End====================================== 
    
    # ======================ProgressBar Start===============================
    def progress_bar(self,streams,chunk,bytes_remaining):
        # print(size_inBytes)
        percentage = (float(abs(bytes_remaining-self.size_inBytes)/self.size_inBytes))*float(100)
        self.prog['value']=percentage
        self.prog.update()
        self.lbl_Video_download.config(text=f'Downloading: {str(round(percentage,2))}%')
        if round(percentage,2) == 100:
            self.lbl_error_msg.config(text='Download Completed...',fg='green')
            # After Download file msg disabled
            self.btn_download.config(state=DISABLED)
    # ======================ProgressBar End====================================== 
    
    # ======================Download Method Start================================ 
    def download(self):
        yt = YouTube(self.var_url.get(),on_progress_callback=self.progress_bar)
        
        # self.video_title  = self.video_title 
        # print(self.video_title )
        # print ("File exists:"+str(os.path.exists(f'Videos/{self.video_title}')))
        
        if self.var_fileType.get()=='Video':
            select_File = yt.streams.filter(progressive=True).first()
            select_File.download('Videos/')
        
        if self.var_fileType.get()=='Audio':
            select_File = yt.streams.filter(only_audio=True).first()
            select_File.download('Audios/')
 # ======================Download Method End====================================== 
 
 # ======================Clear Method Start====================================== 
    def clear(self):
        self.var_fileType.set('Video')
        self.var_url.set('')
        self.prog['value']=0
        self.btn_download.config(state=DISABLED)
        self.lbl_error_msg.config(text='')
        self.video_title.config(text='Video Title Here..')
        self.video_image.config(image='')
        self.video_desc.delete('0.1',END)
        self.lbl_Video_size.config(text='Total Size: 0.00 MB')
        self.lbl_Video_download.config(text='Downloading: 0.00 %')
 # ======================Clear Method End====================================== 

 # ======================Main Window GUI End===================================
root = Tk()
obj = Youtube_app(root)
root.mainloop()