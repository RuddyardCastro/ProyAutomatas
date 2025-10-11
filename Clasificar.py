class Separador_Lexico:
    def __init__(self):
        self.ruta_ops = r"C:\Users\Ruddyard\Desktop\ProyEnGit\archivos\Archivos de diccionario\operadores\operadores.txt"
        self.ruta_prs = r"C:\Users\Ruddyard\Desktop\ProyEnGit\archivos\Archivos de diccionario\palabras reservadas\palabrasReservadas.txt"
        self.ruta_ptn = r"C:\Users\Ruddyard\Desktop\ProyEnGit\archivos\Archivos de diccionario\patrones\patrones.txt"

        self.ops = self._cargar_operadores()
        self.prs = self._cargar_palabras_reservadas()
        self.patrones_tokens = self._cargar_patrones()
        self.ops.sort(key=len, reverse=True)

    # ---------- Métodos de carga ----------
    def _cargar_desde_archivo(self, ruta_archivo):
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
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

    # ---------- Métodos de verificación ----------
    def es_numero(self, palabra):
        if not palabra:
            return False
        if palabra[0] == '-':
            palabra = palabra[1:]
        partes = palabra.split('.')
        if len(partes) > 2:
            return False
        return all(p.isdigit() for p in partes)

    def es_identificador(self, palabra):
        if not palabra:
            return False
        if palabra[0].isalpha() or palabra[0] == '_':
            return all(c.isalnum() or c == '_' for c in palabra)
        return False

    # ---------- Separador de tokens ----------
    def separar_token(self, cTexto):
        tokens_result = []
        lineas = cTexto.splitlines()

        for num_linea, linea in enumerate(lineas, 1):
            i = 0
            while i < len(linea):
                c = linea[i]

                if c.isspace():
                    i += 1
                    continue

                # Comentarios
                if c == '#':
                    tokens_result.append({
                        'tipo': 'Comment',
                        'valor': linea[i:],
                        'linea': num_linea
                    })
                    break

                # Operadores
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

                # Cadenas entre comillas
                if c == '"':
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

                # Palabra completa
                palabra = ""
                while i < len(linea) and not linea[i].isspace() and all(
                    not linea[i:].upper().startswith(op) for op in self.ops
                ):
                    palabra += linea[i]
                    i += 1

                palabra_up = palabra.upper()

                # Palabra reservada
                if palabra_up in self.prs:
                    tokens_result.append({
                        'tipo': 'PR',
                        'valor': palabra,
                        'linea': num_linea
                    })
                    continue

                # Números e identificadores
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

                # ID genérico
                tokens_result.append({
                    'tipo': 'ID',
                    'valor': palabra,
                    'linea': num_linea
                })

        return tokens_result
