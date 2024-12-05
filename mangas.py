import json
from sensor import Sensor
from listaObjetos import ListaObjetos


class Mangas(ListaObjetos):
    def __init__(self, no_manga=None, usuario=None, sensor=None):
 
            super().__init__()
            if no_manga is None:
                self.list = True
            else:
                self.list = False
            self.no_manga = no_manga
            self.usuario = usuario
            self.sensor = sensor
    
    def __str__(self):
        if self.list:
            return self.mostList()
        else:
            return f"{self.no_manga}, {self.usuario} Alumnos: \n{self.sensor}"   
        
    def getDict(self):
        if self.list == False:
            return {
                "no_manga": self.no_manga,
                "user" : self.usuario,
                "sensores" : self.sensor.getDictS()
            }
        else:
            return [g.getDict() for g in self.objetos]

        
    def saveJson(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.getDict(), f, indent=4)
            
                
    def loadJson(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            self.toObject(data)


    def toObject(self, data):
            for item_data in data:
                sensores = Sensor()
                sensores.toObject(item_data['sensores'])
                grupo = Mangas(item_data['no_manga'], item_data['user'], sensores)
                self.agregar_objeto(grupo)

            
if __name__ == "__main__":
    s = Sensor()
    x = Mangas("1", "2", s)
    x.getDict()
    print(x.getDict())
    
    
    
    
    



