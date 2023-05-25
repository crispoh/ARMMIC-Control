import pyvisa
import numpy as np

# Crear instancia del administrador de recursos
rm = pyvisa.ResourceManager()

# Abrir conexión con el osciloscopio
osciloscopio = rm.open_resource("USB0::0x0699::0x0367::C050620::INSTR")

# Configurar el osciloscopio para adquirir los datos de la forma de onda
osciloscopio.write("DAT:SOU CH1")  # Configurar la fuente de datos como Canal 1
osciloscopio.write("DAT:ENC RPB")  # Configurar el formato de datos como binario sin comprimir
osciloscopio.write("DAT:WID 2")    # Configurar el ancho de datos en 2 bytes (int16)
osciloscopio.write("DAT:STAR 1")   # Configurar el punto de inicio de los datos en 1
osciloscopio.write("DAT:STOP 1000")# Configurar el punto de parada de los datos en 1000

# Obtener los datos de la forma de onda
datos_binarios = osciloscopio.query_binary_values("CURV?", datatype='h', container=np.array)

# Cerrar la conexión con el osciloscopio
osciloscopio.close()

# Mostrar los primeros 10 valores de los datos
print("Datos de la forma de onda:")
print(datos_binarios[:1000])