class AFD_analizar:
    # ---------- Métodos de carga ----------
    def __init__(self):
        
        self.ruta_ops = r"C:\Users\Ruddyard\Desktop\ProyEnGit\archivos\Archivos de diccionario\operadores\operadores.txt"
        self.ruta_prs = r"C:\Users\Ruddyard\Desktop\ProyEnGit\archivos\Archivos de diccionario\palabras reservadas\palabrasReservadas.txt"
        self.ruta_ptn = r"C:\Users\Ruddyard\Desktop\ProyEnGit\archivos\Archivos de diccionario\patrones\patrones.txt"

        # Cargar datos
        self.ops = self.cargar_operadores()
        self.prs = self.cargar_palabras_reservadas()
        self.patrones_tokens = self.cargar_patrones()

        # Ordenar operadores de mayor a menor longitud
        self.ops.sort(key=len, reverse=True)

   
    def cargar_desde_archivo(self, ruta):
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                return [linea.strip() for linea in f if linea.strip()]
        except:
            return []

    def cargar_operadores(self):
        return [op.upper() for op in self.cargar_desde_archivo(self.ruta_ops)]

    def cargar_palabras_reservadas(self):
        return [pr.upper() for pr in self.cargar_desde_archivo(self.ruta_prs)]

    def cargar_patrones(self):
        patrones = []
        for linea in self.cargar_desde_archivo(self.ruta_ptn):
            if ',' in linea:
                regex, tipo = linea.split(',', 1)
                patrones.append((regex.strip(), tipo.strip()))
        return patrones

    # ---------- Método  separar token ----------
    def separar_token(self, cTexto, separador_lexico):
     
        return separador_lexico.separar_token(cTexto)

    # ---------- Métodos extras ----------
    def Es_num(self, palabra):
        if not palabra:
            return False
        if palabra.count('.') == 1:
            p1, p2 = palabra.split('.', 1)
            return p1.isdigit() and p2.isdigit()
        return palabra.isdigit()

    def Es_id(self, palabra):
        if not palabra:
            return False
        if palabra[0].isalpha() or palabra[0] == "_":
            return all(c.isalnum() or c == "_" for c in palabra[1:])
        return False

   #---------------------------------------------------------------------------
    def analizar_sintaxis(self, tokens):
        errores = []
        i = 0
        while i < len(tokens):
            t = tokens[i]
            tipo = t['tipo']
            val = t['valor']
            linea = t['linea']

           
            if tipo == 'Coment':
                i += 1
                continue

            # Verificación token inválido
            if tipo not in ('ID', 'NUM', 'PR', 'OP', 'CADENA', 'STR', 'Coment'):
                errores.append(f"L{linea}: Token inválido '{val}'")

            
            if tipo == 'NUM' and (i == 0 or tokens[i-1]['linea'] != linea):
                errores.append(f"L{linea}: No puede iniciar con número '{val}'")

            # Verificación identificador válido
            if tipo == 'ID' and not self.Es_id(val):
                errores.append(f"L{linea}: Identificador inválido '{val}'")

            # Verificación asignación
            if tipo == 'ID' and i + 1 < len(tokens) and tokens[i + 1]['valor'] == '=':
                if i + 2 >= len(tokens):
                    errores.append(f"L{linea}: Falta expresión después de '='")
                else:
                    siguiente = tokens[i + 2]
                    if siguiente['tipo'] not in ('ID', 'NUM', 'CADENA', 'STR'):
                        errores.append(f"L{linea}: Expresión inválida después de '=': '{siguiente['valor']}'")
                i += 2  

            i += 1

        return errores