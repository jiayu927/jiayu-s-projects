# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 11:58:36 2024

@author: Jiayu
"""

import os, csv, time, random, pyglet
import numpy as np
from psychopy import gui, core, visual, event
os.chdir('C:\\Users\\blibl\Desktop\\Serial_recall\\spatial_task')
#===================== Participant DATA Dialog  ============================

part_data = {'part_num' : 4,
            'age'       : 5,
            'gender'    : ['m', 'f', 'd'],
            }

dlg = gui.DlgFromDict(part_data, title='Visual-spatial', order = ['part_num', 'age', 'gender'])
if dlg.OK:
    thisInfo = dlg.data
    #part_data['part_num'], part_data['age'], part_data['gender'] = dlg.data
else: 
    print ('user cancelled')
    core.quit()

#============ Open log file to write ===========
all_paths = {'dir_outputdata'  : os.path.join(os.getcwd(), 'OutputFile_spatial')}
all_paths['logfile'] = os.path.join(all_paths['dir_outputdata'], str(part_data['part_num']) + '_avsr_' + time.strftime("%Y%m%d_%H%M%S") + '.csv')
log_file = open(all_paths['logfile'], 'a') 
log_file.write("participant_num; age; gender; corr_resp; response; accuracy\n") # Heading

#============= setup monitor ===========
win = visual.Window([1920,1080], fullscr = False, monitor="testMonitor", units="deg", color = 'white')
#============ Mouse ===========
myMouse = event.Mouse(visible = True, win = win)
trial_clock = core.Clock()

grid_positions = [(0, 0), (-7, 0), (7, 0), (0, 7), (-7, 7), (7, 7), (-7, -7), (7, -7), (0, -7)]
cue_outward = visual.Rect(win = win, width = 12, height= 12, lineColor = 'black')
cue_middle = visual.Rect(win = win, width = 8, height= 8, lineColor = 'black')
cue_inward = visual.Rect(win = win, width = 4, height= 4, lineColor = 'black')

sequence_length = 9
sequence = random.sample(grid_positions, sequence_length)
sequence_temp1 = list(sequence)
piclist = []
cueinterval = 1
imagelist = []
stimuli = []
stim_element = 0
singlenum = 1
corr_seq = []
imagesClicked = []
retention = 1
clickwait = 0.05
numbersClicked1 = []
responses = []
corr_element = 0 
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
for pos in sequence:
    stimulus = visual.Circle(win, radius=1, fillColor='black', lineColor='black', pos=pos)
    stimulus.draw()
    win.flip()
    core.wait(1)  
    win.flip()
    core.wait(0.5) 
    piclist.append(stimulus)

for i in range(sequence_length):
    trial_response1 = None
    myMouse.clickReset()
    event.clearEvents()
    trial_clock.reset()
    for idx in piclist:
        idx.draw()
    win.flip()
    #buttons, times = myMouse.getPressed(getTime = True)
    while trial_response1 == None:
        buttons, times = myMouse.getPressed(getTime = True)
        a = myMouse.getPos()
        if buttons == [1, 0, 0]:
            for idx in sequence_temp1:
                if myMouse.isPressedIn(piclist[sequence_temp1.index(idx)], buttons=[0]) and idx not in numbersClicked1:
                    trial_response1 = idx
                    numbersClicked1.append(idx)
                    piclist.pop(sequence_temp1.index(trial_response1))
                    sequence_temp1.remove(trial_response1)

            if trial_response1 != None:
                break
            else:
                myMouse.clickReset()
                event.clearEvents()
                core.wait(clickwait)  
                buttons, times = myMouse.getPressed(getTime = True)
    corresp = sequence[i] 
    print(corresp)
    trial_clock.reset()
    responses.append(trial_response1)
    print(responses)
    log_file.write('%i; %i; %s; %s; %s; %s\n' % 
                   (part_data['part_num'],
                    part_data['age'], 
                    part_data['gender'],
                    corresp, 
                    trial_response1,
                    trial_response1 == corresp,
                    ))

win.flip()
log_file.close()
win.close()
core.quit()