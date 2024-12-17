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
import time
import os
import pandas as pd
import ast


df = None
repetitions = {}
edge_socket = None

def main():
    global edge_socket

    print("Loading data simulation...")
    
    """ DATA """
    actual_dir = os.path.dirname(os.path.abspath(__file__))     # NO NEED TO CHANGE
    read_data(actual_dir)

    """ COMUNICATION """
    host = "192.168.1.132"                                      # CHANGE
    port = 12345
    
    try:
        create_connection(host, port)

        if edge_socket:
            print(f"Connection established via BLUETOOTH with the MOBILE")
            press_any_key_to_start('SIMULATION IS READY TO START\nLet´s start')

            sim = input("Do you want to simulate? (Y/N): ").strip().upper()

            while sim=='Y':

                exercise = get_exercise()
                position = get_position()
                id = get_id(exercise, position)
                filter_df = simulated_exercises(exercise, position, id)

                print("\n\nYOU ARE GOING TO START YOUR DAILY ROUTINE:")
                print(f"LET'S DO {len(filter_df)} REPETITIONS OF {exercise.upper()}")
                press_any_key_to_start('ARE YOU READY TO START?')

                name_repet = sorted([key for key in repetitions if key.startswith(f'{id}-{exercise}-{position}')], key=lambda x: int(x.split('-')[-1]))
                n=1
                for name in name_repet:
                    print(f"REPETITION {n}")

                    generate_repetition(repetitions[name], exercise, position)
                    n+1

                    if n==len(filter_df)-1:
                        press_any_key_to_start('\nEXERCISE FINISHED.\n')
                    else:
                        n+1
                        press_any_key_to_start('\nREPETITION FINISHED.\nWAITING FOR START NEXT REPETITION\n')

                
                sim = input("Do you want to continue simulating? (Y/N): ").strip().upper()
        
        else:
            print("Unable to establish connection with the MOBILE")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if edge_socket:
            edge_socket.close()
            print("Connection closed")



def read_data(script_dir):
    """Load simulation data"""
    global df
    global repetitions

    """"""" DATAFRAME SET """""""
    df_file = 'data_shoulder_active.csv'
    df_dir = os.path.join(script_dir, 'Data', 'Preprocessed', df_file)


    if not os.path.isfile(df_dir):
        raise FileNotFoundError(f"The file '{df_file}' was not found in the directory '{df_dir}'.")
        
    try:
        df = pd.read_csv(df_dir, delimiter=';')
    except Exception as e:
        raise ValueError(f"Error reading the file '{df_file}': {e}")
    
    """Data Type Correction"""
    df['GestureLabel'] = df['GestureLabel'].astype('category')
    df['Position'] = df['Position'].astype('category')

    col_metadata = ['SubjectID', 'DateID', 'GestureLabel', 'RepetitionNumber', 'CorrectLabel', 'Position', 'Length']
    col_mov = df.loc[:, ~df.columns.isin(col_metadata)].columns

    for column in col_mov:
        df[column] = df[column].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)



    """"""" SET OF REPETITIONS """""""
    gestures = {
    '2': 'Shoulder_Flexion_Left',
    '3': 'Shoulder_Flexion_Right',
    '4': 'Shoulder_Abduction_Left',
    '5': 'Shoulder_Abduction_Right',
    '6': 'Shoulder_Forward_Elevation'}

    position = {
    'stand' : 'S',
    'chair' : 'C',
    'wheelchair' : 'W',
    'sit' : 'C',
    'Stand-frame' : 'S'}

    sensors = [f"{sensor}_{axis}" for sensor in ['SpineBase', 'SpineMid', 'Neck', 'Head', 'ShoulderLeft', 'ElbowLeft', 'WristLeft', 'HandLeft', 'ShoulderRight', 'ElbowRight', 'WristRight', 'HandRight', 'HipLeft', 'KneeLeft',
               'AnkleLeft', 'FootLeft', 'HipRight', 'KneeRight', 'AnkleRight', 'FootRight', 'SpineShoulder', 'HandTipLeft', 'ThumbLeft', 'HandTipRight', 'ThumbRight'] for axis in ['X', 'Y', 'Z']]
    sensNoActive = [f"{sensor}_{axis}" for sensor in ['SpineBase', 'HipLeft', 'KneeLeft', 'AnkleLeft', 'FootLeft', 'HipRight', 'KneeRight', 'AnkleRight', 'FootRight'] for axis in ['X', 'Y', 'Z']]


    data_dir = os.path.join(script_dir, 'Data', 'Raw_Data_Simplified')
    for file in os.listdir(data_dir):
        file_path = os.path.join(data_dir, file)

        if file.endswith('.txt'):
            no_extension = os.path.splitext(file)[0]

            try:
                SubjectID, DateID, GestureLabel, RepetitionNumber, CorrectLabel, Position = no_extension.split("_")

                if CorrectLabel != '3' and GestureLabel in ['2', '3', '4', '5', '6']:
                    GestureLabel = gestures[GestureLabel]
                    Position = position[Position]

                    try:
                        df_rep = pd.read_csv(file_path, header=None, names=sensors)                       
                        df_rep = df_rep.astype(float)
                        df_rep[sensNoActive] = None

                        repetitions[f'{SubjectID}-{GestureLabel}-{Position}-{RepetitionNumber}'] = df_rep

                    except UnicodeDecodeError:
                        print(f"File could not be read: {file}")
                        continue

            except ValueError:
                print(f'Error processing file: {file}')
                continue


def create_connection(host, port):
    """ Create and return a socket connection """
    global edge_socket

    try:
        edge_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        edge_socket.connect((host, port))
    
    except Exception as e:
        print(f"Error connecting: {e}")
        return None
    

def get_exercise():
    gestures = {
    '1': 'Shoulder_Flexion_Left',
    '2': 'Shoulder_Flexion_Right',
    '3': 'Shoulder_Abduction_Left',
    '4': 'Shoulder_Abduction_Right',
    '5': 'Shoulder_Forward_Elevation'}

    while True:
        print("\n\nWhich exercise do you want to perform? (1-5)")
        print("1. Shoulder Flexion Left")
        print("2. Shoulder Flexion Right")
        print("3. Shoulder Abduction Left")
        print("4. Shoulder Abduction Right")
        print("5. Shoulder Forward Elevation")
        exercise_str = input("Enter an option: ")
                
        if exercise_str in gestures:
            exercise = gestures[exercise_str]
            return exercise

        else:
            print("Invalid option. Please try again.")

def get_position():
    positions = {
    '1': 'S',
    '2': 'C',
    '3': 'W'}

    while True:
        print("\n\nIn which position you are going to perform the exercise? (1-3)")
        print("1. Standing")
        print("2. Sitting on a chair")
        print("3. Wheelchair-bound")

        position_str = input("Enter an option: ")
                
        if position_str in positions:
            position = positions[position_str]
    
            return position

        else:
            print("Invalid option. Please try again.")
    
def get_id(exercise, position):
    global df

    filtered_df = df[(df['GestureLabel'] == exercise) & (df['Position'] == position)]
    id_counts = filtered_df.groupby(['SubjectID']).size().reset_index(name='RepetitionCount')
    id_counts = id_counts.sort_values(by='SubjectID')

    print("\n\nWhich ID do you want to simulate?")
    print(id_counts.to_string(index=False))

    while True:
        id_str = input("Enter an option: ")

        try:
            id = int(id_str)

            if id in df['SubjectID'].values: 
                return id

        except ValueError:
            print("Invalid option. Please try again.")     
    

def simulated_exercises(exercise, position, id):
    global df

    filtered_df = df[
    (df['Position'] == position) & 
    (df['GestureLabel'] == exercise) & 
    (df['SubjectID'] == id)]

    metadata = ['SubjectID', 'DateID', 'GestureLabel','RepetitionNumber', 'CorrectLabel', 'Position', 'Length']
    filtered_df = filtered_df.loc[:, ~filtered_df.columns.isin(metadata)]

    return filtered_df

def press_any_key_to_start(sentence):
    input(f'\n{sentence}')
    os.system('cls' if os.name == 'nt' else 'clear')



def generate_repetition(data, exercise, position):
    """Generate the data of a repetition"""
    global edge_socket

    send_data({"message": "START_OF_REPETITION", "exercise": exercise, "position": position, "length":len(data)})
    messages = ["READY", "STEADY", "GO"]
    for message in messages:
        time.sleep(1)
        print(message)
    
    data = data.dropna(axis=1, how='all')
    for _, row in data.iterrows():
        frame = row.to_dict()
        send_data(frame)
        time.sleep(1/2) #1/30
        
    send_data({"message": "END_OF_REPETITION"})


def send_data(data):
    """Send data to the edge"""
    global edge_socket

    json_data = json.dumps(data)
    print(f"\nSending data: {json_data}\n")
    edge_socket.send(json_data.encode('utf-8'))



if __name__ == "__main__":
    print("\n\n\nSENSOR SIMULATOR")
    main()
