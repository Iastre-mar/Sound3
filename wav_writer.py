import os
import time
import math
import wave


class Writer(object):
    def __init__(self, n_channels, fs, chunk_size, sampwidth, wav_length_second=1,
                 output_dir_wav='./data/wav', prefix='rec'):
        self.n_channels = n_channels
        self.fs = fs
        self.chunk_size = chunk_size
        self.sampwidth = sampwidth
        self.wav_length_second = wav_length_second
        self.max_frame_count = int(math.floor(self.wav_length_second * self.fs /
                                              self.chunk_size))
        self.output_dir_wav = output_dir_wav
        self.prefix = prefix
        self.name = None
        self.count_frame = 0
        self.io_flag = False

    def open_file(self):
        self.name = time.strftime("%Y-%m-%d-%H-%M-%S")
        filename = os.path.join(self.output_dir_wav, self.prefix + '_' + self.name + ".wav")
        try:
            self.wf = wave.open(filename, 'wb')
            self.wf.setnchannels(self.n_channels)
            self.wf.setsampwidth(self.sampwidth)
            self.wf.setframerate(self.fs)
            self.io_flag = True
        except IOError as ie:
            # Наверное нужно что-то более адекватное
            self.io_flag = False

        return self.io_flag

    def write_wav(self, input_stream):
        if self.count_frame == 0:
            self.open_file()
        if self.count_frame == self.max_frame_count:
            # Закрывает текущий файл
            self.wf.close()
            self.open_file()
            self.count_frame = 0
        # Пишет текущий файл
        if self.io_flag:
            self.wf.writeframes(b''.join(input_stream))
            self.count_frame += 1

        return None

    def close_file(self):
        self.wf.close()
