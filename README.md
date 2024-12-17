**Copyright Notice**

All rights reserved. This material, including but not limited to text, images, code, and any other content, is protected under international copyright laws and other intellectual property regulations.

Reproduction, distribution, public communication, transformation, or any other use of the content, in whole or in part, for commercial purposes is strictly prohibited without prior written consent from the copyright holder.

This text is the intellectual property of Group 2 (SRTS): Carlos Rubio Hernán, Miguel Ángel Arias González, Diego Fernández Gómez, Sonia Menéndez Menéndez, from the subject of 'Proyectos en Ingeniería de Datos y Sistemas' of the degree 'Grado en Ingeniería de Datos y Sistemas' of the 'Universidad Politécnica de Madrid'.

For inquiries regarding permissions or licenses, please contact the copyright holder: srtsdemo@gmail.com

© [2024] Group 2 (SRTS). All rights reserved.

## Files Description
Simulation/
├── Data/
│   ├── Correction_Funcionality/
│   │   ├── ideal_sequences.json : ideal sequences for all gestures-positions-joint axes
│   │   ├── treshold.json : treshold for all gestures-positions-joint axes
│   ├── Preprocessed/
│   │   ├── data.csv : all dataset data in a single file
│   │   ├── data_shoulder.csv : all shoulder gestures data with all columns containing information
│   │   ├── data_shoulder_active.csv : all shoulder gestures data but the non-interacting sensors are turned off
│   ├── Raw_Data_Simplified/
│   │   └── ... .txt : all dataset files from the simplified model of the IntelliRehabDS (IRDS) dataset
│   ├── Trained_Models/
│   │   ├── Shoulder_Abduction_Left.pkl : trained model of gesture 'Shoulder_Abduction_Left'
│   │   ├── Shoulder_Abduction_Right.pkl : trained model of gesture 'Shoulder_Abduction_Left'
│   │   ├── Shoulder_Flexion_Left.pkl : trained model of gesture 'Shoulder_Abduction_Left'
│   │   ├── Shoulder_Flexion_Right.pkl : trained model of gesture Shoulder_Flexion_Right'
│   │   └── Shoulder_Forward_Elevation.pkl : trained model of gesture 'Shoulder_Forward_Elevation'
├── Notebooks/
│   ├── Correction_Funcionality : steps of the creation of the correction part
│   ├── Machine_Learning : steps of the creation of the ML models
│   └── Preprocessing : preprocessing of the raw data
├── actuators.py : simulator of the actuators
├── edge.py : simulator of the edge
├── sensors.py : simulator of the sensors
└── env

Because of maximum file size on GitHub reasons, neither the Data folder nor the Notebooks folder could be uploaded. Both can be found in: https://drive.google.com/drive/folders/11haufJA0F9EgCLilFaLO8MBPACXaZtE7?usp=sharing 

As actions before running the simulator:
- You must download the Data folder from: https://drive.google.com/drive/folders/19tgrP-48tzInE2GnGRZ_yQvTyYgT38G7?usp=sharing
- You must change the IP of all scripts to the IP of the computer where you want to run the simulator.

Note: you must have all the python libraries used in these 3 files installed.

For full functionality
- Insert your database credentials in the 'env' file, in order to upload the files to the cloud.

To execute this simulator, you must enter in different terminals, to the folder where the 'Simulation' folder is located.
In each of those terminals, you must execute each of the python codes in that folder (python ____.py), where ___ is the name of the file.
Starting first with the edge.py (since it is the server), and continuing indistinctly with the other two (sensors.py and actuators.py).

