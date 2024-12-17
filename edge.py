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
import os
import pandas as pd
import numpy as np
import joblib

from fastdtw import fastdtw

from azure.cosmos import CosmosClient
from dotenv import load_dotenv
import uuid


ml_models = {}
correct_seq = {}
sensors_socket = None
actuators_socket = None

def main():
    global sensors_socket, actuators_socket

    print("Loading data required...")
    
    """ DATA """
    actual_dir = os.path.dirname(os.path.abspath(__file__))     # NO NEED TO CHANGE
    read_data(actual_dir)

    """ COMUNICATION """
    sensors_host = "192.168.1.132"                               # CHANGE
    sensors_port = 12345

    actuator_host = "192.168.1.132"                              # CHANGE
    actuator_port = 12346
   
    try:
        # exercise_container,_ = create_connection_database()
        create_connection_sensors(sensors_host, sensors_port)
        create_connection_actuators(actuator_host, actuator_port)
        
        while True:
            print("Waiting T-SHIRT to connect...")

            actuators_socket, _ = actuators_socket.accept()
            print(f"Connection established via BLUETOOTH with the ACTUATORS.")

            sensors_socket, _ = sensors_socket.accept()
            print(f"Connection established via BLUETOOTH with the SENSORS")
                
            while True:
                try:
                    data = sensors_socket.recv(4096).decode("utf-8")
                    if not data:
                        print("T-Shirt closed the connection.")
                        break

                    try:
                        message = json.loads(data)
                                
                        if "message" in message:
                            if message["message"] == "START_OF_REPETITION":
                                exercise = message["exercise"]
                                position = message["position"]
                                length = message["length"]

                                df_repetition = repetition(exercise, position, length)
                                label = rating_repetition(df_repetition, exercise, position, length)
                                # upload_database(exercise_container, df_repetition, exercise, label)
                                print("\nWAITING FOR NEXT REPETITION")


                    except json.JSONDecodeError:
                        print("Error decoding JSON messages")
                        continue

                except Exception as e:
                    print(f"Error receiving data: {e}")
                    break

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        if sensors_socket:
            sensors_socket.close()
            print("Sensor connection closed.")
        if actuators_socket:
            actuators_socket.close()
            print("Actuator connection closed.")


def read_data(script_dir):
    """Load required data"""
    global ml_models, correct_seq

    """ MACHINE LEARNING MODELS """
    ml_dir = os.path.join(script_dir, 'Data', 'Trained_Models')
    for model in os.listdir(ml_dir):
        if model.endswith('.pkl'):
            model_path = os.path.join(ml_dir, model)
            model_name = os.path.splitext(model)[0]
            ml_models[model_name] = joblib.load(model_path)

    """ CORRECTION FUNCIONALITIES DATA """
    correct_dir = os.path.join(script_dir, 'Data', 'Correction_Funcionality')
    for file_json in os.listdir(correct_dir):
        if file_json.endswith('.json'):
            file_path = os.path.join(correct_dir, file_json)
            file_name = os.path.splitext(file_json)[0]
            with open(file_path, "r") as file:
                correct_seq[file_name] = json.load(file)

    
    """
def create_connection_database():
    # Connect with the Azure Database

    load_dotenv()
    COSMOS_URI = os.getenv("COSMOS_URI")
    COSMOS_KEY = os.getenv("COSMOS_KEY")
    DATABASE_NAME = os.getenv("DATABASE_NAME")

        
    client = CosmosClient(COSMOS_URI, COSMOS_KEY)

    database = client.get_database_client(DATABASE_NAME)

    exercise_container = database.get_container_client("Pacientes_ejercicio")
    progress_container = database.get_container_client("Pacientes_progreso")

    print(f"Connection established via HTTPS with the DATABASE.")
    return exercise_container, progress_container
    """

def create_connection_sensors(host, port):
    """ Create and return a socket connection """
    global sensors_socket

    try:
        sensors_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sensors_socket.bind((host, port))
        sensors_socket.listen(1)
           
    except Exception as e:
        print(f"Error connecting: {e}")
        return None

def create_connection_actuators(host, port):
    """ Create and return a socket connection """
    global actuators_socket

    try:
        actuators_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        actuators_socket.bind((host, port))
        actuators_socket.listen(1)
           
    except Exception as e:
        print(f"Error connecting: {e}")
        return None



def repetition(exercise, position, length):
    global sensors_socket, correct_seq
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\nRepetition start received")

    df_repetition = pd.DataFrame()

    ideal_seq = correct_seq['ideal_sequences'][exercise][position]
    treshold = correct_seq['treshold'][exercise][position]

    ideal_seq_interp = interpolate(ideal_seq, length)

    i=0
    while True:
        try:
            data = sensors_socket.recv(4096).decode('utf-8')
            if not data:
                break

            try:
                message = json.loads(data)
                if "message" in message and message["message"] == "END_OF_REPETITION":
                    print("\nRepetition end received")
                    return df_repetition

                df_message = pd.DataFrame([message])
                df_repetition = pd.concat([df_repetition, df_message], ignore_index=True)

                print(f"\nExercise data: {message}")
                
                if len(df_repetition)%10==0 or len(df_repetition)==length:
                    ideal_seq_interp_frag = {key: value[i*10:len(df_repetition)] for key, value in ideal_seq_interp.items()}
                    detection_incorrect_movement(df_repetition[i*10:], ideal_seq_interp_frag, treshold)
                    i+=1

            except json.JSONDecodeError:
                print("Error decoding JSON message")
                continue
        
        except Exception as e:
            print(f"Error receiving data: {e}")



def interpolate(original_sample, ideal_length):
    interpolated_data = {}
    for key, value in original_sample.items():
        ideal_index = np.linspace(0, len(value) - 1, ideal_length)
        interpolated_data[key] = np.interp(ideal_index, np.arange(len(value)), value)
    
    return interpolated_data


def detection_incorrect_movement(df, ideal_seq, treshold):   
    incorrect = []
    for column_name, column_data in df.items():
        distance1, _ = fastdtw(column_data, ideal_seq[column_name])
        if distance1 > treshold[column_name]:
            incorrect.append(column_name)

    if incorrect:
        send_notice_actuators({joint: 1 for joint in incorrect})

def send_notice_actuators(notice):
    global actuators_socket

    json_data = json.dumps(notice)
    print(f"\nSending data to actuators: {json_data}")
    actuators_socket.send(json_data.encode('utf-8'))



def rating_repetition(df_repetition, gesture, position, length):
    global ml_models

    possible_positions = ['C', 'S', 'W']
    df = pd.DataFrame({'Length': [length], 'Position': [position]})
    df['Position'] = pd.Categorical(df['Position'], categories=possible_positions)
    df = pd.get_dummies(df, columns=['Position'])
    
    stats = {}
    for col in df_repetition.columns:
        stats[f'{col}_mean'] = df_repetition[col].mean()
        stats[f'{col}_std'] = df_repetition[col].std()
        stats[f'{col}_min'] = df_repetition[col].min()
        stats[f'{col}_max'] = df_repetition[col].max()
        stats[f'{col}_range'] = stats[f'{col}_max'] - stats[f'{col}_min']
        stats[f'{col}_first'] = df_repetition[col].iloc[0]
        stats[f'{col}_last'] = df_repetition[col].iloc[-1]

    stats_df = pd.DataFrame([stats])
    df = pd.concat([df, stats_df], axis=1)

    label = ml_models[gesture].predict(df)
    label_str = {1: 'Correct',
                 0: 'Incorrect'}
    print(f'\nLABEL {label[0]}: {label_str[label[0]]}')
    return label[0]


def upload_database(exercise_container, df, exercise, label):
    try:
        data = {
            'id': str(uuid.uuid4()),
            'idPatient': "001",
            'exercise': exercise,
            'label' : int(label),
            'frames' : df.to_dict(orient='records')
        }

        exercise_container.create_item(body=data)
        print("\nItem added to container Patients_exercise.")

    except Exception as e:
        print(f"Error uploading data: {e}")




if __name__ == "__main__":
    print("\n\nEDGE SIMULATOR")
    main()