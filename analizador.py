import re

class Separador_Lexico:
    
    
    def __init__(self):
        # Rutas de archivos
        self.ruta_ops = r"C:\Users\Ruddyard\Desktop\ProyEnGit\archivos\Archivos de diccionario\operadores\operadores.txt"
        self.ruta_prs = r"C:\Users\Ruddyard\Desktop\ProyEnGit\archivos\Archivos de diccionario\palabras reservadas\palabrasReservadas.txt"
        self.ruta_ptn = r"C:\Users\Ruddyard\Desktop\ProyEnGit\archivos\Archivos de diccionario\patrones\patrones.txt"
        
        # Cargar datos
        self.ops = self._cargar_operadores()
        self.prs = self._cargar_palabras_reservadas()
        self.patrones_tokens = self._cargar_patrones()
    
    def _cargar_desde_archivo(self, ruta_archivo):
        """Carga contenido de un archivo y retorna lista de líneas"""
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                elementos = [linea.strip() for linea in archivo if linea.strip()]
            return elementos
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {ruta_archivo}")
            return []
        except Exception as e:
            print(f"Error al leer el archivo {ruta_archivo}: {e}")
            return []
    
    def _cargar_operadores(self):
        """Carga y procesa operadores"""
        ops = self._cargar_desde_archivo(self.ruta_ops)
        return [op.upper() for op in ops]
    
    def _cargar_palabras_reservadas(self):
        """Carga y procesa palabras reservadas"""
        prs = self._cargar_desde_archivo(self.ruta_prs)
        return [pr.upper() for pr in prs]
    
    def _cargar_patrones(self):
        """Carga y procesa patrones regex"""
        token_patron = self._cargar_desde_archivo(self.ruta_ptn)
        patrones = []
        
        for patron in token_patron:
            if ',' in patron:
                regex, tipo = patron.split(',', 1)
                patrones.append((regex.strip(), tipo.strip()))
        
        return patrones
    
    def separar_token(self, cTexto):
       
        tokens_result = []
        alineas = cTexto.splitlines()
        
        for num_linea, clineas in enumerate(alineas, 1):
            aTokens = clineas.split()
            
            for cPalabra in aTokens:
                token_encontrado = False  
                
                palabra = cPalabra.upper()
                if palabra in self.prs:
                    tokens_result.append({
                        'tipo': 'PR',
                        'valor': cPalabra,
                        'linea': num_linea
                    })
                    token_encontrado = True
                elif palabra in self.ops:
                    tokens_result.append({
                        'tipo': 'OP',
                        'valor': cPalabra,
                        'linea': num_linea
                    })
                    token_encontrado = True
                
                # LUEGO verificar patrones regex
                if not token_encontrado:
                    for patron, token_type in self.patrones_tokens:
                        if re.match(patron, cPalabra):
                            tokens_result.append({
                                'tipo': token_type,
                                'valor': cPalabra,
                                'linea': num_linea
                            })
                            token_encontrado = True
                            break
                
                # si no coincide con nada, es ID
                if not token_encontrado:
                    tokens_result.append({
                        'tipo': 'ID',
                        'valor': cPalabra,
                        'linea': num_linea
                    })
        
        return tokens_result


'''
if __name__ == "__main__":
    analizador = Separador_Lexico()
    
    resultado = analizador.separar_token("if variable + 10  \n if variable + 10  ")

    for token in resultado:
        print(f"Línea {token['linea']}: {token['tipo']}({token['valor']})")'''