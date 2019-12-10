#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 20:39:44 2019

@author: haoqiwang
"""

#%matplotlib qt5
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

NP = 100  #the amount of the particles
L = 100  #the length and width of the box

dt = 0.1 #time step
dt2 = dt**2
time = 0.0
#istep = 0
timelist = [] #a list to store time
escaped=[]
escapedlist=[]
#tt = 0

vcut = L/50/dt  #maximum speed

#initialize the location and the speed
global vx, vy, fx, fy
rx = np.random.random(NP)*L*0.1+45
ry = np.random.random(NP)*L*0.1+45
#vx = (np.random.random(NP)-0.5)*vcut*2
#vy = (np.random.random(NP)-0.5)*vcut*2
vx = np.zeros(NP)
vy = np.zeros(NP)

def force():
    global rx, ry, vx, vy, fx, fy, escaped
    #, T, r2cut, xi
    #fx = np.zeros(NP)
    #fy = np.zeros(NP)
    fx=(np.random.random(NP)-0.5)
    fy=(np.random.random(NP)-0.5)
    return
    
    
def MDrun():
    global rx, ry, vx, vy, fx, fy, dt, time, escaped, escapedlist
    #, istep
    #vcut, T0, T, 
    force()
    vx += dt*fx
    vy += dt*fy
    
    rx += vx*dt
    ry += vy*dt
    
    for i in range(NP):
        if rx[i]>L or rx[i]<0 or ry[i]>L or ry[i]<0:
            rx[i]=L*100
            ry[i]=L*100
            escaped.append(i)
            escaped=list(set(escaped))
    escapedlist.append(len(list(set(escaped))))
    
    #istep += 1
    time += dt
    timelist.append(time)
    return

#animate the process
def animate(frame):#the frame number i
    #global tt
    MDrun()
    line1.set_data(rx, ry)
    line2.set_data(timelist, escapedlist)
    #line2.set_data(TIME, TEMPERATURE)
    #ax2.set_xlim(-3+tt, 3+tt)
    #tt += 0.1
    return line1,line2
#, line2

fig = plt.figure(figsize = (11, 5))
#set the parameters of the ax1
ax1 = fig.add_subplot(1, 2, 1, xlim = (0, int(L)), ylim = (0, int(L)))
ax1.set_title('Brownian Motion')
ax1.set_xlabel('Length')
ax1.set_ylabel('Width')

ax2 = fig.add_subplot(1, 2, 2, xlim=(0,100),ylim = (0, 100))
ax2.set_title('Number of escaped ligands')
ax2.set_xlabel('Time')
ax2.set_ylabel('Number of escaped ligands')

line1,=ax1.plot(rx, ry, 'ro')
line2,=ax2.plot(timelist, escapedlist, '-')

anim1 = animation.FuncAnimation(fig, animate, frames=1000, interval=1)

FFwriter=animation.FFMpegWriter()
anim1.save('brownian_line.mp4',writer=FFwriter)

plt.show()
'''
fig = plt.figure(figsize = (5, 5))
#set the parameters of the ax1
ax1 = fig.add_subplot(1, 1, 1, xlim = (0, int(L)), ylim = (0, int(L)))
ax1.set_title('Brownian Motion')
ax1.set_xlabel('Length')
ax1.set_ylabel('Width')

line1,=ax1.plot(rx, ry, 'ro')

anim1 = animation.FuncAnimation(fig, animate, frames=1000, interval=1)

#plt.rcParams['animation.ffmpeg_path'] = '\\usr\\local\\Cellar\\ffmpeg\\4.2.1_2\\'
#anim1.save('test_animation.mp4',writer='imagemagick')
#anim1.save('test_animation.mp4',writer='FFMpegWriter')
#anim1.save('test_animation.mp4')
''
#FFwriter=animation.FFMpegWriter()
#anim1.save('brownian.mp4',writer=FFwriter)
''
plt.show()
'''