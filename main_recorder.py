import os
import time
import multiprocessing
import audio_reader
import wav_writer
from fourier_transformer import Fft

# Параметры для чтения аудиосигнала
QMAXSIZE = 20  # Максимальное число элементов в очереди
audio_input_queue = multiprocessing.Queue(QMAXSIZE)

n_channels = 2  # Число каналов
fs = 44100  # Частота дискретизации
chunk_size = 1024 * n_channels  # Размер чанка в фреймах
stream_reader = audio_reader.Reader(audio_input_queue, n_channels, fs, chunk_size)  # Микрофон

# Параметры для записи wav файлов
output_dir_wav = os.path.join('./data/wav')
os.makedirs(os.path.dirname(output_dir_wav), exist_ok=True)
filename_prefix_wav = 'rec'
wav_length_second = 10  # Длина фрагмента записи
file_writer = wav_writer.Writer(n_channels, fs, chunk_size, stream_reader.SAMPWIDTH,
                                wav_length_second, output_dir_wav, filename_prefix_wav)  # Запись wav

# Длина записи
record_length = 60
max_count = int(record_length * fs // chunk_size)
count = 0

# Параметры для записи после разложения Фурье
output_dir_fourier = os.path.join('./data/fourier')
os.makedirs(os.path.dirname(output_dir_fourier), exist_ok=True)
filename_prefix_fourier = 'four'
fft = Fft(fs=fs, output_dir_fourier=output_dir_fourier, prefix=filename_prefix_fourier)

stream_reader.start_streaming()
start_time = time.time()
while count < max_count:
    if not audio_input_queue.empty():
        achunk = audio_input_queue.get()
        file_writer.write_wav(achunk)
        fft.name = file_writer.name
        fft.transform(achunk)
        count += 1
print('Длительность работы программы: {:.4f} s'.format(time.time() - start_time))
print('Длительность записанных wav файлов: {:.4f} s'.format(chunk_size * max_count / fs))
stream_reader.stop_streaming()
file_writer.close_file()
# Чтобы избежать broken pipe error очередь должна быть завершена?
while not audio_input_queue.empty():
    achunk = audio_input_queue.get()
audio_input_queue.close()
audio_input_queue.join_thread()
print("Отработала")
