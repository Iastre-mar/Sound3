import os
import numpy as np


class Fft(object):
    def __init__(self, fs, chunk_size, four_length_second, output_dir_fourier, prefix='four'):
        self.fs = fs
        self.chunk_size = chunk_size
        self.four_length_second = four_length_second
        self.max_frame_count = int(np.floor(self.four_length_second * self.fs /
                                            self.chunk_size))
        self.name = None
        self.prefix = prefix
        self.output_dir_fourier = output_dir_fourier
        self.count_frame = 0
        self.io_flag = False

    def open_file(self):
        filename = os.path.join(self.output_dir_fourier, self.prefix + '_' + self.name + ".bin")
        try:
            self.file = open(filename, 'wb')
            self.io_flag = True
        except IOError as ie:
            self.io_flag = False

    def write_four(self, input_stream):
        """
        Записывает звук, преобразованный через Фурье (Вероятно)
        """
        if self.count_frame == 0:
            self.open_file()
            self.segment = []
        if self.count_frame == self.max_frame_count:
            # Записывает отрезок и открывает новый
            FFT = np.fft.rfft(self.segment)
            np.array(FFT, dtype=np.csingle).tofile(self.file)
            self.file.close()
            self.open_file()
            self.count_frame = 0
            self.segment = []
        if self.io_flag:
            self.segment.extend(np.frombuffer(input_stream[0], dtype=np.int16))
            #result = np.reshape(result, (frames_per_buffer, 2))
            #Now to access the left channel, use result[:, 0], and for right channel, use result[:, 1]
            self.count_frame += 1

        return None

    def close_file(self):
        self.file.close()
