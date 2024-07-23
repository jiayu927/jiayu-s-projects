# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 12:08:44 2024

@author: Jiayu
"""

import os, csv, time, random, pyglet
import numpy as np
from psychopy import gui, core, visual, event
os.chdir('C:\\Users\\blibl\Desktop\\Serial_recall\\verbal_task')
trial_clock = core.Clock()
#===================== Participant DATA Dialog  ============================

part_data = {'part_num' : 4,
            'age'       : 5,
            'gender'    : ['m', 'f', 'd'],
            }

dlg = gui.DlgFromDict(part_data, title='Visual-verbal', order = ['part_num', 'age', 'gender'])
if dlg.OK:
    thisInfo = dlg.data
    #part_data['part_num'], part_data['age'], part_data['gender'] = dlg.data
else: 
    print ('user cancelled')
    core.quit()

#============ Open log file to write ===========
all_paths = {'dir_outputdata'  : os.path.join(os.getcwd(), 'OutputFile_verbal')}
all_paths['logfile'] = os.path.join(all_paths['dir_outputdata'], str(part_data['part_num']) + '_avsr_' + time.strftime("%Y%m%d_%H%M%S") + '.csv')
log_file = open(all_paths['logfile'], 'a') 
log_file.write("participant_num; age; gender; corr_resp; response; accuracy\n") 
#log_file.close()
#============= setup monitor ===========
win = visual.Window([1920,1080], fullscr = False, monitor="testMonitor", units="deg", color = 'white')
#============ Mouse ===========
myMouse = event.Mouse(visible = True, win = win)

poslist = [(0, 0), (-7, 0), (7, 0), (0, 7), (-7, 7), (7, 7), (-7, -7), (7, -7), (0, -7)]
cue_outward = visual.Rect(win = win, width = 12, height= 12, lineColor = 'black')
cue_middle = visual.Rect(win = win, width = 8, height= 8, lineColor = 'black')
cue_inward = visual.Rect(win = win, width = 4, height= 4, lineColor = 'black')

rect_1 = visual.Rect(win = win, width = 4, height= 4, lineColor = 'black', pos=(0,0))
rect_2 = visual.Rect(win = win, width = 4, height= 4, lineColor = 'black', pos=(-7,0))
rect_3 = visual.Rect(win = win, width = 4, height= 4, lineColor = 'black', pos=(7,0))
rect_4 = visual.Rect(win = win, width = 4, height= 4, lineColor = 'black', pos=(0,7))
rect_5 = visual.Rect(win = win, width = 4, height= 4, lineColor = 'black', pos=(-7,7))
rect_6 = visual.Rect(win = win, width = 4, height= 4, lineColor = 'black', pos=(7,7))
rect_7 = visual.Rect(win = win, width = 4, height= 4, lineColor = 'black', pos=(-7,-7))
rect_8 = visual.Rect(win = win, width = 4, height= 4, lineColor = 'black', pos=(7,-7))
rect_9 = visual.Rect(win = win, width = 4, height= 4, lineColor = 'black', pos=(0,-7))

cueinterval = 1
imagelist = []
stimuli = []
stim_element = 0
singlenum = 1
corr_seq = []
imagesClicked = []
piclist = []
retention = 1
clickwait = 0.05
numbersClicked = []
responses = []
corr_element = 0 

df_visual = open("numbers.csv", "r")
li = df_visual.readlines()
df_visual.close()
random.shuffle(li)
df_visual = open("numbers_visual_sf.csv", "w")
df_visual.writelines(li)
df_visual.close()
df_visual = open("numbers_visual_sf.csv", "r")
reader_visual = csv.reader(df_visual, delimiter=";")
for row in reader_visual:
    triallength = len(row)
    for i in row:
        imagelist.append(i)
cue_outward.draw()
win.flip()
core.wait(cueinterval)
cue_outward.draw()
cue_middle.draw()
win.flip()
core.wait(cueinterval)
cue_outward.draw()
cue_middle.draw()
cue_inward.draw()
win.flip()
core.wait(cueinterval)
pics = 0
for i in imagelist:
    current = imagelist.pop(0) 
    stimuli.append(current)
    pics += 1
    if pics >= triallength:
        break

num_sequence = list(stimuli)
positions = []
for i in poslist:
    positions.append(i)

for i in stimuli:
    stimulus = i
    corr_seq.append(stimulus)
    pic = visual.ImageStim(win, image=stimuli[stim_element])
    pic.draw(), rect_1.draw()
    win.flip()
    stim_element += 1
    core.wait(singlenum)
win.flip()
core.wait(retention)
random.shuffle(positions)
sequence_temp = list(num_sequence)
stim_element = 0
positions_element = 0
responses = []
for i in stimuli:
    pic = visual.ImageStim(win, image=stimuli[stim_element])
    pos_string = positions[positions_element]
    location = pos_string
    pic.pos = location
    piclist.append(pic)
    stim_element += 1
    positions_element += 1
for i in range(triallength):

    trial_response = None
    myMouse.clickReset()
    event.clearEvents()
    trial_clock.reset()
    for idx in piclist:
        idx.draw()
    rect_1.draw()
    rect_2.draw()
    rect_3.draw()
    rect_4.draw()
    rect_5.draw()
    rect_6.draw()
    rect_7.draw()
    rect_8.draw()
    rect_9.draw()
    win.flip()
    buttons, times = myMouse.getPressed(getTime = True)
    while trial_response == None:
        buttons, times = myMouse.getPressed(getTime = True)
        a = myMouse.getPos()
        
        if buttons == [1, 0, 0]: #Mouse is clicked left
            rt = trial_clock.getTime() # Get reaction time
            for idx in sequence_temp:
                if myMouse.isPressedIn(piclist[sequence_temp.index(idx)], buttons=[0]) and idx not in numbersClicked:
                    trial_response = idx
                    numbersClicked.append(idx)
                    piclist.pop(sequence_temp.index(trial_response))
                    sequence_temp.remove(trial_response)
            if trial_response != None:
                break
            else:
                myMouse.clickReset()
                event.clearEvents()
                core.wait(clickwait)
                buttons, times = myMouse.getPressed(getTime = True)
    corresp = num_sequence[i]
    print(corresp)
    print(type(corresp))
    trial_clock.reset()
    responses.append(trial_response)
    print(responses)
    log_file.write('%i; %i; %s; %s; %s; %s\n' % 
                   (part_data['part_num'],
                    part_data['age'], 
                    part_data['gender'],
                    corresp, 
                    trial_response,
                    trial_response == corresp,
                    ))

win.flip()
log_file.close()
win.close()
core.quit()