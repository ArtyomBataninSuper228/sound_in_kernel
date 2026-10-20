import torch
import cv2 as cv
import time
import numpy as np
from matplotlib import pyplot as plt
from threading import Thread
import torch.nn.functional as F

def div(m):
    n = len(m.shape)
    res = torch.zeros(m.shape, dtype = m.dtype, device = m.device)
    shifts = []
    for i in range(n):
        shifts.append(0)
    axis = list(range(n))
    for i in range(n):
        shifts[i] = 1
        res += torch.roll(m, shifts=shifts, dims= axis)
        shifts[i] = -1
        res += torch.roll(m, shifts, axis)
        shifts[i] = 0
    res -= 2*n*m
    return res


class Simulation:


    def __init__(self, shape, device = None, default = None, masses = None, dtype = torch.float32, dt = 10**(-5), k = 1, c = 343, toe = None, f= None):
        self.dtype = dtype
        if device is None:
            device = torch.device("mps" if torch.mps.is_available() else "cpu")
        if default is None:
            default = torch.zeros(shape, dtype = dtype, device = device)
        if masses is None:
            masses = torch.ones(shape, dtype = dtype, device = device)
        self.field = default
        self.masses = masses
        self.device = device
        self.shape = shape
        self.toe = None
        self.F = torch.zeros(shape, dtype = dtype, device = device)
        self.V = torch.zeros(shape, dtype = dtype, device = device)
        self.dt = dt
        self.k = k
        self.c = c
        self.lmbda = c*(2**0.5*dt)/k
        self.f = f
        self.to_show = torch.zeros(shape, dtype=self.dtype, device="cpu")
        if(self.lmbda > 1):
            raise "dt is too large"
        if (shape != default.shape):
            print(f"{shape}, default: {default.shape}")
            raise("shape is inconsistent with default" + f"{shape}, default: {default.shape}")
        self.T = 0
    def set_max_dt(self):
        self.dt = self.k/(2**0.5*self.c)
        self.lmbda = 1
    def do_step(self):
        self.F = div(self.field)
        self.F.div_(self.masses)

        self.V += self.F*self.lmbda
        self.field += self.V*self.lmbda/2
        self.T += self.dt
    def update(self):
        while 1:
            self.do_step()
            if self.f != None:
                self.f()
            if self.toe != None and self.T >= self.toe:
                break


if __name__ == "__main__":
    c = 343
    dt = 10 ** -4
    shape = (1000, 1000)
    sim = Simulation(shape, c=c, dt=dt)#, device = torch.device("cpu"))
    sim.field[500][500] = 10
    for i in range(100):
        for j in range(100):
            if((i-50)**2 + (j-50)**2) <= 50**2:
                sim.field[i+450][j+450] = 10
    to_show = torch.zeros(shape, dtype=sim.dtype)
    i = 0
    #sim.set_max_dt()
    sim.toe = (500 - 50) / 343

    '''
    sim.update()
    x = []
    y = []
    for i in range(500, 1000):
        x.append(float(sim.field[i][500]))
        y.append(i)
    plt.plot(y, x)
    plt.show()


    '''
    t = Thread(target=sim.update)
    t.start()




    while 1:
        # sim.do_step()
        to_show.copy_(sim.field)
        mn = to_show.min()
        mx = to_show.max()
        show = ((to_show.cpu().numpy() - float(mn)) * float(255 / (mx - mn))).astype("uint8")
        # show *= int((255/(show.max()-show.min())))
        cv.imshow("field", cv.resize(show, (2000, 2000), cv.INTER_LINEAR))
        cv.waitKey(1)
        time.sleep(0.01)
        # print(sim.T, float(sim.field[50][50] - sim.field[0][0]), show.max() - show.min())







