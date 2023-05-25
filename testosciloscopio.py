import pyvisa #pip install pyvisa (https://pyvisa.readthedocs.io/en/latest/)
import numpy as np
from struct import unpack
import pylab

# Abrir comunicacion con el osciloscopio
scope = pyvisa.instrument("USB0::0x0699::0x0363::C065087::INSTR")

# Configurar el osciloscopio
scope.write(":STOP")
scope.write(":WAV:POIN:MODE RAW")
scope.write(":WAV:FORM BYTE")
scope.write(":WAV:BYT_N 1")
scope.write(":WAV:DATA?")
rawdata = scope.read_raw()
scope.write(":RUN")

# Obtener los datos
headerlen = 2 + int(rawdata[1])
header = rawdata[:headerlen]
ADC_wave = rawdata[headerlen:-1]
ADC_wave = np.array(unpack('%sB' % len(ADC_wave),ADC_wave))

# Obtener los parametros de la forma de onda
scope.write(":WAV:XINC?")
xinc = float(scope.read())
scope.write(":WAV:XOR?")
xor = float(scope.read())
scope.write(":WAV:YINC?")
yinc = float(scope.read())
scope.write(":WAV:YOR?")
yor = float(scope.read())

# Graficar
x = np.arange(0, xinc*len(ADC_wave), xinc)
y = yinc*(ADC_wave - yor)
pylab.plot(x,y)
pylab.show()
