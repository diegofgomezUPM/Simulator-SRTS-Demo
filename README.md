# Simulation Project

## **Copyright Notice**

All rights reserved. This material, including but not limited to text, images, code, and any other content, is protected under international copyright laws and other intellectual property regulations.

Reproduction, distribution, public communication, transformation, or any other use of the content, in whole or in part, for commercial purposes is strictly prohibited without prior written consent from the copyright holder.

This text is the intellectual property of **Group 2 (SRTS)**: Carlos Rubio Hernán, Miguel Ángel Arias González, Diego Fernández Gómez, Sonia Menéndez Menéndez, from the subject of *'Proyectos en Ingeniería de Datos y Sistemas'* of the degree *'Grado en Ingeniería de Datos y Sistemas'* of the *'Universidad Politécnica de Madrid'*.

For inquiries regarding permissions or licenses, please contact the copyright holder: **srtsdemo@gmail.com**

© 2024 Group 2 (SRTS). All rights reserved.

---

## **Directories and Files**

### Data
It contains all the data used in the project, organized in different subfolders:

- **Correction_Funcionality**
  - `ideal_sequences.json`: ideal sequences for all gestures-positions-joint axes.
  - `treshold.json`: treshold for all gestures-positions-joint axes.

- **Preprocessed**
  - `data.csv`: all dataset data in a single file.
  - `data_shoulder.csv`: all shoulder gestures data with all columns containing information.
  - `data_shoulder_active.csv`: all shoulder gestures data but the non-interacting sensors are turned off.

- **Raw_Data_Simplified**
  - `... .txt`: all dataset files from the simplified model of the IntelliRehabDS (IRDS) dataset.

- **Trained_Models**
  - `Shoulder_Abduction_Left.pkl`: trained model of gesture 'Shoulder_Abduction_Left'.
  - `Shoulder_Abduction_Right.pkl`: trained model of gesture 'Shoulder_Abduction_Right'.
  - `Shoulder_Flexion_Left.pkl`: trained model of gesture 'Shoulder_Flexion_Left'.
  - `Shoulder_Flexion_Right.pkl`: trained model of gesture Shoulder_Flexion_Right'.
  - `Shoulder_Forward_Elevation.pkl`: trained model of gesture 'Shoulder_Forward_Elevation'.

---

### Notebooks
It contains the Jupyter Notebooks used in different stages of the project:

- **Correction_Funcionality**: steps of the creation of the correction part.
- **Machine_Learning**: steps of the creation of the ML models.
- **Preprocessing**: preprocessing of the raw data.

---

### Archivos Principales

- `actuators.py`: simulator of the actuators.
- `edge.py`: simulator of the edge
- `sensors.py`: simulator of the sensors.
- `env`: environment file for database configuration.

---







### **Important Notes**

#### **Data and Notebooks**
Due to maximum file size limitations on GitHub:
- The **Data** folder and **Notebooks** folder could not be uploaded directly to this repository.
- Both can be found at the following link: [Data and Notebooks on Google Drive](https://drive.google.com/drive/folders/11haufJA0F9EgCLilFaLO8MBPACXaZtE7?usp=sharing)

#### **Before Running the Simulator**
1. Download the **Data** folder from: [Download Data Folder](https://drive.google.com/drive/folders/19tgrP-48tzInE2GnGRZ_yQvTyYgT38G7?usp=sharing)
2. Update the IP addresses in all scripts to match the IP of the computer where you will run the simulator.
3. Ensure all required Python libraries are installed.

#### **For Full Functionality**
- Insert your database credentials into the `env` file to allow file uploads to the cloud.

---

### **Execution Instructions**

To run the simulator:
1. Open three separate terminal windows.
2. Navigate in each terminal to the directory containing the `Simulation` folder.
3. Run each Python script in the following order:
   - First, run `edge.py` (as it serves as the server):
     ```bash
     python edge.py
     ```
   - Then, run the other two scripts (`sensors.py` and `actuators.py`) in any order:
     ```bash
     python sensors.py
     python actuators.py
     ```

---

### **Contact**
For any questions or issues, please contact **Group 2 (SRTS)** at: **srtsdemo@gmail.com**
