
import copy
import time
from math import *
import dearpygui.dearpygui as dpg
import math
import numpy
from matplotlib import pyplot as plt
import torch

e = math.e

m = []
mv = []
mt = []
mex = []
sp = 40
x = 0
a = 0
t = 0
dt = 0.001
K = 0.1



def tn(A, B):
    dx = A[0] - B[0]
    dy = A[1] - B[1]
    if dx == 0:
        return 0
    else:
        return dy/dx

def func(x):
    return mv[round(x/dt)]
def func2(x):
    return x%10<5#math.sin(math.pi*x/4) + math.sin(math.pi*x/10) +  math.sin(math.pi*x/3)*0.25
def create_grafic(massiv, data):
    nums = len(data)
    dpg.create_context()
    dpg.create_viewport(title='График', width=1500, height=900)
    dpg.show_imgui_demo()
    with dpg.window(pos = (0, 0), width=1500, height=890):
        with dpg.plot(width=1400, height=850):
            plot = dpg.last_item()
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis)
            xaxis = dpg.last_item()
            # dpg.set_axis_limits(xaxis, massiv[0], massiv[-1])
            dpg.add_plot_axis(dpg.mvYAxis)
            yaxis = dpg.last_item()
            dpg.set_axis_limits_auto(yaxis)
            for i in range(nums):
                #dpg.add_series
                dpg.add_line_series(massiv, data[i], parent=yaxis, label=str(i + 1))
            # dpg.add_line_series(massiv, volts, parent=yaxis, label="")
            # dpg.add_line_series(massiv, dv1, parent=yaxis, label="∆U1")
            # dpg.add_line_series(massiv, dv2, parent=yaxis, label="∆U2")
            # dpg.add_line_series(massiv, power, parent=yaxis, label="Power")

    dpg.create_viewport(title='Grafik', width=1440, height=850)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()

    dpg.destroy_context()
def integral(min, max, dx, f):
    x = min
    S = 0
    while x <= max:
        A = f(x)
        x += dx
        B = f(x)
        S += dx * (A+B)/2
    return S
def differenzial(f, dx, x=0):
    yf = f(x)
    ys = f(x + dx)
    t = tn([x, yf], [x +dx, ys])
    return t
def fourie(func, max, min, dx):
    num = (max-min)/dx
    min_f = 1/(2*num*dx)
    max_f = 1/(2*dx)
    f = min_f
    res = []
    while f <= max_f:
        freq = copy.deepcopy(f)
        def fns(x):
            #print(math.sin(math.pi*x*freq))
            return math.sin(math.pi*x*freq)*func(x)
        def fnc(x):
            #print(math.sin(math.pi*x*freq))
            return math.cos(math.pi*x*freq)*func(x)
        Asin = integral(min, max, dx, fns)
        Acos = integral(min, max, dx, fnc)
        A = (Asin**2 + Acos**2)**0.5
        sinfi = Asin/A
        cosfi = Asin / A
        res.append((f, A, sinfi, cosfi))

        f += 1/(2*num*dx)
    return res


def obrat_fourie(freq, ampls, min, max, dx):

    res = numpy.zeros(int((max-min)/dx + 1))
    massiv = []
    num = 0
    while min < max:
        massiv.append(min)
        for    i in range(len(freq)):
            if ampls[i] > 1:
                print(freq[i])
                res[num] += ampls[i]*math.sin(math.pi*freq[i]* min)
        min += dx
        num += 1
    return massiv, res


    #pass
#dat = [32, 10.5, 6.3, 4.5, 3.5, 2.7, 2.3, 2, 1.7, 1.5, 1.3, 1.14]
#massiv = [1/5, 0.6, 1, 1.4, 1.8, 2.2, 2.6, 3, 3.4, 3.8, 4.2, 4.6]
#massiv, res = obrat_fourie(massiv, dat, -1000, 1000, 1)
#create_grafic(massiv, [dat])

def sin(x):
    x=((x/(2*math.pi))%1)*2*math.pi
    ret = 0
    minus = False
    if x > math.pi:
        x -= math.pi
        minus = True
    for n in range(1, 80, 2):
        if minus:
            ret -= (x**n)/math.factorial(n)
            minus = False
        else:
            ret += (x ** n) / math.factorial(n)
            minus = True
    return ret
def s(t):
    t = ((t / (2 * math.pi)) % 1) * 2 * math.pi
    dt = 1 / 100
    x1 = 0
    sp = dt
    T = 0
    if t > math.pi:
        t -= math.pi
        sp = -dt

    while T < t:
        sp += -x1*(dt**2)
        x1 += sp
        T += dt
    return x1



def callback(sender, app_data):

    _helper_data = app_data[0]
    transformed_x = app_data[1]
    transformed_y = app_data[2]
    #transformed_y1 = app_data[3] # for channel = 3
    #transformed_y2 = app_data[4] # for channel = 4
    #transformed_y3 = app_data[5] # for channel = 5
    #mouse_x_plot_space = _helper_data["MouseX_PlotSpace"]   # not used in this example
    #mouse_y_plot_space = _helper_data["MouseY_PlotSpace"]   # not used in this example
    mouse_x_pixel_space = _helper_data["MouseX_PixelSpace"]
    mouse_y_pixel_space = _helper_data["MouseY_PixelSpace"]
    dpg.delete_item(sender, children_only=True, slot=2)
    dpg.push_container_stack(sender)
    dpg.configure_item("demo_custom_series", tooltip=False)
    for i in range(0, len(transformed_x)):
        #dpg.draw_text((transformed_x[i]+15, transformed_y[i]-15), str(i), size=20)
        dpg.draw_circle((transformed_x[i], transformed_y[i]), 2, fill=(50+i*5, 50+i*50, 0, 255))
        if mouse_x_pixel_space < transformed_x[i]+15 and mouse_x_pixel_space > transformed_x[i]-15 and mouse_y_pixel_space > transformed_y[i]-15 and mouse_y_pixel_space < transformed_y[i]+15:
            dpg.draw_circle((transformed_x[i], transformed_y[i]), 30)
            dpg.configure_item("demo_custom_series", tooltip=True)
            dpg.set_value("custom_series_text", "Current Point: " + str(i))
    dpg.pop_container_stack()
'''
with dpg.window(label="Tutorial") as win:
    dpg.add_text("Hover an item for a custom tooltip!")
    with dpg.plot(label="Custom Series", height=400, width=-1):
        dpg.add_plot_legend()
        xaxis = dpg.add_plot_axis(dpg.mvXAxis)
        with dpg.plot_axis(dpg.mvYAxis):
            with dpg.custom_series(x_data, y_data, 2, label="Custom Series", callback=callback, tag="demo_custom_series"):
                dpg.add_text("Current Point: ", tag="custom_series_text")
            dpg.fit_axis_data(dpg.top_container_stack())

dpg.set_primary_window(win, True)
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
'''

def get_distribution(m):
    a = list(set(m))
    l = len(m)
    a.sort()
    numbers = []
    for el in a:
        numbers.append(m.count(el)/l)
    return a, numbers
"""
massive = fourie(func2, 100, 0, 0.01)
m1 = []
m2 = []
for i in massive:
    m1.append(i[0])
    m2.append(i[1])
create_grafic(m1, [m2])
pyplot.plot(m1, m2)
pyplot.show()
"""

def do_runge_kutta_classic_step(sys, dif, step, h):
    sys2 = copy.copy(sys)
    k1 = dif(sys)
    sys2 = step(copy.copy(sys), h / 2, k1)
    k2 = dif(sys2)
    sys2 = step(copy.copy(sys), h / 2, k2)
    k3 = dif(sys2)
    sys2 = step(copy.copy(sys), h, k3)
    k4 = dif(sys2)
    k = (k1 + k2 * 2 + k3 * 2 + k4) / 6
    sys = step(sys, h, k)
    return sys


def do_my4_1_step(sys, dif, step, h):
    sys2 = copy.copy(sys)
    k1 = dif(sys)
    sys2 = step(sys2, h, k1)
    k2 = dif(sys2)
    sys2 = step(sys2, h, k2)
    k3 = dif(sys2)
    sys2 = step(sys2, h, k3)
    k4 = dif(sys2)
    k = (k1*15 + k2 * 7 + k3  + k4) / 24
    sys = step(sys, h, k)
    return sys

def do_my4_2_step(sys, dif, h):
    sys2 = copy.copy(sys)
    k1 = dif(sys2)
    sys2 = sys2 + h/2*k1#step(sys2, h / 2, k1)
    k2 = dif(sys2)
    sys2 = sys2 + h/2*k2#step(sys2, h / 2, k2)
    k3 = dif(sys2)
    sys2 = sys2 + h/2*k3#step(sys2, h/2, k3)
    k4 = dif(sys2)
    k = (k4 - k3  + k2 * 2 + k1) / 3
    return k

def do_my4_3_step(sys, dif, step, h):
    sys2 = copy.copy(sys)
    k1 = dif(sys2)
    sys2 = step(sys2, h / 3, k1)
    k2 = dif(sys2)
    sys2 = step(sys2, h / 3, k2)
    k3 = dif(sys2)
    sys2 = step(sys2, h/3, k3)
    k4 = dif(sys2)
    k = (27*k4 - 69*k3 + 69*k2 - 19*k1)/8
    sys = step(sys, h, k)
    return sys

def get_length(vector):# Возвращает длину n мерного вектора записаного в np.matrix
    if type(vector) != numpy.matrix:
        return vector
    elif vector.shape[0] == 1:
        sm = 0
        for i in range(vector.shape[1]):
            sm += get_length(vector[0, i])**2
        return sm**0.5

    else:
        sm = 0
        for i in range(len(vector)):
            sm += get_length(vector[i])**2
        return sm**0.5
def test_sys(sys, fd, fs, k, h):# функция ошибки при подборе значения f'(x+h) для решения уравнения f(x+h) = f(x) + hf'(x+h)
    sys2 = fs(copy.copy(sys), h, k)
    delta =  fd(sys2) - k
    return numpy.linalg.norm(delta)
def seek_solution_1d(sys, fd, fs, h):# функция подбирает значение f'(x+h) что бы минимизировать ошибку при решении уравнения f(x+h) = f(x) + hf'(x+h)
    st_sys = copy.copy(sys)
    k1 = fd(sys)
    sys = fs(sys, h, k1)
    k2 = fd(sys)
    delta = k2-k1
    t1 = test_sys(st_sys, fd, fs, k1, h)
    t2 = test_sys(st_sys, fd, fs, k2, h)
    a = t2-t1
    b = t1 - a
    n = -b/a - 1
    return k1 + delta*n
def seek_solution_nd(sys, fd, fs, h):#аналогична прошлой, просто для многомерных функций
    st_sys = copy.copy(sys)
    k1 = fd(sys)
    sys = fs(sys, h, k1)
    k2 = fd(sys)
    delta = k2-k1
    #t1 = test(st_sys, fd, fs, k1, h)
    #t2 = test(st_sys, fd, fs, k2, h)
    #a = t2-t1
    #b = t1 - a
    #n = -b/a - 1
    num = 5
    '''
    ks = []
    errors = []
    for i in range(num*2):
        errors.append(float(test(st_sys, fd, fs, k1 + delta/num*i, h)))
        ks.append(i)
    pyplot.plot(ks, errors)
    pyplot.show()
    '''
    t1 = test_sys(st_sys, fd, fs, k1, h)
    t2 = test_sys(st_sys, fd, fs, k1 + delta/num, h)
    a = t2 - t1
    b = t1 - a
    n = -b/a - 1
    #print(test(st_sys, fd, fs, k1 + delta*n/num, h), n)
    return k1 + delta*n/num

def do_backward_euler_step(sys, dif, step, h):
    sys2 = copy.copy(sys)
    k = seek_solution_nd(sys2, dif, step, h)
    sys = step(sys, h, k)
    return sys

def do_new_method_step(sys, dif, step, h): #pendulum full energy optimised
    sys1 = copy.copy(sys)
    sys2 = copy.copy(sys)
    sys2 = do_backward_2_step(sys2, dif, step, h)
    sys1 = step(sys1, h, dif(sys))
    sysr = (sys1*0.6531343815962066 + sys2*0.3468656184037933)
    return sysr

def do_backward_2_step(sys, dif, step, h):
    k1 = seek_solution_nd(copy.copy(sys), dif, step, h)
    sys2 = step(copy.copy(sys), h, k1)
    k2 = seek_solution_nd(sys2, dif, step, h)
    k = (k1+k2)/2
    sys = step(sys, h, k)
    return sys


def get_variance(sample):
    median = sum(sample)/len(sample)
    variance = 0
    for i in range(len(sample)):
        variance += ((sample[i] - median)**2)/len(sample)
    return variance


#signal, sampling_rate = soundfile.read("Artemii/2025-10-22 17.32.57.wav")
#maxt = len(signal)/sampling_rate - 1
#def f(t):
#    num = round(t*sampling_rate)
#    return signal[num]
#m = fourie(f, maxt/4, 0, 4/sampling_rate)
#f, datasin, datacos  = [], [], []

#for i in m:
#    f.append(i[0])
#    datasin.append(i[1]*i[2])
#    datacos.append(i[1]*i[3])
#pyplot.plot( f, datasin, datacos)
#pyplot.show()


def median(M):
    return sum(M)/len(M)

def dispersion(M):
    dispersion = 0
    med = median(M)
    for i in range(0, len(M)):
        dispersion += (M[i] - med)**2
    return dispersion/len(M)

def fourie_torch(data_tensor, dx, max_f = None, minf = 0, df = 1):
    data_tensor-= data_tensor.min()
    data_tensor/= data_tensor.max()
    data_tensor-= 0.5
    device = data_tensor.device
    dtype = data_tensor.dtype
    if max_f == None:
        max_f = 1/(2*dx)
    N = data_tensor.shape[0]

    NF = int((max_f-minf)/df)
    mf = torch.zeros(NF, dtype = dtype, device = device)
    mA = torch.zeros(NF, dtype = dtype, device = device)
    msin = torch.zeros(NF, dtype = dtype, device = device)
    mcos = torch.zeros(NF, dtype = dtype, device = device)
    base_tensor = torch.zeros(N, dtype=dtype, device = device)
    sintensor = torch.zeros(N, dtype=dtype, device = device)
    costensor = torch.zeros(N, dtype=dtype, device = device)
    outtensor = torch.zeros(N, dtype=dtype, device = device)
    for i in range(N):
        base_tensor[i] = 2*pi*i*dx

    for i in range(NF):
        #print(NF)
        F = df*(i)+minf
        torch.sin(base_tensor*F, out = sintensor)
        torch.cos(base_tensor*F, out = costensor)
        torch.mul(data_tensor, sintensor, out = outtensor)
        #plt.plot(sintensor.tolist())
        #plt.plot(outtensor.tolist())
        #plt.show()
        S = outtensor.sum()
        torch.mul(data_tensor, costensor, out = outtensor)
        C = outtensor.sum()
        A = (S**2+C**2)**0.5
        mf[i] = F
        mA[i] = A
        msin[i] = S
        mcos[i] = C
    return(mf, mA/N, msin/N, mcos/N)

def get_grad(f, pred, res, dx):
    probe = copy.copy(res)
    probe.fill(0)

    a = numpy.linalg.norm(f(pred))
    for i in range(0, len(pred)):
        probe[i] = dx
        a1 = numpy.linalg.norm(f(pred+probe))
        a2 = numpy.linalg.norm(f(pred-probe))
        df_di = (a1-a2)/(2*dx)
        res[i] = df_di
        probe[i] = 0
def get_sol(f, sys, pred, dx):
    func =  lambda p: p - f(sys+p)
    for i in range(2):
        grad = numpy.zeros(len(pred), dtype = numpy.float64)
        get_grad(func, pred, grad, dx)
        pred-=grad*(func(pred)/numpy.linalg.norm(grad)/2)
def new_backward_step(sys, f, dt):
    pred = f(sys)
    get_sol(f, sys, pred, dt)
    sys += pred*dt
    return sys


