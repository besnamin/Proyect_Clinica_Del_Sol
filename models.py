
import db

from werkzeug.security import generate_password_hash, check_password_hash
 
        
      
#Clase para manejar los usuarios
class paciente():
    usuario=''
    nombre=''
    documento=''
    correo=''
    contrasena=''
    

    def __init__(self, pusuario,pnombre,pdocumento,pcorreo, pcontrasena) :
        self.usuario = pusuario
        self.nombre = pnombre
        self.documento = pdocumento
        self.correo = pcorreo
        self.contrasena = pcontrasena
        

        #Classmethod para crear instancias de usuario desde la bd.
    @classmethod
    def cargar(cls, p_usuario):
        sql = "SELECT usuario, nombre, documento,correo FROM pacientes WHERE usuario = ?;" 
        obj = db.ejecutar_select(sql, [p_usuario])
        if obj:
            if len(obj)>0:
                return cls(obj[0]["usuario"], obj[0]["nombre"],obj[0]["documento"], obj[0]["correo"], '******')

        return None

    @classmethod
    def cargar2(cls, p_usuario):
        sql = "SELECT usuario, nombre, documento,correo FROM medicos WHERE usuario = ?;" 
        obj = db.ejecutar_select(sql, [p_usuario])
        if obj:
            if len(obj)>0:
                return cls(obj[0]["usuario"], obj[0]["nombre"],obj[0]["documento"], obj[0]["correo"], '******')

        return None

    @classmethod
    def cargaradmin(cls, p_usuario):
        sql = "SELECT usuario, nombre, documento,correo FROM administrador WHERE usuario = ?;" 
        obj = db.ejecutar_select(sql, [p_usuario])
        if obj:
            if len(obj)>0:
                return cls(obj[0]["usuario"], obj[0]["nombre"],obj[0]["documento"], obj[0]["correo"], '******')

        return None
    
    
    #Metodo para insertar el usuario en la base de datos
    def insertar(self):
        sql = "INSERT INTO pacientes (usuario, nombre, documento, correo, contrasena) VALUES (?, ?, ?, ?, ?);"
        #generate_password_hash crea un hash seguro para almacenar la contraseña del usuario en la bd 
        hashed_pwd = generate_password_hash(self.contrasena, method='pbkdf2:sha256', salt_length=32)
        afectadas = db.ejecutar_insert(sql, [self.usuario, self.nombre, self.documento, self.correo, hashed_pwd])
        return (afectadas>0)

    def insertar2(self):
        sql = "INSERT INTO medicos (usuario, nombre, documento, correo, contrasena) VALUES (?, ?, ?, ?, ?);"
        #generate_password_hash crea un hash seguro para almacenar la contraseña del usuario en la bd 
        hashed_pwd = generate_password_hash(self.contrasena, method='pbkdf2:sha256', salt_length=32)
        afectadas = db.ejecutar_insert(sql, [self.usuario, self.nombre, self.documento, self.correo, hashed_pwd])
        return (afectadas>0)

    #Metodo para verificar el usuario contra la base de datos
    def autenticar(self):
        #Este query es inseguro porque puede permitir una inyección SQL
        #sql = "SELECT * FROM usuarios WHERE usuario = '" + self.usuario + "' AND contrasena = '"  + self.contrasena + "';"    
        #Para mitigar usamos comandos SQL parametrizados
        sql = "SELECT * FROM pacientes WHERE usuario = ?;"
        obj = db.ejecutar_select(sql, [ self.usuario ])
        if obj:
            if len(obj) >0:
                #Agregamos la invocación al metodo check_password_hash
                #para verificar el password digitado contra el hash seguro almacenado en bd.
                if check_password_hash(obj[0]["contrasena"], self.contrasena):
                    return True
        
        return False

    def autenticar2(self):
        #Este query es inseguro porque puede permitir una inyección SQL
        #sql = "SELECT * FROM usuarios WHERE usuario = '" + self.usuario + "' AND contrasena = '"  + self.contrasena + "';"    
        #Para mitigar usamos comandos SQL parametrizados
        sql = "SELECT * FROM medicos WHERE usuario = ?;"
        obj = db.ejecutar_select(sql, [ self.usuario ])
        if obj:
            if len(obj) >0:
                #Agregamos la invocación al metodo check_password_hash
                #para verificar el password digitado contra el hash seguro almacenado en bd.
                if check_password_hash(obj[0]["contrasena"], self.contrasena):
                    return True
        
        return False

    def autenticar3(self):
        #Este query es inseguro porque puede permitir una inyección SQL
        #sql = "SELECT * FROM usuarios WHERE usuario = '" + self.usuario + "' AND contrasena = '"  + self.contrasena + "';"    
        #Para mitigar usamos comandos SQL parametrizados
        sql = "SELECT * FROM administrador WHERE usuario = ?;"
        obj = db.ejecutar_select(sql, [ self.usuario ])
        if obj:
            if len(obj) >0:
                #Agregamos la invocación al metodo check_password_hash
                #para verificar el password digitado contra el hash seguro almacenado en bd.
                if check_password_hash(obj[0]["contrasena"], self.contrasena):
                    return True
        
        return False

    def cargar_nombre(self):
        sql = "SELECT nombre FROM medicos  WHERE usuario = ?;"
        return db.ejecutar_select(sql, [self.usuario])

    @classmethod
    def cargar_nombre2(cls, p_usuario):
        sql = "SELECT nombre FROM medicos WHERE usuario = ?;" 
        obj = db.ejecutar_select(sql, [p_usuario])
        if obj:
            if len(obj)>0:
                return cls(obj[0]["nombre"])

        return None

    @classmethod
    def cargar_nombre3(cls, p_usuario):
        sql = "SELECT usuario, nombre, documento,correo FROM pacientes WHERE usuario = ?;" 
        obj = db.ejecutar_select(sql, [p_usuario])
        if obj:
            if len(obj)>0:
                return cls(obj[0]["usuario"], obj[0]["nombre"],obj[0]["documento"], obj[0]["correo"], '******')

        return None

    @classmethod
    def cargar3(cls, p_usuario):
        sql = "SELECT nombre FROM medicos WHERE usuario = ?;" 
        return db.ejecutar_select(sql, [p_usuario])
        



class citas():
    usuario=''
    paciente=''
    doctor=''
    fecha=''
    observacion=''
    calificacion=''

    def __init__(self, pusuario, ppaciente, pdoctor, pfecha, pobservacion,pcalificacion):
        self.usuario = pusuario
        self.paciente = ppaciente
        self.doctor = pdoctor
        self.fecha = pfecha
        self.observacion = pobservacion
        self.calificacion = pcalificacion

    @classmethod
    def cargar2(cls, pusuario):
        sql = "SELECT * FROM citas WHERE usuario = ?;"
        resultado = db.ejecutar_select(sql, [ pusuario ])
        if resultado:
            if len(resultado)>0:
                return cls(resultado[0]["usuario"], 
                resultado[0]["paciente"], resultado[0]["doctor"],
                resultado[0]["fecha"], resultado[0]["observaciones"], resultado[0]["calificacion"])
        
        return None

    
    @classmethod
    def cargar(cls, pfecha):
        sql = "SELECT * FROM citas WHERE fecha = ?;"
        resultado = db.ejecutar_select(sql, [ pfecha ])
        if resultado:
            if len(resultado)>0:
                return cls(resultado[0]["usuario"], 
                resultado[0]["paciente"], resultado[0]["doctor"],
                resultado[0]["fecha"], resultado[0]["observaciones"], resultado[0]["calificacion"])
        
        return None
    
    def insertar3(self):
        sql = "INSERT INTO citas (usuario, paciente, doctor, fecha) VALUES (?,?,?,?);"
        afectadas = db.ejecutar_insert(sql, [ self.usuario, self.paciente, self.doctor, self.fecha])
        return ( afectadas > 0 )

    def eliminar(self):
        sql = "DELETE mensajes WHERE id = ?;"
        afectadas = db.ejecutar_insert(sql, [ self.usuario ])
        return ( afectadas > 0 )

    def responder(self):
        sql = "UPDATE citas SET calificacion = ?  WHERE fecha= ?;"
        afectadas = db.ejecutar_insert(sql, [ self.calificacion, self.fecha ])
        return ( afectadas > 0 )

    

    def responder2(self):
        sql = "UPDATE citas SET observaciones = ?  WHERE fecha= ?;"
        afectadas = db.ejecutar_insert(sql, [ self.observacion, self.fecha ])
        return ( afectadas > 0 )

    
    def listado2(self):
        sql = "SELECT * FROM citas  WHERE doctor = ?;"
        return db.ejecutar_select(sql, [self.doctor])

    def listado(self):
        sql = "SELECT * FROM citas  WHERE usuario = ?;"
        return db.ejecutar_select(sql, [self.usuario])

    @staticmethod
    def listado3():
        sql = "SELECT * FROM citas ORDER BY id;"
        return db.ejecutar_select(sql, None)

    @staticmethod
    def listado4():
        sql = "SELECT * FROM pacientes ;"
        return db.ejecutar_select(sql, None)

    @staticmethod
    def listado5():
        sql = "SELECT * FROM medicos ;"
        return db.ejecutar_select(sql, None)
       
    
    @staticmethod
    def listado_paginado(filas_por_pagina, numero_pagina):
        #Utiliza la sentencia LIMIT para extraer los registros paginados.
        sql = "SELECT * FROM mensajes ORDER BY id LIMIT " + str((numero_pagina-1)*filas_por_pagina) + ", " + str(filas_por_pagina) + ";"
        return db.ejecutar_select(sql, None)