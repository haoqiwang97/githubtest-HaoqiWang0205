#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 20:40:12 2019

@author: haoqiwang
"""

#brownian, 8 receptors, ligands-ligands interactions, delta t absorbed
#%matplotlib qt5
import numpy as np
import math
from matplotlib import pyplot as plt
from matplotlib import animation

n1 = 100  #the amount of the ligands
radius_l=5 #radius of ligands

n2 = 8 #the amount of receptors

radius_r=20 #radius of receptor
L = 1000  #the length and width of the box
D = 1 #difussion constant
dt = 0.1 #time step
dt2 = dt*dt
time = 0.0
#istep = 0
timelist = [] #a list to store time

lcharge=1 #charge of ligands
rcharge=-2 #charge of receptor
#tt = 0


alpha=0.1#drag force
epsilon = 1.0#permittivity
xi = 1.0#Debye-Huckel for charge interactions

epsilon1=1.0

r2cut = (epsilon1*2)**2  #maximum distance with which particles 
                        #could sense the interaction

vcut = L/100/dt  #maximum speed

#initialize the location and the speed
global vx, vy, fx, fy
'''
rx = np.random.random(n1)*L*0.01+495
ry = np.random.random(n1)*L*0.01+495
#rx = np.random.random(n1)*L/10
#ry = np.random.random(n1)*L/10

#vx = (np.random.random(n1)-0.5)*vcut*2
#vy = (np.random.random(n1)-0.5)*vcut*2
vx = np.zeros(n1)
vy = np.zeros(n1)
'''
rx = np.random.random(n1)*L
ry = np.random.random(n1)*L 
vx = (np.random.random(n1)-0.5)*vcut*2
vy = (np.random.random(n1)-0.5)*vcut*2
#give position of receptors
#rx_r=np.zeros(n2)+50
#ry_r=np.zeros(n2)+50

#rx_r=[500,100,500,900,217,217,783,783]
#ry_r=[100,500,900,500,217,783,783,217]

rx_r=np.random.random(n2)*L
ry_r=np.random.random(n2)*L

counter=np.zeros(n2)
#absorbed=np.zeros(n2)
absorbed=[]
absorbedlist=[]
#test = np.zeros((n2, 1), dtype=np.int)

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
            
            dr6 = dr2*dr2*dr2
            dr12 = dr6*dr6
            
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
            
            #Lenord Jones potential
            f4 = (12.0*epsilon1**12/dr12 - 6.0*epsilon1**6/dr6)/dr2
            fx4 = f4*dx
            fy4 = f4*dy
            
            fx[i] += fx1+fx2+fx4  #the values of interaction force 
            fx[j] -= fx1+fx2+fx4 #are the same with opposite direction
            fy[i] += fy1+fy2+fy4  #between two particles
            fy[j] -= fy1+fy2+fy4
            
            #fx[i] += fx1  #the values of interaction force 
            #fx[j] -= fx1  #are the same with opposite direction
            #fy[i] += fy1  #between two particles
            #fy[j] -= fy1
            
    for i in range(n1):
        for k in range(n2):
            dx_r = rx[i] - rx_r[k]
            dy_r = ry[i] - ry_r[k]
            dr2_r = dx_r*dx_r + dy_r*dy_r
            dr_r=dr2_r**0.5
            if(dr_r<radius_l+radius_r):
                continue
            #f3 is ligand-receptor interaction
            
            f3=(1/(4*math.pi*epsilon))*((lcharge*rcharge)/dr_r)*math.exp(-dr_r/xi)
            sin_r=dy_r/dr_r
            cos_r=dx_r/dr_r
            fx3=f3*cos_r
            fy3=f3*sin_r
            fx[i] += fx3
            fy[i] += fy3
        '''
        for k in range(n2):
            dx_r = rx[i] - rx_r[k]
            dy_r = ry[i] - ry_r[k]
            dr2_r = dx_r*dx_r + dy_r*dy_r
            if dr2_r<=radius_r*radius_r:
                print ('absorbed')
            else:
                continue
            '''
    return
 
#count=0
def MDrun():
    global rx, ry, vx, vy, fx, fy, dt, time, vcut, count,absorbed,r2cut#, dr2_r
    #, istep
    #, T0, T, 
    
    force()
    
    vx += dt*fx
    vy += dt*fy
    
    #the speed can`t exceed the vcut
    for i in range(n1):
        if(abs(vx[i])>vcut):
            vx[i] = abs(vx[i])/vx[i]*vcut
        if(abs(vy[i])>vcut):
            vy[i] = abs(vy[i])/vy[i]*vcut
    
    #record the step to judge if ligand is absorbed in dt
    rx_old=rx
    ry_old=ry
    
    rx += vx*dt
    ry += vy*dt
    ''
    for i in range(n1):
        if(rx[i]<0 or rx[i]>L):
            vx[i] = -vx[i]
        if(ry[i]<0 or ry[i]>L):
            vy[i] = -vy[i]
    ''
    ''
    #judge distance between ligands and receptors
    #count=0
    #dr2_r=[]
    #ii=0
    for i in range(n1):
        for k in range(n2):
            dx_r = rx[i] - rx_r[k]
            dy_r = ry[i] - ry_r[k]
            dr2_r = dx_r*dx_r + dy_r*dy_r
            dr_r=dr2_r**0.5
            
            #judge absorbtion
            if dr_r-radius_l-radius_r<=radius_r:
                rx[i]=rx_r[k]
                ry[i]=ry_r[k]
                absorbed.append(i)
                absorbed=list(set(absorbed))
                #unabsorbed=remove....
            else:
                dx_r_old = rx_old[i] - rx_r[k]
                dy_r_old = ry_old[i] - ry_r[k]
                dr2_r_old = dx_r_old*dx_r_old + dy_r_old*dy_r_old
                dr_r_old=dr2_r_old**0.5
                u=np.random.random()
                d1=dr_r-radius_r-radius_l
                d2=dr_r_old-radius_r-radius_l
                q=math.exp((-d1*d2)/(D*dt))
                if q>u:
                    rx[i]=rx_r[k]
                    ry[i]=ry_r[k]
                    absorbed.append(i)
                    absorbed=list(set(absorbed))
                else:
                    continue
    '' 
    #istep += 1
    time += dt
    timelist.append(time)
    absorbedlist.append(len(list(set(absorbed))))
    return

#for istep in range(100):
    #MDrun()
''
#animate the process
def animate(frame):#the frame number i
    #global tt
    MDrun()
    line1.set_data(rx, ry)
    line2.set_data(timelist, absorbedlist)
    #line2.set_data(TIME, TEMPERATURE)
    #ax2.set_xlim(-3+tt, 3+tt)
    #tt += 0.1
    #text=len(absorbed)
    #plt.text(4, 1, text)
    return line1, line2
#, line2

fig = plt.figure(figsize = (11, 5))
#set the parameters of the ax1
ax1 = fig.add_subplot(1, 2, 1, xlim = (0, int(L)), ylim = (0, int(L)))
ax1.set_title('Brownian Motion with Receptors')
ax1.set_xlabel('Length')
ax1.set_ylabel('Width')

#plt.text('tt')
#text=len(absorbed)
#plt.text(4, 1, text)

circle1 = plt.Circle((rx_r[0], ry_r[0]), radius_r, color='blue')
circle2 = plt.Circle((rx_r[1], ry_r[1]), radius_r, color='blue')
circle3 = plt.Circle((rx_r[2], ry_r[2]), radius_r, color='blue')
circle4 = plt.Circle((rx_r[3], ry_r[3]), radius_r, color='blue')
circle5 = plt.Circle((rx_r[4], ry_r[4]), radius_r, color='blue')
circle6 = plt.Circle((rx_r[5], ry_r[5]), radius_r, color='blue')
circle7 = plt.Circle((rx_r[6], ry_r[6]), radius_r, color='blue')
circle8 = plt.Circle((rx_r[7], ry_r[7]), radius_r, color='blue')

ax1.add_artist(circle1)
ax1.add_artist(circle2)
ax1.add_artist(circle3)
ax1.add_artist(circle4)
ax1.add_artist(circle5)
ax1.add_artist(circle6)
ax1.add_artist(circle7)
ax1.add_artist(circle8)

ax2 = fig.add_subplot(1, 2, 2, xlim=(0,100),ylim = (0, 100))
ax2.set_title('Number of absorbed ligands')
ax2.set_xlabel('Time')
ax2.set_ylabel('Number of absorbed ligands')

line1,=ax1.plot(rx, ry, 'ro', markersize=radius_l)
line2,=ax2.plot(timelist, absorbedlist, '-')

anim1 = animation.FuncAnimation(fig, animate, frames=1000, interval=1)

#plt.rcParams['animation.ffmpeg_path'] = '\\usr\\local\\Cellar\\ffmpeg\\4.2.1_2\\'
#anim1.save('test_animation.mp4',writer='FFMpegWriter')
#anim1.save('test_animation.gif',writer='imagemagick')
''
FFwriter=animation.FFMpegWriter()
anim1.save('brow_8recep_line_ligandinter_jones_wall_randomre1.mp4',writer=FFwriter)
''
plt.show()
''
