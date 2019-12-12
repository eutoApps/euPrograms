import tkinter as tk
from tkinter import ttk #for the horizontal/vertical lines
import winsound #to play the bell sound file (.wav only)
from datetime import datetime as dt
from datetime import timedelta
import time as tt1#to make the program only run once a minute
import sched as ss1#to schedule rather than have infinite loop with sleep
import threading #so that the program doesn't lock and freeze
from tkinter.filedialog import askopenfilename #to choose a new audio file
from functools import partial #to have one launch() function, not 5 for each sch

#CONSTANTS / Global Vars
paddX,paddY = 10,5
fontt = "Courier 10 bold"
resourcesFolder = 'PythonBellResources_DO_NOT_MOVE_DELETE_OR_RENAME/'
defFile = resourcesFolder+'wesley_DEFAULT_times_DO_NOT_MOVE_OR_DELETE.txt'
chapelFile = resourcesFolder+'wesley_CHAPEL_times_DO_NOT_MOVE_OR_DELETE.txt'
extra1File = resourcesFolder+'wesley_EXTRA1_times_DO_NOT_MOVE_OR_DELETE.txt'
extra2File = resourcesFolder+'wesley_EXTRA2_times_DO_NOT_MOVE_OR_DELETE.txt'
extra3File = resourcesFolder+'wesley_EXTRA3_times_DO_NOT_MOVE_OR_DELETE.txt'
extra4File = resourcesFolder+'wesley_EXTRA4_times_DO_NOT_MOVE_OR_DELETE.txt'
extra5File = resourcesFolder+'wesley_EXTRA5_times_DO_NOT_MOVE_OR_DELETE.txt'
audioFileTxtAddress = resourcesFolder+'wesleyAudioFIle_DO_NOT_MOVE_OR_DELETE.txt'
whichFile = defFile #set the default to Default
defaultAudioFile = resourcesFolder+'newhourlychimebeg.wav'
audioFile = defaultAudioFile

#Read from the audio txt file if possible
try:
    with open(audioFileTxtAddress,'r') as f:
        audioFile = f.readline()
except:pass

#Popup a window with a custom message
def popper(msgForLabel,labelOrMsg='m'):
    popup = tk.Toplevel(mW)
    popup.geometry('200x200')
    msg = tk.Message(popup,text=msgForLabel)
    if labelOrMsg=='l':
        msg = tk.Label(popup,text=msgForLabel)
    msg.pack()
    msg.place(relx=.5, rely=.4, anchor="c")
    closeBtn = tk.Button(popup,text='Close',command=popup.destroy)
    closeBtn.pack()
    closeBtn.place(relx=.5, rely=.7, anchor="c")
    mW.wait_window(popup) #so that mW waits for this window to be read before changing the audio file

####Set up the main Window (mW)
mW = tk.Tk()
mW.title('Wesley Bell Program')
#mW.geometry('1000x1000')
mW.resizable(False,False)
mW.columnconfigure(0,uniform="fred")
mW.columnconfigure(2)
mW.columnconfigure(4,uniform="fred")
logo = tk.PhotoImage(file=resourcesFolder+
                     "wesley logo_DO_NOT_MOVE_DELETE_OR_RENAME.png")
imgLabel = tk.Label(mW,image=logo,bg='white')
imgLabel.grid(row=0,column=0,padx=paddX,pady=paddY)
programTitleLabel = tk.Label(mW, text='Wesley Bell\nProgram',font=("Courier 18 bold"))
programTitleLabel.place(anchor='center')
programTitleLabel.grid(row=0,column=2,padx=paddX,pady=paddY,columnspan=3,sticky='EW')
#Horizontal Line
hSeparator = ttk.Separator(mW,orient='horizontal')
hSeparator.grid(row=1,column=0,pady=paddY,columnspan=5, sticky='EW')

####Set up 3 Frames, left center right
bsFrame = tk.Frame(mW) #bell schedules' frame
bsFrame.grid(row=3,column=0,sticky='NS',padx=paddX,pady=(0,10))
vl1 = ttk.Separator(mW, orient='vertical') #Vertical Line 1
vl1.grid(row=2,column=1,pady=paddY,sticky='NS')
tsFrame = tk.Frame(mW) #time slots' frame
tsFrame.grid(row=3,column=2,pady=(0,10))
vl2 = ttk.Separator(mW, orient='vertical') #Vertical Line 2
vl2.grid(row=2,column=3,pady=paddY,sticky='NS')
ssFrame = tk.Frame(mW) #start save frame
ssFrame.grid(row=3,column=4,sticky='NS',padx=paddX,pady=(0,10))

####BELL SCHEDULES & File Chooser, Bell Ringer
whichProgramSV = tk.StringVar() #This is a Time Slots label. It's here cause I need to reference it in the launch functions
bsLabel = tk.Label(bsFrame, text='Schedule', font=('Courier 9 bold'))
bsLabel.grid(row=0,column=0,pady=paddY)
#This function fills in the time slots
def fillTimeSlots():
    try:
        with open(whichFile,'r') as tsFile:
            timeSlotWhichLine=0
            lines = tsFile.readlines()
            last = lines[-1]
            for line in lines:
                timeSlotStringVars[timeSlotWhichLine].set(line.strip())
                timeSlotWhichLine+=1
    except:
        for ts in timeSlotStringVars:ts.set('')
#Schedule Buttons
def launch(l,f):
    whichProgramSV.set(l)
    global whichFile
    whichFile = f
    fillTimeSlots()
defaultBtn = tk.Button(bsFrame,text='Default',command=partial(launch,'Default',defFile),relief='groove')
defaultBtn.grid(row=1,column=0,pady=paddY)
chapelBtn = tk.Button(bsFrame,text='Chapel',command=partial(launch,'Chapel',chapelFile),relief='groove')
chapelBtn.grid(row=2,column=0,pady=paddY)
extra1Btn = tk.Button(bsFrame,text='Extra 1',command=partial(launch,'Extra 1',extra1File),relief='groove')
extra1Btn.grid(row=3,column=0,pady=paddY)
extra2Btn = tk.Button(bsFrame,text='Extra 2',command=partial(launch,'Extra 2',extra2File),relief='groove')
extra2Btn.grid(row=4,column=0,pady=paddY)
extra3Btn = tk.Button(bsFrame,text='Extra 3',command=partial(launch,'Extra 3',extra3File),relief='groove')
extra3Btn.grid(row=5,column=0,pady=paddY)


#Audio Section
#Choose a new audio file
def chooseBell():
    global audioFile
    popper('The current audio file:\n{}'.format(audioFile))
    tk.Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    audioFile = askopenfilename() #change the audio file
    #save the new audio file (if successful)
    try:
        with open(audioFileTxtAddress,'w') as f:
            if not audioFile:
                f.write(defaultAudioFile)
                audioFile = defaultAudioFile
            else:
                f.write(audioFile)
    except:pass
    popper('The newly updated audio file is:\n{}'.format(audioFile))
audioLabel = tk.Label(bsFrame,text='Audio',font=(fontt))
audioLabel.grid(row=6,column=0,pady=paddY)
bellBtn = tk.Button(bsFrame,text='Bell',command=chooseBell,relief='groove')
bellBtn.grid(row=7,column=0,pady=paddY)
#Ring the bell once
def ringOnce():
    winsound.PlaySound(audioFile,winsound.SND_FILENAME)
def ringOnceThread():
    roT = threading.Thread(target=ringOnce)
    roT.start()
ringBtn = tk.Button(bsFrame,text='Ring x1',command=ringOnceThread,relief='groove')
ringBtn.grid(row=8,column=0,pady=paddY)

####TIME SLOTS
whichProgramSV.set('Default')
whichProgramLabel = tk.Label(tsFrame, textvariable=whichProgramSV,font=(fontt))
whichProgramLabel.grid(row=0,column=0,pady=paddY,columnspan=2)

timeSlotEFs = [i for i in range(24)]#create a list length 24. the list content doesn't matter
timeSlotStringVars = [tk.StringVar() for i in range(24)]
#Define all the needed StringVars
for i in range(len(timeSlotStringVars)):
    timeSlotStringVars[i] = tk.StringVar()
#Define, and place all the Time Slot tk.Entry Fields
timeSlotRow,timeSlotCol=1,0
#The first time slot is gonna be at row0 col0. The second row0 col1. The third row1 col1, and so forth.
timeSlotEFs[0] = tk.Entry(tsFrame,textvariable=timeSlotStringVars[0],
                          width=6,font='Times 12',relief='flat')
timeSlotEFs[0].grid(row=timeSlotRow,column=timeSlotCol,padx=3,pady=1)
alternator = 1
for i in range(1,len(timeSlotEFs)):
    if alternator%2!=0:
        timeSlotCol=1
    else:
        timeSlotRow+=1
        timeSlotCol=0
    alternator+=1
    timeSlotEFs[i] = tk.Entry(tsFrame,textvariable=timeSlotStringVars[i],
                              width=6,font='Times 12',relief='flat')
    timeSlotEFs[i].grid(row=timeSlotRow,column=timeSlotCol,padx=3,pady=1)
#Fill in time slots with times, if a save file exists
fillTimeSlots()

####ACTION (Start, Stop, Save) & Status
statusSV = tk.StringVar() #says whether program is running or not. I put up here cause need to reference it soon
ssLabel = tk.Label(ssFrame, text='Action', font=(fontt))
ssLabel.grid(row=0,column=0,pady=paddY)
s = ss1.scheduler(tt1.time,tt1.sleep)#I dunno know what this line does, other than set a Scheduler
e = None #e will be an event passed to s
################Start
#Sigh. Eek, note that this scheduler's loop is /supposed/ to call itself!
#I spent an hour splitting start into 2 functions, then wondering
#why window wouldn't close!. It was cuz sched only ran 1x, then stopped, so e wasnone
def start(whichFileToPlayHere,lines,absNow):
    global e
    #check current time with timeslots
    hourMinute = dt.now()
    timee = hourMinute.strftime('%H%M')    
    for line in lines:
        if line.strip()==timee:
            winsound.PlaySound(audioFile,winsound.SND_FILENAME)
    absNow+=60#recursive add 60. must be here, not as arg3 of e*
    #enterabs ensures every 60 seconds without delay
    e = s.enterabs(absNow+60,1,start,(whichFileToPlayHere,lines,absNow))#not here*
    s.run()#must be at the end of this function
def start2():
    global statusSV,statusLabel2
    if statusSV.get()=='On':return#only have 1 thread running
    statusSV.set('On')
    statusLabel2.configure(fg='green')
    whichFileToPlayHere = whichFile
    try:
        with open(whichFileToPlayHere,'r') as tsFile:
            lines = tsFile.readlines()
    except:pass
    #get the current time, and floor it to the nearest minute for scheduler
    now = tt1.time()
    nowDT = dt.fromtimestamp(now)
    flooredDT = nowDT - timedelta(0,nowDT.second)
    flooredNow = dt.timestamp(flooredDT)-60#-60 is cause recursive has +60 each loop
    #the thread
    t = threading.Thread(target=start,args=(whichFileToPlayHere,lines,flooredNow))
    t.start() #not t.run(), but t.start()
startBtn = tk.Button(ssFrame, text='START', command=start2,relief='groove')
startBtn.grid(row=1,column=0,pady=paddY)
################Stop
def stop():
    global statusLabel2
    try:s.cancel(e)
    except:pass
    statusSV.set('Off')
    statusLabel2.configure(fg='red')
stopBtn = tk.Button(ssFrame, text='Stop', command=stop,relief='groove')
stopBtn.grid(row=2,column=0,pady=paddY)
################Save
def save():
    with open(whichFile,'w') as outputFile:
        for t in timeSlotEFs:
            outputFile.write(t.get()+'\n')
    popper('Successfully saved.','l')
saveBtn = tk.Button(ssFrame, text='Save', command=save,relief='groove')
saveBtn.grid(row=3,column=0,pady=paddY)

########Status
statusLabel1 = tk.Label(ssFrame,text='Status',font=(fontt))
statusLabel1.grid(row=4,column=0,pady=(81,paddY))
statusLabel2 = tk.Label(ssFrame,textvariable=statusSV,font=('Courier 18 bold'),fg='red')
statusLabel2.grid(row=5,column=0,pady=paddY)
statusSV.set('Off')
sigLabel=tk.Label(ssFrame,text='eutoApps',font=('Courier 7'))
sigLabel.grid(row=6,column=0,pady=(21,0),sticky='e')

#These are lists purely for the look (color, font, etc) of the program
allWidgets=[programTitleLabel,bsFrame,tsFrame,ssFrame,bsLabel,#0 to 4
                  defaultBtn,chapelBtn,extra1Btn,audioLabel,bellBtn,#5 to 9
                  ringBtn,whichProgramLabel,ssLabel,startBtn,stopBtn,#10 to 14
                  saveBtn,statusLabel1,statusLabel2,extra2Btn,extra3Btn,#15 to 19
                    mW]#20
btnsList,labelsList=[5,6,7,9,10,13,14,15,18,19],[4,8,11,12,16]
for w in allWidgets:
    w.configure(bg='white')
#allWidgets[0].configure(bg='light gray',fg='blue')
for i in btnsList:allWidgets[i].configure(font=('Courier 10 bold'),bg='white')
for i in btnsList:allWidgets[i].grid(sticky='ew')#to make all buttons same width
for i in labelsList:allWidgets[i].configure(bg='light blue',width=8)
for i in [4,8,12,16]:allWidgets[i].grid(sticky='ew')
bsFrame.configure(bg='light gray')
tsFrame.configure(bg='gray')
ssFrame.configure(bg='light gray')

########Make sure user to Stop thread before Exiting (if user forgets)
def on_closing():
    try:#this for any weird things that prevent successful close
        #such as if the bell file is currently sounding for the first time
        #and therefore status is "On" but queue is still empty
        if statusSV.get()=='On':
            s.cancel(e)
        mW.destroy()
    except:return
mW.protocol("WM_DELETE_WINDOW", on_closing)
########LAUNCH PROGRAM
mW.mainloop()
