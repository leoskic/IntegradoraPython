from listaObjetos import ListaObjetos
import json
import datetime
from datetime import datetime

class Sensor(ListaObjetos):
    
    def __init__(self, clave=None, valor=None, fecha=None):
        super().__init__()
        if clave is None and fecha is None and valor is None:
            self.list = True
        else:
            self.list = False
        self.clave = clave
        self.valor = valor
        self.fecha = fecha
        

    

    def __str__(self):
         if self.list:
            return self.mostList()
         else:
            return f"tipo : {self.clave}, data : {self.valor}, date : {self.fecha} "
        
    def getDictS(self):
        if self.list:
            return [a.getDictS() for a in self.objetos]
        else:
            return {
                "tipo": self.clave,
                "data" : self.valor,
                "date" : self.fecha
            }
        
            

    def saveJson(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.getDictS(), f, indent=4)
            
    def loadJson(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            self.toObject(data)
            
    def toObject(self, data):
            for item_data in data:
                sen = Sensor(item_data['tipo'], item_data['data'], item_data['date'])
                self.agregar_objeto(sen)


if __name__ == "__main__":
    fecha = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    sen = Sensor("PU01", "45", fecha)
    sen.saveJson("datos_local.json") 
   
    
    