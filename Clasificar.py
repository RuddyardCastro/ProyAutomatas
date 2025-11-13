class Separador_Lexico:
    def __init__(self):
        self.ruta_ops = r"C:\Users\Ruddyard\Desktop\ProyEnGit\archivos\Archivos de diccionario\operadores\operadores.txt"
        self.ruta_prs = r"C:\Users\Ruddyard\Desktop\ProyEnGit\archivos\Archivos de diccionario\palabras reservadas\palabrasReservadas.txt"
        self.ruta_ptn = r"C:\Users\Ruddyard\Desktop\ProyEnGit\archivos\Archivos de diccionario\patrones\patrones.txt"

        self.ops = self.cargar_operadores()
        self.prs = self._cargar_palabras_reservadas()
        self.patrones_tokens = self.cargar_patrones()
        self.ops.sort(key=len, reverse=True)  

    
    def cargar_desde_archivo(self, ruta_archivo):
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                return [linea.strip() for linea in f if linea.strip()]
        except:
            return []

    def cargar_operadores(self):
        return [op.upper() for op in self.cargar_desde_archivo(self.ruta_ops)]

    def _cargar_palabras_reservadas(self):
        return [pr.upper() for pr in self.cargar_desde_archivo(self.ruta_prs)]

    def cargar_patrones(self):
        patrones = []
        for linea in self.cargar_desde_archivo(self.ruta_ptn):
            if ',' in linea:
                regu, tipo = linea.split(',', 1)
                patrones.append((regu.strip(), tipo.strip()))
        return patrones

    def es_numero(self, palabra):
        if not palabra:
            return False
        #  Verificar que después del - hay contenido
        if palabra[0] == '-':
            if len(palabra) == 1:  # Solo hay un signo negativo
                return False
            palabra = palabra[1:]
        
        #  Manejar caso de punto decimal al inicio o final
        if palabra.startswith('.') or palabra.endswith('.'):
            return False
            
        partes = palabra.split('.')
        if len(partes) > 2:  
            return False
        return all(p.isdigit() for p in partes if p)  #  validar partes no vacías

    def es_identificador(self, palabra):
        if not palabra:
            return False
        
        if palabra[0].isalpha() or palabra[0] == '_':
            return all(c.isalnum() or c == '_' for c in palabra[1:])
        return False

    def separar_token(self, cTexto):
        tokens_result = []
        lineas = cTexto.splitlines()

        for num_linea, linea in enumerate(lineas, 1):
            i = 0
            while i < len(linea):
                cont = linea[i]

                #  espacios  
                if cont.isspace():
                    i += 1
                    continue

                
                if cont == '#':
                    tokens_result.append({
                        'tipo': 'Coment',
                        'valor': linea[i:],
                        'linea': num_linea
                    })
                    break

                
                token_encontrado = False
                for op in self.ops:
                    if linea[i:i+len(op)].upper() == op:
                        tokens_result.append({
                            'tipo': 'OP',
                            'valor': linea[i:i+len(op)],
                            'linea': num_linea
                        })
                        i += len(op)
                        token_encontrado = True
                        break
                if token_encontrado:
                    continue

                #str
                if cont == '"':
                    fin = i + 1
                    while fin < len(linea) and linea[fin] != '"':
                        fin += 1
                    if fin < len(linea):
                        fin += 1  
                    palabra = linea[i:fin]
                    tokens_result.append({
                        'tipo': 'STR',
                        'valor': palabra,
                        'linea': num_linea
                    })
                    i = fin
                    continue

                
                palabra = ""
                if cont.isalnum() or cont == '_':
                    palabra += linea[i]
                    i += 1
                    while i < len(linea) and (linea[i].isalnum() or linea[i] == '_'):
                        palabra += linea[i]
                        i += 1
                else:
                    
                    palabra = cont
                    i += 1
                    while i < len(linea) and not (linea[i].isalnum() or linea[i].isspace() or linea[i] == '_' or linea[i] == '"'):
                
                        posible_op = palabra + linea[i]
                        op_encontrado = any(op.startswith(posible_op.upper()) for op in self.ops)
                        if not op_encontrado:
                            break
                        palabra += linea[i]
                        i += 1
                
                if palabra:
                    palabra_up = palabra.upper()

                
                    if palabra_up in self.prs:
                        tokens_result.append({
                            'tipo': 'PR',
                            'valor': palabra,
                            'linea': num_linea
                        })
                        continue

                    if self.es_numero(palabra):
                        tokens_result.append({
                            'tipo': 'NUM',
                            'valor': palabra,
                            'linea': num_linea
                        })
                        continue
                    
                    elif self.es_identificador(palabra):
                        tokens_result.append({
                            'tipo': 'ID',
                            'valor': palabra,
                            'linea': num_linea
                        })
                        continue

                    
                    tokens_result.append({
                        'tipo': 'ERROR',
                        'valor': palabra,
                        'linea': num_linea,
                        'descripcion': 'Token no reconocido'
                    })

        return tokens_result