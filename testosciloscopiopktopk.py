import pyvisa

# Crear instancia del administrador de recursos
rm = pyvisa.ResourceManager()

# Abrir conexión con el osciloscopio
osciloscopio = rm.open_resource("USB0::0x0699::0x0367::C050620::INSTR")

# Configurar el osciloscopio y leer la amplitud pico a pico
osciloscopio.write("MEASUrement:IMMed:TYPE PK2pk")  # Configurar la medida pk-pk
valor_pkpk = osciloscopio.query_ascii_values("MEASUrement:IMMed:VALue?")[0]

# Mostrar el resultado en consola
print("Amplitud pico a pico:", valor_pkpk, "V")

# Cerrar la conexión con el osciloscopio
osciloscopio.close()
