# ST0263-Entrega1
Trabajo creado para realizar conexiones TPC/IP a traves de web sockets creando un cliente para hacer peticiones para diferentes URLs, el client recibira los datos del servidor por el puerto que se le envie y guardara el tipo de archivo que se le envie y su contenido en la carpeta UPLOAD que se borrara después de finalizar el programa.

# ¿Cómo usarlo?
Se debe de utilizar python 3.X para ejecutarlo y se debe de tener las dependencias de BeautifulSoup y socket que se instalan de esta forma:
```Shell
pip install socket 
pip install bs4
```
## Ejecución en terminal
yacurl.py debe de ser ejecutado desde una terminal y pasarle los parametros de la URL para conectarse, opcionalmente se le pueden agregar el puerto y el metodo por el cual se desea acceder a la página.

**IMPORTANTE**
  - Si no se pasa un puerto, por defecto se pasara el puerto: **80**
  - Si no se pasa un metodo, por defecto se pasara el metodo: **GET**

### Usage
```console
$ python yacurl.py URL (OPTIONAL) --PORT (OPTIONAL) /METHOD
```

### Examples
```console
$ python yacurl.py www.google.com --80 /GET
```
