import matplotlib.pyplot as plt

from integral import *
from scipy.io import wavfile
import os


dir = "media/1"
samplerate = 0
data =[]


for i in os.listdir(dir):

    if i[-4:] == ".wav":
        file = wavfile.read(os.path.join(dir, i))
        data.append([i, file])
piks = []
'''
for exp in data:
    name, sound = exp
    samplerate = sound[0]
    sound_data=sound[1]
    mf, ma, s, c = fourie_torch(torch.tensor(sound_data[:,0].astype("float64")), 1/samplerate, max_f=20000, minf=2000, df = 10)
    #plt.close()
    #plt.style.use('seaborn-v0_8-paper')
    #plt.figure(figsize=(32, 18))
    #plt.plot(mf, ma)
    #plt.savefig(os.path.join(dir, name + ".png"), dpi=300)
    plt.close()
    middle = ma.sum()/len(ma)
    piks.append([])
    for i in range(len(ma)):
        if(ma[i] > 10*middle and mf[i] > 4000):
            piks[-1].append([i, float(mf[i]), float(ma[i])])
            print(float(mf[i]))

'''


file = wavfile.read(os.path.join(dir, "full.wav"))
sr, data = file
data = data[:,0]
data = torch.tensor(data.astype("float64"))
dt = 0.25
T = 0
f = 5800
Y = []
X = []
i = 0
while T < data.shape[0]/sr -dt:
    i_st = int(T*sr)
    i_end = int((T+1)*sr)
    mf, ma, s, c = fourie_torch(torch.slice_copy(data, 0, i_st, i_end), 1 / sr, max_f=20000,minf=2000, df=10)
    plt.close()
    prev = 0
    print(T)
    middle = ma.sum() / ma.shape[0]
    plt.figure(figsize=(32, 18))
    for j in range(mf.shape[0] - 1):

        if (ma[j] > ma[j + 1] and ma[j] > middle*11.45):

            #print(mf[j])
            prev = j
            plt.annotate(
                f"{float(mf[j])}",  # Текст подписи
                xy=(mf[j], ma[j]),  # Координаты, на которые указывает стрелка
                xytext=(mf[j] + 10, ma[j] + 0.001),  # Координаты, где будет сидеть сам текст
                arrowprops=dict(
                    facecolor="black", shrink=0.05, width=1, headwidth=6
                ),  # Настройки стрелки
                fontsize=10,
                color="blue",
            )

    Y.append(ma[84])
    X.append(T)
    plt.plot(mf, ma)
    plt.ylim(0, max(ma)+0.001)
    plt.xlabel('Частота')
    plt.ylabel('Амплитуда')
    plt.savefig(os.path.join(dir, "gr", f"{round(T*1000)}_{round((T+dt)*1000)}" + ".png"), dpi=300)
    plt.close()

    T+= dt
    i += 1



plt.plot(X, Y)
plt.show()




