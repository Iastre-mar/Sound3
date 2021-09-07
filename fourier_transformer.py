import os
import numpy as np


class Fft(object):
    def __init__(self, fs, output_dir_fourier, prefix='four'):
        self.fs = fs
        self.name = None
        self.prefix = prefix
        self.output_dir_fourier = output_dir_fourier

    def transform(self, achank):
        """
        Вроде высчитывает преобразование Фурье
        """
        decoded = np.frombuffer(achank[0], dtype=np.int16)  # Только левый канал
        FFT = np.fft.rfft(decoded)  # Преобразование Фурье
        filename = os.path.join(self.output_dir_fourier, self.prefix + '_' + self.name + ".bin")
        file = open(filename, 'ab')
        np.array(FFT, dtype=np.csingle).tofile(file)
        file.close()
        return None
