# 🎓 Face Recognition Attendance Management System

A **Face Recognition based Attendance Management System** built using **Python, OpenCV, and Tkinter**.
The system captures student facial images, trains a recognition model, and automatically marks attendance using a webcam.

---

# 🚀 Features

* 📸 Capture student face images
* 🧠 Train face recognition model
* 👤 Automatic attendance using webcam
* 📄 Export attendance to CSV
* 📝 Manual attendance option
* 🖥 Simple GUI using Tkinter

---

# 🛠 Tech Stack

* Python
* OpenCV
* Tkinter
* NumPy
* Pandas
* Pillow

---

# 📦 Installation

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/Face-Recognition-Attendance-System.git
cd Face-Recognition-Attendance-System
```

---

# 🧪 Create Virtual Environment (Recommended)

Using a virtual environment prevents dependency conflicts.

## Create Environment

```bash
conda create -n face_attendance python=3.10
```

---

## Activate Environment

```bash
conda activate face_attendance
```

Your terminal will look like:

```
(face_attendance) username@computer %
```

---

# 📥 Install Required Libraries

Install dependencies inside the virtual environment:

```bash
pip install opencv-contrib-python
pip install numpy
pip install pandas
pip install pillow
pip install pymysql
```

---

# ▶️ Run the Project

Make sure the environment is activated.

```bash
python AMS_Run.py
```

The GUI will open.

---

# ⏹ Stop the Program

Press **CTRL + C** in the terminal or close the GUI window.

---

# 🔌 Deactivate Virtual Environment

When you finish working:

```bash
conda deactivate
```

Your terminal will return to the base environment.

Example:

```
(base) username@computer %
```

---

# 🔁 Full Workflow Example

Every time you want to run the project:

```bash
conda activate face_attendance
cd ~/Desktop/attendence/Face-Recognition-Attendance-System
python AMS_Run.py
```

After finishing:

```bash
conda deactivate
```

---

# 📁 Project Structure

```
Face-Recognition-Attendance-System
│
├── AMS_Run.py
├── haarcascade_frontalface_default.xml
│
├── TrainingImage
│
├── TrainingImageLabel
│
├── StudentDetails
│     └── StudentDetails.csv
│
├── Attendance
│     └── Manually_Attendance
```

---

# 🧑‍💻 Usage

### Register Student

1. Enter **Enrollment Number**
2. Enter **Student Name**
3. Click **Take Images**

Images will be saved in:

```
TrainingImage/
```

---

### Train Model

Click **Train Images**.

The trained model will be saved in:

```
TrainingImageLabel/Trainer.yml
```

---

### Automatic Attendance

Click **Automatic Attendance**.

The system will detect faces and mark attendance automatically.

Attendance will be saved as:

```
Attendance/Subject_Date_Time.csv
```

---

### Manual Attendance

If face recognition fails, use:

**Manually Fill Attendance**

You can manually enter student data.

---

# 📊 Output Example

```
Attendance/AI_2026-03-14_10-25-34.csv
```

---

# ⚠️ Notes

* Good lighting improves accuracy.
* Blurry images reduce recognition accuracy.
* Training time increases with more students.

---

# 🔮 Future Improvements

* Web dashboard
* Deep learning face recognition (FaceNet / DeepFace)
* Cloud database
* Real-time analytics

---

# 👨‍💻 Author

**Siddharth Prajapati**

---

⭐ If you like this project, consider giving it a **star on GitHub**.
