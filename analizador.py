import re
#? Strip eleiimina espacios 
def cargar_desde_archivo(ruta_archivo):
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


ruta_ops = r"C:\Users\Ruddyard\Desktop\ProyEnGit\archivos\Archivos de diccionario\operadores\operadores.txt"
ruta_prs = r"C:\Users\Ruddyard\Desktop\ProyEnGit\archivos\Archivos de diccionario\palabras reservadas\palabrasReservadas.txt"
ruta_ptn = r"C:\Users\Ruddyard\Desktop\ProyEnGit\archivos\Archivos de diccionario\patrones\patrones.txt"



ops = [op.upper() for op in cargar_desde_archivo(ruta_ops)]
prs = [pr.upper() for pr in cargar_desde_archivo(ruta_prs)]
token_patron = cargar_desde_archivo(ruta_ptn)

#-- Por se archivo txt se agrega 
#lista
patrones_tokens = []
for patron in token_patron:
    if ',' in patron:
        #-- Split limina epacio 
        regex, tipo = patron.split(',', 1)
        patrones_tokens.append((regex.strip(), tipo.strip()))


def Separar_Token(cTexto):
    tokens_result = []
    alineas = cTexto.splitlines()
    
    for num_linea, clineas in enumerate(alineas, 1):
        aTokens = clineas.split()
        
        for cPalabra in aTokens:
            token_encontrado = False  
            
        
            palabra = cPalabra.upper()
            if palabra in prs:
                tokens_result.append({
                    'tipo': 'PR',
                    'valor': cPalabra,
                    'linea': num_linea
                })
                token_encontrado = True
            elif palabra in ops:
                tokens_result.append({
                    'tipo': 'OP',
                    'valor': cPalabra,
                    'linea': num_linea
                })
                token_encontrado = True
            
            # LUEGO verificar patrones regex
            if not token_encontrado:
                for patron, token_type in patrones_tokens:
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

resultado = Separar_Token("if variable + 10  \n if variable + 10  ")

for token in resultado:
    print(f"Línea {token['linea']}: {token['tipo']}({token['valor']})")

'''
