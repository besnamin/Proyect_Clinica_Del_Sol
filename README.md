# Proyect_Clinica_Del_Sol
NRC: 1192 T-D2
GRUPO: 20
EQUIPO No : 5

Integrantes:
BENJAMIN ANTONIO LIZARAZO SIERRA
JIMENA CHARLES JIMENEZ
RAFAEL SANCHEZ AYALA
JEINER BAEZ MANTILLA
ANDRES FERNANDO TUNUBALA TUNUBALA

1. CREAMOS UN ENTORNO ENV
2. INSTALAMOS FLASK
3. INSTALAMOS FLASK-WTF
4. INSTALAMOS YAGMAIL
5. CREAMOS LAS CARPETAS STATIC Y TEMPLATES
6. CREAMOS UNA PLANTILLA (layout) QUE SIRVE DE PANTALLA INICIAL Y DE GUIA PARA LOS FORMULARIOS
7. CREAMOS UNA CLASE FORMS DONDE TENEMOS LOS FORMULARIOS Y CAMPOS QUE VAMOS A UTILIZAR
8. CREAMOS LAS VISTAS REGISTRO Y SESION, DONDE VAN A IR NUESTROS FORMULARIOS
9. CREAMOS NUESTRA HOJA DE ESTILOS PARA DARLE FORMA A NUESTRAS VISTAS
10. EN NUESTRA CLASE APP DEFINIMOS LAS RUTAS Y LOS METODOS.
11. Creamos los archivos html de las vitas del paciente, para pedir citas, realizar comentatios y cerrar sesion
12. creamos 2 formularios nuevos para relizar las citas y hacer comentarios
13. En nuestar app.py definimos las nuevas rutas que creamos y los metodos controladores
14. En nuestra hoja de estilos le dimos forma a la pagina de inicio del paciente cuando inicie sesion
15. Creamos mas archivos html para las vistas del medico y del administrados y ademas las vistas necesarias para ver las citas e insertar las observaciones
16. En nuestro archico app.py creamos los metodos y rutas de acceso para todas las vistas html 
17. Creamos una carpeta db en la cual ingresaremos una tabla sqlite con las tablas de administrador,pacientes,medicos y citas
18. Creamos un archivo db.py en el cual haremos la conexion con nuestra base de datos, en esta archivo estaran las funciones de conectar, insertar y select que serviran para interaccionar con nuestra base de datos.
19. creamos un archivo models.py en el cual tendremos los creamos las clases usuario y  citas con sus respectivos metodos para autenticar, insertar y cargar datos desde la base de datos.
20. En nuestros metodos controladores creamos objetos de tipo usuario o citas segun sea el caso para cargar los datos del formulario y poder insertar, seleccionar, eliminar o segun sea lo requerido en la base de datos.
21. Para guardar las contraseñas en nuestra base de datos y no viajen en texto plano usamos generate_password_hash para que nuestras contraseñas se encripten y viajen seguras a la base de datos, y check_password_hash para cuando necesitemos comprobar que una contraseña ingresada coincide con lo que se guardo de forma encriptada en la base de datos.
22. Para proteger el contenido y los que cada usuario segun sea su rol puede ver y acceder creamos las sesiones , con decoradores loguin_required, loguin_required_medico , loguin_required_admin, esto lo hacemos accediendo a la base de datos con una funcion cargar nombre_usuario
23. Ahora agregamos a cada vista el loguin_required segun el caso y con esto nos haceguramos proteger lo que se puede acceder y ademas mantenemos la sesion hasta que el usuario le de a salir que cerrara la sesion y regresaremos a la pagina d einicio.
24. En nuestro layout segun sea el g.user se mostraran varios menus diferentes e imagenes diferentes.
25. creamos en la carpeta static una carpeta js y ahi creamos un archivo javascript para verificar la informacion del lado del cliente antes de que los formularios se reendericen y viajen al servidor.
26. Atraves del comando pip freeze > requirements.txt que cargara todas las dependencias necesarias para el funcionamiento de nuestra aplicacion, esto nos servira a la hora de cargar nuestra aplicacion a la nube.
27. Subimos nuestra aplicacion a pythonanywhere y obtenemos el siguiente link para acceder a nuestra aplicacion:
https://clinicadelsol.pythonanywhere.com/
