import serial
import time
import datetime
from bson import ObjectId
from datetime import datetime
from sensor import Sensor
from mongo_conect import Mongoconection
from mangas import Mangas

class ConexionSerial:
    def __init__(self, puerto="COM10", tasa_baudios=9600):
        self.tasa = tasa_baudios
        self.puerto = puerto
        self.db = Mongoconection("Mangas", "Mangas", "mongodb+srv://leoskic:0000@cluster0.zqrur.mongodb.net/")
        self.chaleco = Mangas()
        self.chaleco.loadJson("datos_local.json")
        print(self.chaleco)
    
    def leer_puerto(self):
        # Inicializa la conexión serial
        ser = serial.Serial("COM10", 9600, timeout=1)

        # Espera un poco para que se establezca la conexión
        time.sleep(2)

        try:
            while True:
                if ser.in_waiting > 0:  # Verifica si hay datos disponibles para leer
                    line = ser.readline().decode('utf-8').rstrip()  # Lee la línea y decodifica
                    fecha = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                    parts = line.split(':')
                    sensor = Sensor(parts[0], parts[1], fecha)
                    print(sensor)
                    # self.mandarInfoLocal()
                    self.actualizarSensores(sensor)

        except KeyboardInterrupt:
            print("Lectura interrumpida.")

        finally:
            ser.close()

    def actualizarSensores(self, data):
    # Verifica si la conexión a MongoDB está activa
    
        if self.db.ping():
            try:
                # Intenta actualizar el documento en la base de datos
                sensor_data = data.getDictS()  # Asegúrate de que 'data' tenga este método
                result = self.db.collection.update_one(
                    {"no_manga": self.chaleco[0].no_manga},  # Busca por el ID en chaleco
                    {"$push": {"sensores": sensor_data}}       # Actualiza el arreglo 'sensores'
                )
                print(f"Resultado de la actualización: {result.modified_count} documento(s) actualizado(s).")
            except Exception as e:
                print(f"Error al actualizar en MongoDB: {e}")
        else:
        # Si la conexión a MongoDB falla, guarda los datos localmente
            try:
                self.chaleco.sensor.agregar_objeto(data)  # Agrega el sensor al objeto local
                self.chaleco.saveJson("datos_local.json")  # Guarda los datos en un archivo local
                print("Conexión fallida. Sensor guardado localmente.")
            except Exception as e:
                print(f"Error al guardar localmente: {e}")
            
    def mandarInfoLocal(self):
    # Verifica si la conexión a MongoDB está activa
        if self.db.ping():
            if self.chaleco[0].sensor.objetos:  # Comprueba si hay sensores almacenados localmente
                for sensor in self.chaleco[0].sensor.objetos:
                    try:
                        # Inserta cada sensor en MongoDB
                        sensor_data = sensor.getDictS()  # Obtén los datos del sensor como un diccionario
                        result = self.db.collection.update_one(
                            {"no_manga": self.chaleco[0].no_manga},  # Usa el ID correcto
                            {"$push": {"sensores": sensor_data}}       # Agrega el sensor al arreglo
                        )
                        print(f"Sensor sincronizado con MongoDB. Resultado: {result.modified_count}")
                    except Exception as e:
                        print(f"Error al sincronizar sensor: {e}")
                
                # Vacía los sensores locales después de sincronizarlos
                self.chaleco.sensor = Sensor()
                self.chaleco.saveJson("datos_local.json")  # Actualiza el archivo local
                print("Sensores locales sincronizados y limpiados.")
            else:
                print("No hay información de sensores para subir.")
        else:
            print("Conexión a MongoDB fallida. Los datos no se pueden sincronizar.")

        # Considera si realmente necesitas llamar a `self.leer_puerto()` aquí
        self.leer_puerto()
        
    def ping(self):
            conexion= Mongoconection("Mangas")
            validar=conexion.ping()
            return validar 

if __name__ == "__main__":
    conexion = ConexionSerial()
    conexion.leer_puerto()