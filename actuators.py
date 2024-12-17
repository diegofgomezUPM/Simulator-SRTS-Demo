"""
**Copyright Notice**

All rights reserved. This material, including but not limited to text, images, code, and any other content, is protected under international copyright laws and other intellectual property regulations.

Reproduction, distribution, public communication, transformation, or any other use of the content, in whole or in part, for commercial purposes is strictly prohibited without prior written consent from the copyright holder.

This text is the intellectual property of Group 2 (SRTS): Carlos Rubio Hernán, Miguel Ángel Arias González, Diego Fernández Gómez, Sonia Menéndez Menéndez, from the subject of 'Proyectos en Ingeniería de Datos y Sistemas' of the degree 'Grado en Ingeniería de Datos y Sistemas' of the 'Universidad Politécnica de Madrid'.

For inquiries regarding permissions or licenses, please contact the copyright holder: srtsdemo@gmail.com

© [2024] Group 2 (SRTS). All rights reserved.
"""

import socket
import json


edge_socket = None

def main():
    global edge_socket

    """ COMUNICATION """
    host = "192.168.1.132"                      # CHANGE
    port = 12346

    try:
        create_connection(host, port)
        
        if edge_socket:
            print(f"Connection established via BLUETOOTH with the MOBILE")

            while True:
                try:
                    data = edge_socket.recv(4096).decode('utf-8')
                    if not data:
                        break

                    try:
                        message = json.loads(data)
                        correct(message)
            
                    except json.JSONDecodeError:
                        print("Error decoding JSON message")
                        continue
                
                except Exception as e:
                    print(f"Error receiving data: {e}")

        else:
            print("Unable to establish connection with the MOBILE")     

    except Exception as e:
            print(f"An error occurred: {e}")

    finally:
        if edge_socket:
            edge_socket.close()
            print("Connection closed")


def create_connection(host, port):
    """ Create and return a socket connection """
    global edge_socket

    try:
        edge_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        edge_socket.connect((host, port))
           
    except Exception as e:
        print(f"Error connecting: {e}")
        return None


def correct(message):
    print("\n\nACTUATORS ACTIVATING ON")
    for key in message.keys():
        joint, _ = key.split("_")
        print(f'{joint}')

if __name__ == "__main__":
    print("\n\n\nACTUATOR SIMULATOR")
    main()
