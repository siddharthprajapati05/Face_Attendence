# 🎓 Face Recognition Attendance System

> An AI-powered, real-time face recognition attendance management system built with Python, OpenCV, and a modern dark-themed Tkinter GUI. Designed for classrooms and institutions — automatically marks attendance in just **3 seconds** using a webcam.

[![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)](https://python.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8.1-green?logo=opencv)](https://opencv.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.3.3-purple)](https://pandas.pydata.org)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 📊 Project Stats

| Metric | Value |
|---|---|
| 📄 Lines of Code | ~1,120 |
| 📁 Total Project Files | 88 |
| 🖼️ Training Images / Student | 71 samples |
| ⚡ Recognition Window | 3 seconds |
| 🐍 Python Version | 3.10 |
| 🧠 ML Algorithm | LBPH Face Recognizer |
| 💾 Storage Format | Per-subject CSV files |
| 🖥️ GUI Framework | Tkinter (dark theme) |

---

## ✨ Features

### 👤 For Students
- ✅ **Auto Attendance** — Look at the camera for 3 seconds, attendance is saved automatically
- ✏️ **Manual Attendance** — Fill attendance manually if camera is unavailable
- 📂 **View Records** — Instantly preview the last 5 attendance entries per subject

### 🔐 For Admin (Password Protected)
- 📸 **Register New Students** — Capture 71 face images per student via webcam
- 🧠 **Train Recognition Model** — One-click model training with live status feedback
- 👥 **Manage Students** — View all registered students in a scrollable dark table
- 🗑️ **Remove Students** — Delete student from database and all training images in one click

### 🛡️ Safety & Reliability
- ⚠️ Friendly popup warnings instead of crashes (no students, model not found, etc.)
- 🔒 Admin panel with login protection (Username + Password)
- 📅 Single CSV file per subject — no duplicate files per session
- 🍎 macOS-compatible buttons (Frame+Label instead of tk.Button)

---

## 🖼️ UI Overview

| Screen | Description |
|---|---|
| **Main Window** | Dark dashboard with live clock, system log, stats, and action buttons |
| **Admin Login** | Dark card-style login form with Enter key support |
| **Admin Dashboard** | Register student + Train model + Student list with remove button |
| **Auto Attendance** | Subject input → 3-second camera window → auto-close + recent records popup |
| **Recent Records** | Last 5 attendance rows shown in a dark styled table |

---

## 🛠️ Tech Stack

| Library | Version | Purpose |
|---|---|---|
| `opencv-contrib-python` | 4.8.1.78 | Face detection & LBPH recognition |
| `numpy` | 1.26.4 | Image array processing |
| `pandas` | 2.3.3 | CSV attendance data management |
| `pillow` | 12.1.1 | Image handling |
| `pymysql` | — | Optional: MySQL database support |
| `tkinter` | built-in | GUI framework |

---

## 📁 Project Structure

```
Face-Recognition-Attendance-System/
│
├── Face.py                          # Main application (1120+ lines)
├── haarcascade_frontalface_default.xml  # Face detection model
│
├── TrainingImage/                   # Student face image datasets
│     └── Name.EnrollmentNo.N.jpg
│
├── TrainingImageLabel/              # Trained LBPH model
│     └── Trainer.yml
│
├── StudentDetails/                  # Student registry
│     └── StudentDetails.csv         # Enrollment, Name, Date, Time
│
├── Attendance/                      # Per-subject attendance records
│     ├── chem.csv
│     ├── phy.csv
│     ├── maths.csv
│     └── Manually_Attendance/
│
└── README.md
```

---

## ⚙️ Setup & Installation

### Step 1 — Clone the Repository

```bash
git clone https://github.com/siddharthprajapati05/Face_Attendence.git
cd Face-Recognition-Attendance-System
```

### Step 2 — Create Conda Environment

```bash
conda create -n face_attendance python=3.10
```

### Step 3 — Activate Environment

```bash
conda activate face_attendance
```

Your terminal prompt will change to:
```
(face_attendance) username@computer %
```

> ⚠️ **Always activate this environment before running the app.** Running with base Anaconda Python will cause NumPy/OpenCV import errors.

### Step 4 — Install Dependencies

```bash
pip install opencv-contrib-python==4.8.1.78
pip install numpy==1.26.4
pip install pandas
pip install pillow
pip install pymysql
```

Or install all at once:

```bash
pip install opencv-contrib-python==4.8.1.78 numpy==1.26.4 pandas pillow pymysql
```

---

## ▶️ Running the Application

```bash
conda activate face_attendance
cd ~/Desktop/attendence/Face-Recognition-Attendance-System
python Face.py
```

The dark-themed GUI will launch automatically.

---

## 🔄 Full Workflow

### 🔐 Admin Setup (First Time)

1. Click **🔐 Admin Panel** in the main window
2. Login with:
   - **Username:** `My name full name`
   - **Password:** `password is nike name + dob of 💕 + me`
3. In the Admin Dashboard:
   - Enter **Enrollment Number** and **Student Name**
   - Click **📸 Capture Images** → look at webcam (71 images captured)
   - Click **🧠 Train Model** → wait for training to complete
4. Student is now registered and ready for attendance

### ✅ Daily Attendance (Students)

1. Click **✅ Auto Attendance** from the main window
2. Enter the **Subject Name** (e.g., `chem`, `phy`, `maths`)
3. Click **▶ Start Attendance (3 sec)**
4. Look at the webcam — face is detected and recognized
5. After 3 seconds: attendance is saved, window auto-closes, recent records shown

### 📂 View Attendance Records

1. Click **✅ Auto Attendance**
2. Enter the subject name
3. Click **📂 View Sheets** → see last 5 entries in a popup

---

## 📋 Attendance CSV Format

Each subject has its own file: `Attendance/<subject>.csv`

```csv
Enrollment,Name,Date,Time
1231,Siddharth,2026-05-05,19:51:44
1231,Siddharth,2026-05-05,19:56:53
```

> New entries are **appended** to the same file — no duplicate files per session.

---

## ⚠️ Important Notes

| Situation | What happens |
|---|---|
| No students registered | ⚠️ Warning popup — no crash |
| Model not trained yet | ⚠️ Warning popup — no crash |
| Face not in database | Shown as "Unknown" in camera — no crash |
| Camera not closed | Fixed: uses `cv2.waitKey()` flush loop (macOS fix) |
| Wrong Python environment | Run `conda activate face_attendance` first |

- 💡 **Good lighting** significantly improves recognition accuracy
- 📏 Capture images at **similar distance** to how attendance will be taken
- 🔁 **Retrain the model** after adding any new student

---

## ⏹️ Stop the Application

Press **Ctrl + C** in the terminal, or close the main window.

```bash
conda deactivate   # when done working
```

---

## 🔮 Future Improvements

- [ ] Deep learning face recognition (FaceNet / DeepFace) for better accuracy
- [ ] Web dashboard for attendance analytics
- [ ] Cloud database integration (MySQL / Firebase)
- [ ] Email/SMS notification when attendance is marked
- [ ] Multi-camera support
- [ ] Attendance report export (PDF)

---

## 👨‍💻 Author

**Siddharth Prajapati**

- GitHub: [@siddharthprajapati05](https://github.com/siddharthprajapati05)

---

> ⭐ If this project helped you, give it a **star on GitHub!**
