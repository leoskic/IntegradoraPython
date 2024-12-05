import serial
import time

# Configura el puerto serial y la velocidad de transmisión
arduino = serial.Serial(port='COM10', baudrate=9600, timeout=1)

time.sleep(2)  # Esperar 2 segundos para que el Arduino se inicialice

# Enviar datos al Arduino
arduino.write(b'Hola Arduino\n')

# Leer datos enviados desde el Arduino
while True:
    if arduino.in_waiting > 0:  # Verifica si hay datos disponibles
        data = arduino.readline().decode('utf-8').strip()  # Lee y decodifica la línea
        print("Data from Arduino:", data)
        time.sleep(1)

# Cerrar la conexión al finalizar
arduino.close()

