import json

import cv2

from Simulation import *
import math
import torch.nn.functional as F
random_f = open("/dev/urandom", "rb")

def get_random_n(mn, mx):
    n = math.ceil(math.log(mx-mn, 256))
    res = 0
    data = random_f.read(n)
    for i in range(n):
        res += data[i]*255**i
    return  mn + res%(mx-mn)




def draw_circle(X, Y, r, m, v=1):
    mnx = max(0, X-r)
    mxx = min(m.shape[0]-1, X+r)
    mny = max(0, Y - r)
    mxy = min(m.shape[1]-1, Y + r)
    for x in range(mnx, mxx+1):
        mn =  math.sqrt(r**2 - (X-x)**2)
        print(x/X)
        for y in range(mny, mnx+1): #(int(mny+mn), math.ceil(2*mn+mny)):
            if((x-X)**2 + (y-Y)**2 <= r**2):
                m[x][y] = v


random = get_random_n
data = []
times = []
end = []
nxt = 0
def e():
    global end
    i = input()
    end.append(0)
    print("END")

if __name__ == "__main__":

    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    # Если матрица одноканальная (ЧБ), ставим isColor=False
    video_writer = cv.VideoWriter('simulation_output.mp4', fourcc, 30.0, (1000, 1000), isColor=False)



    dt = 10 ** -10
    shape = (2000, 2000)
    c = 5500 *shape[0]/2
    sim = Simulation(shape, c=c, dt=dt)#, device = torch.device("cpu"))


    def f():
        global nxt
        data.append(float(sim.field[shape[0]//2][shape[1]*2//3]))
        times.append(sim.T)
        sim.V *= 1 - 10**(-9)

        if sim.T >= nxt:
            nxt = sim.T + 100*sim.dt
            tensor_4d = sim.field.unsqueeze(0).unsqueeze(0)

            # 2. Масштабируем до 1000x1000 прямо силами графического чипа (Metal)
            # Bilinear на mps работает очень быстро
            resized_mps = F.interpolate(tensor_4d, size=(1000, 1000), mode='bilinear', align_corners=False).squeeze()

            # 3. Находим мин и макс на mps
            mn = resized_mps.min()
            mx = resized_mps.max()

            # 4. Нормализуем и приводим к uint8 на mps
            # Добавляем 1e-5 от деления на ноль
            show_tensor = ((resized_mps - mn) * (255.0 / (mx - mn + 1e-5))).to(torch.uint8)

            # 5. Переносим на CPU и превращаем в numpy.
            # Так как память общая, .cpu().numpy() на Mac — это фактически просто создание "обертки"
            show_np = show_tensor.cpu().numpy()
            # 6. Отрисовываем. cv.resize больше НЕ НАДО вызывать, картинка уже 1000x1000
            # cv.imshow("field", show_np)
            video_writer.write(show_np)
            # cv2.imwrite(f"/Users/artembatanin/PycharmProjects/Science/Labs/Coffee/data/field{k}.jpg", show_np)
            # cv.waitKey(1)
            # sim.field[shape[0]//2, shape[1]//2] = math.sin(2*math.pi*sim.T/500*c)
            print(sim.T/sim.toe)
    sim.f = f

    sim.masses.fill_((6000/343)**2*10**10)
    L = 1000
    H = 100
    sim.masses[shape[0]//2 - H//2:shape[0]//2+H//2,shape[1]//2 - L//2:shape[1]//2 + L//2] = 1
    for i in range(10):
        sim.field[shape[0]//2 - H//2:shape[0]//2 + H//2, shape[1]//2 - L//2+i] = 10#10*math.cos(math.pi*i/100/2)

    to_show_1 = torch.zeros((shape[0]//20, shape[1]//20), dtype=torch.float32)
    to_show = torch.zeros((shape[0]//20, shape[1]//20), dtype=torch.float32)
    i = 0
    sim.set_max_dt()
    sim.toe = L*6/c

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
    k = 0

    while 1:
        time.sleep(0.01)
        """
        tensor_4d = sim.field.unsqueeze(0).unsqueeze(0)

        # 2. Масштабируем до 1000x1000 прямо силами графического чипа (Metal)
        # Bilinear на mps работает очень быстро
        resized_mps = F.interpolate(tensor_4d, size=(1000, 1000), mode='bilinear', align_corners=False).squeeze()

        # 3. Находим мин и макс на mps
        mn = resized_mps.min()
        mx = resized_mps.max()

        # 4. Нормализуем и приводим к uint8 на mps
        # Добавляем 1e-5 от деления на ноль
        show_tensor = ((resized_mps - mn) * (255.0 / (mx - mn + 1e-5))).to(torch.uint8)

        # 5. Переносим на CPU и превращаем в numpy.
        # Так как память общая, .cpu().numpy() на Mac — это фактически просто создание "обертки"
        show_np = show_tensor.cpu().numpy()
        # 6. Отрисовываем. cv.resize больше НЕ НАДО вызывать, картинка уже 1000x1000
        cv.imshow("field", show_np)
        video_writer.write(show_np)
        #cv2.imwrite(f"/Users/artembatanin/PycharmProjects/Science/Labs/Coffee/data/field{k}.jpg", show_np)
        cv.waitKey(1)
        k+= 1
        print(sim.T)
        """
        if sim.T >= sim.toe or len(end) != 0 :
            video_writer.release()
            plt.plot(times, data)
            plt.show()
            file = open("simulation_output.txt", "w")
            json.dump([data, times], file)
            file.close()

            break
