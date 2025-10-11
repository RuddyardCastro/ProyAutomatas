class AFD_analizar:
    def __init__(self):
        # Rutas de archivos
        self.ruta_ops = r"C:\Users\Ruddyard\Desktop\ProyEnGit\archivos\Archivos de diccionario\operadores\operadores.txt"
        self.ruta_prs = r"C:\Users\Ruddyard\Desktop\ProyEnGit\archivos\Archivos de diccionario\palabras reservadas\palabrasReservadas.txt"
        self.ruta_ptn = r"C:\Users\Ruddyard\Desktop\ProyEnGit\archivos\Archivos de diccionario\patrones\patrones.txt"

        # Cargar datos
        self.ops = self._cargar_operadores()
        self.prs = self._cargar_palabras_reservadas()
        self.patrones_tokens = self._cargar_patrones()

        # Ordenar operadores de mayor a menor longitud
        self.ops.sort(key=len, reverse=True)

    # ---------- Métodos de carga ----------
    def _cargar_desde_archivo(self, ruta):
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                return [linea.strip() for linea in f if linea.strip()]
        except:
            return []

    def _cargar_operadores(self):
        return [op.upper() for op in self._cargar_desde_archivo(self.ruta_ops)]

    def _cargar_palabras_reservadas(self):
        return [pr.upper() for pr in self._cargar_desde_archivo(self.ruta_prs)]

    def _cargar_patrones(self):
        patrones = []
        for linea in self._cargar_desde_archivo(self.ruta_ptn):
            if ',' in linea:
                regex, tipo = linea.split(',', 1)
                patrones.append((regex.strip(), tipo.strip()))
        return patrones

    # ---------- Método principal: separar token ----------
    def separar_token(self, cTexto, separador_lexico):
        """
        Usa Separador_Lexico para obtener tokens
        """
        return separador_lexico.separar_token(cTexto)

    # ---------- Métodos auxiliares ----------
    def _es_numero(self, palabra):
        if not palabra:
            return False
        if palabra.count('.') == 1:
            p1, p2 = palabra.split('.', 1)
            return p1.isdigit() and p2.isdigit()
        return palabra.isdigit()

    def _es_identificador(self, palabra):
        if not palabra:
            return False
        if palabra[0].isalpha() or palabra[0] == "_":
            return all(c.isalnum() or c == "_" for c in palabra[1:])
        return False

    # ---------- Análisis sintáctico ----------
    def analizar_sintaxis(self, tokens):
        """
        Reglas básicas:
        - ID = NUM|ID|STR
        - No iniciar línea con NUM
        - Detectar tokens inválidos
        """
        errores = []
        i = 0
        while i < len(tokens):
            t = tokens[i]
            tipo = t['tipo']
            val = t['valor']
            linea = t['linea']

            # Token inválido
            if tipo not in ('ID','NUM','PR','OP','CADENA','STR'):
                errores.append(f"L{linea}: Token inválido '{val}'")

            # Línea inicia con número → error
            if tipo in ('NUM') and (i == 0 or tokens[i-1]['linea'] != linea):
                errores.append(f"L{linea}: No puede iniciar con número '{val}'")

            # Asignación simple: ID = NUM|ID|CADENA|STR
            if tipo == 'ID' and i+1 < len(tokens) and tokens[i+1]['valor'] == '=':
                if i+2 >= len(tokens):
                    errores.append(f"L{linea}: Falta expresión después de '='")
                else:
                    siguiente = tokens[i+2]
                    if siguiente['tipo'] not in ('ID','NUM','CADENA','STR'):
                        errores.append(f"L{linea}: Expresión inválida después de '=': '{siguiente['valor']}'")
                i += 2  # saltar '=' y siguiente token

            i += 1

        return errores
