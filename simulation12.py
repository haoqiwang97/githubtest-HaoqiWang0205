#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 20:38:43 2019

@author: haoqiwang
"""

#brownian motion with Dybye, ligands released from center
#record number of the escaped ligands

#%matplotlib qt5
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import math

n1 = 100  #the amount of the particles
L = 100  #the length and width of the box

dt = 0.1 #time step
dt2 = dt**2
time = 0.0
#istep = 0
timelist = [] #a list to store time
escaped=[]
escapedlist=[]
#tt = 0

epsilon=1.0
lcharge=1
xi=1.0

radius_l=5

vcut = L/100/dt  #maximum speed

#initialize the location and the speed
global vx, vy, fx, fy
rx = np.random.random(n1)*L*0.1+45
ry = np.random.random(n1)*L*0.1+45
#vx = (np.random.random(NP)-0.5)*vcut*2
#vy = (np.random.random(NP)-0.5)*vcut*2
vx = np.zeros(n1)
vy = np.zeros(n1)

def force():
    global rx, ry, vx, vy, fx, fy, r2cut
    #T, r2cut, xi
    fx = np.zeros(n1)
    fy = np.zeros(n1)
    for i in range(n1-1):
        for j in range(i+1, n1):
            dx = rx[i] - rx[j]
            dy = ry[i] - ry[j]
            dr2 = dx*dx + dy*dy
            dr=dr2**0.5 
            
            #dr6 = dr2*dr2*dr2
            #dr12 = dr6*dr6
            
            #if(dr2>r2cut):
                #continue 
            
            if(dr<radius_l*2):
                continue
            #f1 is Brownian motion
            fx1=np.random.random()-0.5
            fy1=np.random.random()-0.5
            #f2 is ligand-ligand interaction
            f2=(1/(4*math.pi*epsilon))*((lcharge*lcharge)/dr)*math.exp(-dr/xi)
            sin=dy/dr
            cos=dx/dr
            fx2=f2*cos 
            fy2=f2*sin
            '''
            #Lenord Jones potential
            f4 = (12.0*epsilon1**12/dr12 - 6.0*epsilon1**6/dr6)/dr2
            fx4 = f4*dx
            fy4 = f4*dy
            '''
            fx[i] += fx1+fx2  #the values of interaction force 
            fx[j] -= fx1+fx2  #are the same with opposite direction
            fy[i] += fy1+fy2  #between two particles
            fy[j] -= fy1+fy2
    return

def MDrun():
    global rx, ry, vx, vy, fx, fy, dt, time, escaped, escapedlist
    #, istep
    #vcut, T0, T, 
    force()
    vx += dt*fx
    vy += dt*fy
    
    for i in range(n1):
        if(abs(vx[i])>vcut):
            vx[i] = abs(vx[i])/vx[i]*vcut
        if(abs(vy[i])>vcut):
            vy[i] = abs(vy[i])/vy[i]*vcut
    
    rx += vx*dt
    ry += vy*dt
    
    for i in range(n1):
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
ax1.set_title('Brownian Motion with Debye–Hückel')
ax1.set_xlabel('Length')
ax1.set_ylabel('Width')

ax2 = fig.add_subplot(1, 2, 2, xlim=(0,100),ylim = (0, 100))
ax2.set_title('Number of escaped ligands')
ax2.set_xlabel('Time')
ax2.set_ylabel('Number of escaped ligands')

line1,=ax1.plot(rx, ry, 'ro')
line2,=ax2.plot(timelist, escapedlist, '-')

anim1 = animation.FuncAnimation(fig, animate, frames=1000, interval=1)
''
FFwriter=animation.FFMpegWriter()
anim1.save('brownian_line_dybye.mp4',writer=FFwriter)
''
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