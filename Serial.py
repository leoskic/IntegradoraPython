import serial
import json
import time
import pymongo
from sensor import Sensor
from pymongo import MongoClient
from datetime import datetime

class ConexionSerial:
    def _init_(self, puerto, tasa_baudios=9600):
        try:
            self.ser = serial.Serial(puerto, tasa_baudios)
            print(f"Conexión establecida en {puerto}")
        except serial.SerialException:
            print(f"Error: No se pudo conectar al puerto {puerto}")
            self.ser = None  

    def leer_linea(self):
        if self.ser and self.ser.in_waiting > 0:  # Verifica si hay datos disponibles
            try:
                return self.ser.readline().decode('utf-8', 'ignore').strip()
            except UnicodeDecodeError:
                print("Error de codificación al leer datos.")
                return None
        return None

    def leer_puerto(self):
        # Inicializa la conexión serial
        ser = serial.Serial(self.port, self.baudrate, timeout= self.timeout)

        # Espera un poco para que se establezca la conexión
        time.sleep(2)

        try:
            while True:
                if ser.in_waiting > 0:  # Verifica si hay datos disponibles para leer
                    line = ser.readline().decode('utf-8').rstrip()  # Lee la línea y decodifica
                    fecha = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                    parts = line.split(':')
                    sensor = Sensor(parts[0], parts[1], fecha)
                    self.mandarInfoLocal()
                    self.actualizarSensores(sensor)




        except KeyboardInterrupt:
            print("Lectura interrumpida.")

        finally:
            ser.close()
    


    def cerrar(self):
        if self.ser:
            self.ser.close()
            print("Conexión cerrada.")


class GestorSensores:
    def __init__(self, archivo_config, puertos_seriales, uri_mongo="mongodb://localhost:27017/", db_nombre="TechRoom"):
        self.configuracion_sensores = self.cargar_configuracion(archivo_config)
        # Inicializa una lista de conexiones seriales para cada puerto especificado
        self.conexiones_seriales = [ConexionSerial(puerto) for puerto in puertos_seriales]
        
        # Conectar a MongoDB
        self.client = MongoClient(uri_mongo)  # Conecta al servidor MongoDB
        self.db = self.client[db_nombre]  # Selecciona la base de datos
        self.collection = self.db['Sensores']  # Selecciona la colección donde se guardarán los datos

    def cargar_configuracion(self, archivo_config):
        try:
            with open(archivo_config, 'r') as f:
                # Lee y convierte el archivo JSON a un diccionario de configuración
                configuracion = json.load(f)
                # Crea un diccionario para buscar sensores por su 'id'
                return {sensor["id"]: sensor for sensor in configuracion}
        except FileNotFoundError:
            print("Error: El archivo config.json no fue encontrado.")
            return {}
        except json.JSONDecodeError:
            print("Error: El archivo config.json tiene un formato incorrecto.")
            return {}

    def procesar_datos(self, datos):
        datos_procesados = {}
        lineas = datos.strip().split('\n')  # Divide los datos en líneas individuales

        for linea in lineas:
            if linea.startswith(("USN", "LER", "LEA", "LEV", "DTT", "DHH", "SMQ", "PIR", "MAG")):
                partes = linea.split(":")
                if len(partes) == 2:
                    clave = partes[0].strip()
                    valor = partes[1].strip()
                    datos_procesados[clave] = valor  

        return datos_procesados

    def mostrar_datos(self, datos_procesados):
        print("================ DATOS RECIBIDOS =================")
        print("Descripción detallada de los dispositivos conectados:")

        dispositivos = []

        for clave, valor in datos_procesados.items():
            # Busca información del sensor en el archivo de configuración
            info_sensor = self.configuracion_sensores.get(clave[:3])
            if info_sensor:
                nombre = info_sensor["nombre"]
                tipo_sensor = info_sensor["sensor"]
                unidad = info_sensor.get("valor") or info_sensor.get("unidades", "")
                
                # Formatea la información de cada dispositivo
                dispositivos.append(f"- Dispositivo: {nombre}, Tipo de sensor/dispositivo: {tipo_sensor}, Valor medido: {valor} {unidad if unidad else ''}")
            else:
                dispositivos.append(f"- {clave}: {valor}")

        print("\n".join(dispositivos))
        print("==================================================")

        # Guardar los datos procesados en MongoDB
        self.guardar_datos_mongo(datos_procesados)

    def guardar_datos_mongo(self, datos_procesados):
        # Añadir la fecha y hora actual a los datos
        datos_procesados['timestamp'] = datetime.now()

        # Insertar los datos en la colección de MongoDB
        try:
            self.collection.insert_one(datos_procesados)
            print("Datos guardados en MongoDB.")
        except Exception as e:
            print(f"Error al guardar los datos en MongoDB: {e}")

    def ejecutar(self):
        try:
            while True:
                # Lee datos de cada conexión serial
                for conexion in self.conexiones_seriales:
                    datos = conexion.leer_linea()
                    if datos:
                        datos_procesados = self.procesar_datos(datos)
                        self.mostrar_datos(datos_procesados)
        except KeyboardInterrupt:
            print("Cerrando conexiones...")
            for conexion in self.conexiones_seriales:
                conexion.cerrar()
            print("Programa terminado.")


if __name__ == "_main_":
    puertos_seriales = ['COM3', 'COM4']  # Cambiar según los puertos de tus dispositivos
    gestor_sensores = GestorSensores('config.json', puertos_seriales)
    gestor_sensores.ejecutar()