from bs4 import BeautifulSoup # Parser para la response del HTML
import os # Para crear el directorio donde se suben los archivos
import sys # Para recibir los argumentos del sistema
import socket # Liberia para crear el cliente para hacer la petición HTTPs
import shutil # Borra arbol de directorios


def client_socket(URL:str, PORT:int = 80, method:str = 'GET') -> str:
    pivote = URL.find('/')
    if pivote == -1:
        target_host = URL
        action = '/'
    else:
        target_host = URL[0:pivote]
        action = URL[pivote:]
    
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        client.settimeout(3)

        # connect the client 
        client.connect((target_host,PORT))

        # send some data 
        request = "%s %s HTTP/1.1\r\nHost:%s\r\nConnection: close\r\n\r\n" % (method, action, target_host)


        print(f'''HTTP-SEND(REQUEST):\n{request}''')
        


        client.sendall(request.encode())  
        
        # receive some data 
        response = b""
        try:
            while True:
                chunk = client.recv(4096)
                if len(chunk) == 0:     # No more data received, quitting
                    break
                response = response + chunk
        except socket.timeout as e:
            print('Se acabo el tiempo de recibir')

        http_response = repr(response)
        #http_response_len = len(http_response)
        
        #display the response
        #print("[RECV] - length: %d" % http_response_len)
        request_file = '.html'
        if action != '/':
            action = action.split('/')
            request_file = action[-1]
            pivote = request_file.find('.')
            if pivote != -1:
                request_file = request_file[pivote:]

        return http_response, request_file


    except Exception as error:
        raise Exception(error)
    finally:
        client.close()


def decoficador_http(http_response:str, file_type:str) -> None:
    http_response = http_response.strip().split('\\r\\n')
    print('HTTP-RESPONSE:')
    print(http_response[0][2:])
    for item in http_response[1:-1]:
        print(item)
    html = http_response[-1][0:-1].split('\\n')

    html_parser = ''
    file = open(f'UPLOAD/request.html','w')
    for item in html:
        html_parser = html_parser + item
        

    soup = BeautifulSoup(html_parser, 'html.parser')

    prettify_string = soup.prettify()
    print(prettify_string)
    file.write(prettify_string)
    file.close()


def create_folder() -> None:
    exec_folder = str(__file__)
    exec_folder = exec_folder[0 : exec_folder.find('yacurl.py')]
    os.mkdir(exec_folder + 'UPLOAD')


def delete_folder() -> None:
    exec_folder = str(__file__)
    exec_folder = exec_folder[0 : exec_folder.find('yacurl.py')]
    shutil.rmtree(exec_folder + 'UPLOAD')


if __name__ == "__main__":
    len_args = len(sys.argv)
    if len_args < 2 or len_args > 5:
        print("Example: python yacurl.py www.google.com --80 /GET")
        sys.exit('Usage: python yacurl.py URL(SIN el http(s)://) (OPTIONAL: --PORT DEFAULT: 80) (OPTIONAL: /METHOD DEFAULT: GET)')

    try:
        try:    
            create_folder() # Carpeta donde se guardara las paginas y archivos de yacurl
        except:
            print('La carpeta no se ha borrado!')
        
        URL = sys.argv[1].strip()
        if URL.startswith('http'):
            sys.exit('No se puede enviar el HTTP o HTTPS en la URL')

        http_response = None
        file_type = None
        if len_args == 2:
            http_response, file_type = client_socket(URL = URL)
        elif len_args == 3:
            parameter = sys.argv[2]
            if parameter.startswith('--'):
                PORT = int(parameter.replace('--','').strip())
                http_response, file_type = client_socket(URL = URL, PORT = PORT)
            else:
                method = parameter.replace('/','').strip()
                http_response, file_type = client_socket(URL = URL, method = method)

        elif len_args == 4:
            PORT = int(sys.argv[2].replace('--','').strip())
            method = sys.argv[3].replace('/','').strip()
            
            http_response, file_type = client_socket(URL = URL, PORT = PORT, method = method)

        decoficador_http(http_response = http_response, file_type = file_type)

    except Exception as e:
        print('Error: ' + str(e))
    finally:
        input('Presione Enter para salir del programa y borrar la carpeta de archivos...')
        delete_folder() # Elimina todas las carpetas creadas!
