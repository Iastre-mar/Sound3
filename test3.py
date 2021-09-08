import matplotlib.pyplot as plt
import numpy as np

f = open('./data/fourier/four_2021-09-08-16-08-23.bin', 'rb')
data = np.fromfile(f, dtype=np.csingle)
f.close()
N = int(len(data) * 2) - 1  # Нужно переделать, не знаю почему так
T = 1 / 44100
xf = np.fft.rfftfreq(N, T)
yf = 10*np.log10(np.abs(data))  # Возможно перевод в децибелы
#yf = np.abs(data)

plt.subplot(1, 1, 1, label="test")
plt.title('Разложение Фурье')
plt.plot(xf, yf, 'g')
#plt.xlim(4, 3000)
plt.ylabel('Амплитуда (dB)')
plt.xlabel('Частота (Hz)')

plt.subplots_adjust(hspace=1)
plt.rc('font', size=15)
fig = plt.gcf()
fig.set_size_inches(16, 9)
fig.savefig('Fourier.png', dpi=160)
