#!/usr/bin/python

# Plotting I-V curves

import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path += '.'
from x_inf import *
from input_vars import * # Global variables from input data file.

# Simulation Parameters
deltat = 0.01e-3
duration = 0.03                 #*********************      Duration    Duration   ***************
numpoints = int(round(duration/deltat))
numtests = 160
#xaxis = (deltat:deltat:duration) * 1e3
xaxis = [round(x * 1e3, 2) for x in np.arange(deltat, duration+deltat, deltat)]
V_mV = 1e3

# Input parameters
onset = int(round(0.002/deltat))
offset = int(round(0.022/deltat))

# Variable Declaration
V = list()
I_j = list()
I_mem = list()
I_Ca = list()
V_Ca = list()
I_KS = list()
V_KS = list()
I_KF = list()
V_KF = list()
I_K = list()
V_K = list()
Ca = list()
n = list()
p = list()
q = list()
e = list()
f = list()
h = list()

for i in range(0,numtests):
    V.append(list())
    I_mem.append(list())
    Ca.append(list())
    n.append(0)
    p.append(0)
    q.append(0)
    e.append(0)
    f.append(0)
    h.append(0)
    I_j.append(0)
    I_Ca.append(0)
    V_Ca.append(0)
    I_K.append(0)
    V_K.append(0)
    I_KS.append(0)
    V_KS.append(0)
    I_KF.append(0)
    V_KF.append(0)
    for j in range(0,numpoints):
        V[i].append(0)
        I_mem[i].append(0)
        Ca[i].append(0)
I_j.append(0)

# Input initialization
for i in range(0,numtests):
    for j in range(0,numpoints):
        V[i][j] = -70e-3

Vstim = 80e-3
for i in range(0,numtests):
    for j in range(onset-1,offset):
        V[i][j] = Vstim
    Vstim = Vstim - 1e-3

# Variable initialization
for j in range(0,numtests):
    Ca[j][0] = 0
    n[j] = x_inf(V[j][0], Vhalf_n, k_n)
    p[j] = x_inf(V[j][0], Vhalf_p, k_p)
    q[j] = x_inf(V[j][0], Vhalf_q, k_q)
    e[j] = x_inf(V[j][0], Vhalf_e, k_e)
    f[j] = x_inf(V[j][0], Vhalf_f, k_f)

# Start of simulation
for j in range(0,numtests):
    for i in range(1,numpoints):
        dn = (x_inf(V[j][i-1], Vhalf_n, k_n) - n[j])/T_n
        n[j] = n[j] + dn*deltat
        dp = (x_inf(V[j][i-1], Vhalf_p, k_p) - p[j])/T_p
        p[j] = p[j] + dp*deltat
        dq = (x_inf(V[j][i-1], Vhalf_q, k_q) - q[j])/T_q
        q[j] = q[j] + dq*deltat
        de = (x_inf(V[j][i-1], Vhalf_e, k_e) - e[j])/T_e
        e[j] = e[j] + de*deltat
        df = (x_inf(V[j][i-1], Vhalf_f, k_f) - f[j])/T_f
        f[j] = f[j] + df*deltat
        h[j] = x_inf(Ca[j][i-1], Cahalf_h, k_h)

        IKS = gKS * n[j] * (V[j][i-1] - VKS)
        IKF = gKF * p[j]**4 * q[j] * (V[j][i-1] - VKF)
        ICa = gCa * e[j]**2 * f[j] * (1 + (h[j] - 1) * alphaCa) * (V[j][i-1] - VCa)
        IL = gL * (V[j][i-1] - VL)

        dCa = -(Ca[j][i-1]/T_Ca + thiCa*ICa)
        Ca[j][i] = Ca[j][i-1] + dCa*deltat

        if (onset < i < offset):
            if abs(ICa / Cmem) > abs(I_Ca[j]):
                I_Ca[j] = ICa / Cmem
                V_Ca[j] = V[j][i] * V_mV
            if abs(IKS / Cmem) > abs(I_KS[j]):
                I_KS[j] = IKS / Cmem
                V_KS[j] = V[j][i] * V_mV
            if abs(IKF / Cmem) > abs(I_KF[j]):
                I_KF[j] = IKF / Cmem
                V_KF[j] = V[j][i] * V_mV
            if abs(((IKS + IKF) / Cmem)) > abs(I_K[j]):
                I_K[j] = (IKS + IKF) / Cmem
                V_K[j] = V[j][i] * V_mV


plt.figure(1)
plt.plot(V_Ca, I_Ca, 'r', label='$I_{Ca}$')
plt.xlim(-40,80)
plt.ylim(-8,6)
plt.ylabel('I_Ca (A/F)')
plt.xlabel('V (mV)')

plt.figure(2)
plt.plot(V_KS, I_KS, 'y', label='$I_{Kf}$')
plt.xlim(-70,50)
plt.ylim(-5,40)
plt.ylabel('I_Ks (A/F)')
plt.xlabel('V (mV)')

plt.figure(3)
plt.plot(V_KS, I_KF, 'c', label='$I_{Ks}$')
plt.xlim(-70,50)
plt.ylim(-5,40)
plt.ylabel('I_Kf (A/F)')
plt.xlabel('V (mV)')

plt.figure(4)
plt.plot(V_K, I_K, 'k', label='$I_{K}$')
plt.xlim(-70,50)
plt.ylim(-5,40)
plt.ylabel('I_K (A/F)')
plt.xlabel('V (mV)')

plt.show()
