

class ListaObjetos:
    def __init__(self):
        # Inicializar lista objeto 
        self.objetos = []

    def __getitem__(self, index):
        # Buscar por index
        
        return self.objetos[index]

    def __setitem__(self, index, objeto):
        # Actualizar
        self.objetos[index] = objeto

    def __len__(self):
        # Cantidad de objetos lista
        return len(self.objetos)

    # def __str__(self):
    #    #Mostrar lista en lista
    #     return '\n'.join([str(objeto) for objeto in self.objetos])
    
    """def mostList(self):
       #Mostrar lista en lista
        return '\n'.join(str(objeto) for objeto in self.objetos)"""
    def mostList(self):
            # Mostrar lista enumerada
            if not self.objetos:
                return "No hay objetos en la lista."
            
            return '\n'.join(f"{i + 1}. {str(objeto)}" for i, objeto in enumerate(self.objetos))


    def agregar_objeto(self, objeto):
        # Agregar un objeto
        self.objetos.append(objeto)

    def eliminar_objeto(self, index):
        # Eliminar un objeto con idex
        if 0 <= index < len(self.objetos):
            del self.objetos[index]
        else:
            print("Índice fuera de rango")

    def listar_objetos(self):
        # Mostrar la lista de objetos
        return [str(objeto) for objeto in self.objetos]
