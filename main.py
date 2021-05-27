import numpy as np

taille = 10000
distance = np.linspace(0, 200, taille)
gear = np.zeros(taille)
torque = np.zeros(taille)
rpm = []
delta_d = distance[1]-distance[0]
v = 110/3.6

for i in distance:
    coeffs = [3.4, v, -delta_d]
    roots = np.roots(coeffs)
    t = roots[1]
    v = v + 6.8*t
    rpm.append(v*1000*3.6/(60*1.765*9/30*14/23))

print(v*3.6, rpm[-1])
