import pyaudio
import numpy as np


class Reader(object):
    """
    Микрофон
    """

    def __init__(self, audio_input_queue, n_channels, fs, chunk_size=1024):
        self.audio_input_queue = audio_input_queue  # Очередь для буферизации поступающего аудиосигнала
        self.n_channels = n_channels  # Число каналов
        self.fs = fs  # Частота дискретизации сигнала
        self.CHUNK = chunk_size
        self.FORMAT = pyaudio.paInt16  # Иначе записывает звуки ада, нужно разобраться
        # Инициализация объекта pyaudio
        self.p = pyaudio.PyAudio()
        self.SAMPWIDTH = self.p.get_sample_size(self.FORMAT)
        # Открытие аудиопотока
        self.open_stream()

    def callback(self, in_data, frame_count, time_info, status):
        """
        Странная многопоточность встроенная в pyaudio
        """
        try:
            if not self.audio_input_queue.full():
                self.audio_input_queue.put([in_data])
            return None, pyaudio.paContinue
        except RuntimeError as re:
            # Если что-то затормозит то программа не упадет
            return None, pyaudio.paContinue

    def open_stream(self):
        """
        Открытие аудиопотока pyaudio
        """
        self.audio_stream = self.p.open(format=self.FORMAT,
                                        channels=self.n_channels,
                                        rate=self.fs,
                                        input=True,
                                        frames_per_buffer=self.CHUNK,
                                        stream_callback=self.callback)

        return None

    def start_streaming(self):
        self.audio_stream.start_stream()
        return None

    def stop_streaming(self):
        """
        Остановка потока
        """
        # Закрытие потока
        self.audio_stream.stop_stream()
        self.audio_stream.close()
        # Уничтожение объекта pyaudio
        self.p.terminate()
        return None
