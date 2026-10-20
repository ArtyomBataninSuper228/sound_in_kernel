from integral import *


meandr = []
for i in range(10000):
    if i%40 < 20:
        meandr.append(1)
    else:
        meandr.append(0)
meandr = torch.tensor(meandr, dtype=torch.float64)
mf, ma, s, c = fourie_torch(meandr, 1 /48000 , max_f=20000,minf=100, df=10)
plt.plot(mf, ma)

plt.show()

