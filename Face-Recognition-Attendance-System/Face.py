import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import cv2
import csv
import os
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
# ── Dark Theme Palette ────────────────────────────────────────────────────────
BG      = "#0d1117"
CARD    = "#161b22"
BORDER  = "#30363d"
ACCENT  = "#238636"
BLUE    = "#1f6feb"
RED     = "#da3633"
YELLOW  = "#e3b341"
TEXT    = "#e6edf3"
SUBTEXT = "#8b949e"
ENTRY_C = "#21262d"
HOV_G   = "#2ea043"
HOV_B   = "#388bfd"
HOV_R   = "#f85149"

def _hover(btn, on_color, off_color):
    btn.bind("<Enter>", lambda e: btn.configure(bg=on_color))
    btn.bind("<Leave>", lambda e: btn.configure(bg=off_color))

# ── Main Window ───────────────────────────────────────────────────────────────
window = tk.Tk()
window.title("FAMS - Face Recognition Attendance System | Siddharth Prajapati")
window.geometry('1280x720')
window.configure(bg=BG)
window.resizable(True, True)

# GUI for manually fill attendance


def manually_fill():
    global sb
    sb = tk.Tk()
    # sb.iconbitmap('AMS.ico')
    sb.title("Enter subject name...")
    sb.geometry('580x320')
    sb.configure(background='grey80')

    def err_screen_for_subject():

        def ec_delete():
            ec.destroy()
        global ec
        ec = tk.Tk()
        ec.geometry('300x100')
        # ec.iconbitmap('AMS.ico')
        ec.title('Warning!!')
        ec.configure(background='snow')
        Label(ec, text='Please enter your subject name!!!', fg='red',
              bg='white', font=('times', 16, ' bold ')).pack()
        Button(ec, text='OK', command=ec_delete, fg="black", bg="lawn green", width=9, height=1, activebackground="Red",
               font=('times', 15, ' bold ')).place(x=90, y=50)

    def fill_attendance():
        ts = time.time()
        Date = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour, Minute, Second = timeStamp.split(":")
        # Creatting csv of attendance

        # Create table for Attendance
        date_for_DB = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
        global subb
        subb = SUB_ENTRY.get()
        DB_table_name = str(subb + "_" + Date + "_Time_" +
                            Hour + "_" + Minute + "_" + Second)

        import pymysql.connections

        # Connect to the database
        try:
            global cursor
            connection = pymysql.connect(
                host='localhost', user='root', password='', db='manually_fill_attendance')
            cursor = connection.cursor()
        except Exception as e:
            print(e)

        sql = "CREATE TABLE " + DB_table_name + """
                        (ID INT NOT NULL AUTO_INCREMENT,
                         ENROLLMENT varchar(100) NOT NULL,
                         NAME VARCHAR(50) NOT NULL,
                         DATE VARCHAR(20) NOT NULL,
                         TIME VARCHAR(20) NOT NULL,
                             PRIMARY KEY (ID)
                             );
                        """

        try:
            cursor.execute(sql)  # for create a table
        except Exception as ex:
            print(ex)  #

        if subb == '':
            err_screen_for_subject()
        else:
            sb.destroy()
            MFW = tk.Tk()
            # MFW.iconbitmap('AMS.ico')
            MFW.title("Manually attendance of " + str(subb))
            MFW.geometry('880x470')
            MFW.configure(background='grey80')

            def del_errsc2():
                errsc2.destroy()

            def err_screen1():
                global errsc2
                errsc2 = tk.Tk()
                errsc2.geometry('330x100')
                # errsc2.iconbitmap('AMS.ico')
                errsc2.title('Warning!!')
                errsc2.configure(background='grey80')
                Label(errsc2, text='Please enter Student & Enrollment!!!', fg='black', bg='white',
                      font=('times', 16, ' bold ')).pack()
                Button(errsc2, text='OK', command=del_errsc2, fg="black", bg="lawn green", width=9, height=1,
                       activebackground="Red", font=('times', 15, ' bold ')).place(x=90, y=50)

            def testVal(inStr, acttyp):
                if acttyp == '1':  # insert
                    if not inStr.isdigit():
                        return False
                return True

            ENR = tk.Label(MFW, text="Enter Enrollment", width=15, height=2, fg="black", bg="grey",
                           font=('times', 15))
            ENR.place(x=30, y=100)

            STU_NAME = tk.Label(MFW, text="Enter Student name", width=15, height=2, fg="black", bg="grey",
                                font=('times', 15))
            STU_NAME.place(x=30, y=200)

            global ENR_ENTRY
            ENR_ENTRY = tk.Entry(MFW, width=20, validate='key',
                                 bg="white", fg="black", font=('times', 23))
            ENR_ENTRY['validatecommand'] = (
                ENR_ENTRY.register(testVal), '%P', '%d')
            ENR_ENTRY.place(x=290, y=105)

            def remove_enr():
                ENR_ENTRY.delete(first=0, last=22)

            STUDENT_ENTRY = tk.Entry(
                MFW, width=20, bg="white", fg="black", font=('times', 23))
            STUDENT_ENTRY.place(x=290, y=205)

            def remove_student():
                STUDENT_ENTRY.delete(first=0, last=22)

            # get important variable
            def enter_data_DB():
                ENROLLMENT = ENR_ENTRY.get()
                STUDENT = STUDENT_ENTRY.get()
                if ENROLLMENT == '':
                    err_screen1()
                elif STUDENT == '':
                    err_screen1()
                else:
                    time = datetime.datetime.fromtimestamp(
                        ts).strftime('%H:%M:%S')
                    Hour, Minute, Second = time.split(":")
                    Insert_data = "INSERT INTO " + DB_table_name + \
                        " (ID,ENROLLMENT,NAME,DATE,TIME) VALUES (0, %s, %s, %s,%s)"
                    VALUES = (str(ENROLLMENT), str(
                        STUDENT), str(Date), str(time))
                    try:
                        cursor.execute(Insert_data, VALUES)
                    except Exception as e:
                        print(e)
                    ENR_ENTRY.delete(first=0, last=22)
                    STUDENT_ENTRY.delete(first=0, last=22)

            def create_csv():
                import csv
                cursor.execute("select * from " + DB_table_name + ";")
                csv_name = 'Attendance/Manually_Attendance/' + DB_table_name + '.csv'
                with open(csv_name, "w") as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow(
                        [i[0] for i in cursor.description])  # write headers
                    csv_writer.writerows(cursor)
                    O = "CSV created Successfully"
                    Notifi.configure(text=O, bg="Green", fg="white",
                                     width=33, font=('times', 19, 'bold'))
                    Notifi.place(x=180, y=380)
                import csv
                import tkinter
                root = tkinter.Tk()
                root.title("Attendance of " + subb)
                root.configure(background='grey80')
                with open(csv_name, newline="") as file:
                    reader = csv.reader(file)
                    r = 0

                    for col in reader:
                        c = 0
                        for row in col:
                            # i've added some styling
                            label = tkinter.Label(root, width=18, height=1, fg="black", font=('times', 13, ' bold '),
                                                  bg="white", text=row, relief=tkinter.RIDGE)
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()

            Notifi = tk.Label(MFW, text="CSV created Successfully", bg="Green", fg="white", width=33,
                              height=2, font=('times', 19, 'bold'))

            c1ear_enroll = tk.Button(MFW, text="Clear", command=remove_enr, fg="white", bg="black", width=10,
                                     height=1,
                                     activebackground="white", font=('times', 15, ' bold '))
            c1ear_enroll.place(x=690, y=100)

            c1ear_student = tk.Button(MFW, text="Clear", command=remove_student, fg="white", bg="black", width=10,
                                      height=1,
                                      activebackground="white", font=('times', 15, ' bold '))
            c1ear_student.place(x=690, y=200)

            DATA_SUB = tk.Button(MFW, text="Enter Data", command=enter_data_DB, fg="black", bg="SkyBlue1", width=20,
                                 height=2,
                                 activebackground="white", font=('times', 15, ' bold '))
            DATA_SUB.place(x=170, y=300)

            MAKE_CSV = tk.Button(MFW, text="Convert to CSV", command=create_csv, fg="black", bg="SkyBlue1", width=20,
                                 height=2,
                                 activebackground="white", font=('times', 15, ' bold '))
            MAKE_CSV.place(x=570, y=300)

            def attf():
                import subprocess
                subprocess.Popen(["open", "Attendance/Manually_Attendance"])

            attf = tk.Button(MFW,  text="Check Sheets", command=attf, fg="white", bg="black",
                             width=12, height=1, activebackground="white", font=('times', 14, ' bold '))
            attf.place(x=730, y=410)

            MFW.mainloop()

    SUB = tk.Label(sb, text="Enter Subject : ", width=15, height=2,
                   fg="black", bg="grey80", font=('times', 15, ' bold '))
    SUB.place(x=30, y=100)

    global SUB_ENTRY

    SUB_ENTRY = tk.Entry(sb, width=20, bg="white",
                         fg="black", font=('times', 23))
    SUB_ENTRY.place(x=250, y=105)

    fill_manual_attendance = tk.Button(sb, text="Fill Attendance", command=fill_attendance, fg="black", bg="SkyBlue1", width=20, height=2,
                                       activebackground="white", font=('times', 15, ' bold '))
    fill_manual_attendance.place(x=250, y=160)
    sb.mainloop()

# For clear textbox


def clear():
    txt.delete(first=0, last=22)


def clear1():
    txt2.delete(first=0, last=22)


def del_sc1():
    sc1.destroy()


def err_screen():
    global sc1
    sc1 = tk.Tk()
    sc1.geometry('300x100')
    # sc1.iconbitmap('AMS.ico')
    sc1.title('Warning!!')
    sc1.configure(background='grey80')
    Label(sc1, text='Enrollment & Name required!!!', fg='black',
          bg='white', font=('times', 16)).pack()
    Button(sc1, text='OK', command=del_sc1, fg="black", bg="lawn green", width=9,
           height=1, activebackground="Red", font=('times', 15, ' bold ')).place(x=90, y=50)

# Error screen2


def del_sc2():
    sc2.destroy()


def err_screen1():
    global sc2
    sc2 = tk.Tk()
    sc2.geometry('300x100')
    # sc2.iconbitmap('AMS.ico')
    sc2.title('Warning!!')
    sc2.configure(background='grey80')
    Label(sc2, text='Please enter your subject name!!!', fg='black',
          bg='white', font=('times', 16)).pack()
    Button(sc2, text='OK', command=del_sc2, fg="black", bg="lawn green", width=9,
           height=1, activebackground="Red", font=('times', 15, ' bold ')).place(x=90, y=50)

# For take images for datasets


def take_img():
    l1 = txt.get()
    l2 = txt2.get()
    if l1 == '':
        err_screen()
    elif l2 == '':
        err_screen()
    else:
        try:
            cam = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
            detector = cv2.CascadeClassifier(
                'haarcascade_frontalface_default.xml')
            Enrollment = txt.get()
            Name = txt2.get()
            sampleNum = 0
            while (True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    # incrementing sample number
                    sampleNum = sampleNum + 1
                    # saving the captured face in the dataset folder
                    cv2.imwrite("TrainingImage/" + Name + "." + Enrollment + '.' + str(sampleNum) + ".jpg", gray)
                    print(f"Images Saved for Enrollment : {Enrollment} | Sample: {sampleNum}")
                    cv2.imshow('Frame', img)
                # wait for 100 miliseconds
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                #
                # # break if the sample number is morethan 100
                elif sampleNum > 70:
                    break


            cam.release()
            cv2.waitKey(1)
            cv2.destroyAllWindows()
            cv2.waitKey(1)
            ts = time.time()
            Date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            row = [Enrollment, Name, Date, Time]
            with open('StudentDetails/StudentDetails.csv', 'a+') as csvFile:
                writer = csv.writer(csvFile, delimiter=',')
                writer.writerow(row)
                csvFile.close()
            res = "Images Saved for Enrollment : " + Enrollment + " Name : " + Name
            Notification.configure(
                text=res, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
            Notification.place(x=250, y=400)
        except FileExistsError as F:
            f = 'Student Data already exists'
            Notification.configure(text=f, bg="Red", width=21)
            Notification.place(x=450, y=400)


def _warn_popup(title, message):
    """Show a dark-themed warning popup — no crash, no freeze."""
    pop = tk.Toplevel(window)
    pop.title(title)
    pop.configure(bg=BG)
    pop.resizable(False, False)
    pop.grab_set()

    hdr = tk.Frame(pop, bg=CARD, height=54,
                   highlightbackground=BORDER, highlightthickness=1)
    hdr.pack(fill="x"); hdr.pack_propagate(False)
    tk.Label(hdr, text=title, bg=CARD, fg=YELLOW,
             font=("Helvetica", 13, "bold")).place(x=14, y=14)

    tk.Label(pop, text=message, bg=BG, fg=TEXT,
             font=("Helvetica", 11), justify="center",
             padx=30, pady=20).pack()

    btn_f = tk.Frame(pop, bg=BLUE, cursor="hand2")
    btn_f.pack(pady=(0, 18))
    btn_l = tk.Label(btn_f, text="  OK  ", bg=BLUE, fg=TEXT,
                     font=("Helvetica", 11, "bold"), padx=20, pady=8)
    btn_l.pack()
    for w in (btn_f, btn_l):
        w.bind("<Enter>",    lambda e: [btn_f.configure(bg=HOV_B), btn_l.configure(bg=HOV_B)])
        w.bind("<Leave>",    lambda e: [btn_f.configure(bg=BLUE),  btn_l.configure(bg=BLUE)])
        w.bind("<Button-1>", lambda e: pop.destroy())
    pop.bind("<Return>", lambda e: pop.destroy())


# for choose subject and fill attendance
def subjectchoose():
    def Fillattendances():
        sub = tx.get()
        if sub == '':
            err_screen1()
            return

        # ── Pre-flight: check students are registered ─────────────────────────
        csv_path = "StudentDetails/StudentDetails.csv"
        if not os.path.isfile(csv_path) or os.path.getsize(csv_path) == 0:
            _warn_popup("⚠️  No Students Registered",
                        "Please register at least one student\nvia the Admin Panel before marking attendance.")
            return

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        try:
            recognizer.read("TrainingImageLabel/Trainer.yml")
        except:
            _warn_popup("⚠️  Model Not Found",
                        "No trained model found.\nGo to Admin Panel → Train Model first.")
            return

        harcascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(harcascadePath)
        df = pd.read_csv(csv_path, names=['Enrollment', 'Name', 'Date', 'Time'])

        if df.empty:
            _warn_popup("⚠️  No Students Registered",
                        "Student list is empty.\nRegister students via Admin Panel first.")
            return

        cam = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
        font = cv2.FONT_HERSHEY_SIMPLEX
        col_names = ['Enrollment', 'Name', 'Date', 'Time']
        attendance = pd.DataFrame(columns=col_names)

        # Timer starts AFTER camera + model are ready (true 3-second window)
        now = time.time()
        future = now + 3

        while True:
            ret, im = cam.read()
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.2, 5)
            for (x, y, w, h) in faces:
                global Id
                Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
                if conf < 70:
                    print(conf)
                    global Subject
                    global aa
                    global date
                    global timeStamp
                    Subject = tx.get()
                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    aa = df.loc[df['Enrollment'] == Id]['Name'].values
                    global tt
                    if len(aa) == 0:          # ID recognised but not in CSV
                        Id = 'Unknown'
                        tt = 'Unknown'
                        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 3)
                        cv2.putText(im, tt, (x, y - 10), font, 0.8, (0, 25, 255), 2)
                    else:
                        tt = str(Id) + "-" + str(aa[0])
                        attendance.loc[len(attendance)] = [Id, aa[0], date, timeStamp]
                        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 220, 80), 3)
                        cv2.putText(im, str(tt), (x, y - 10), font, 0.8, (0, 255, 100), 2)
                else:
                    Id = 'Unknown'
                    tt = str(Id)
                    cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 3)
                    cv2.putText(im, str(tt), (x, y - 10), font, 0.8, (0, 25, 255), 2)

            if time.time() > future:
                break

            attendance = attendance.drop_duplicates(['Enrollment'], keep='first')
            cv2.imshow('Filling Attendance (3 sec) — press ESC to cancel', im)
            key = cv2.waitKey(30) & 0xff
            if key == 27:
                break

        # Force close the OpenCV window on macOS
        cam.release()
        cv2.waitKey(200)            # allow last frame to process
        cv2.destroyAllWindows()
        for _ in range(20):         # flush macOS event queue
            cv2.waitKey(1)

        attendance = attendance.drop_duplicates(['Enrollment'], keep='first')
        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Subject = tx.get()

        # One file per subject — append if it already exists
        fileName = "Attendance/" + Subject + ".csv"
        file_exists = os.path.isfile(fileName)
        attendance.to_csv(fileName, mode='a', header=not file_exists, index=False)
        print(attendance)

        M = f"✅  Attendance saved — {len(attendance)} student(s) marked"
        Notifica.configure(text=M, fg=ACCENT)

        # Auto-close the sub-window
        windo.after(800, windo.destroy)

        # Show last 5 rows in a dark popup
        _show_recent(fileName, Subject)

    def _show_recent(csv_path, subject_name):
        """Show last 5 rows of the subject CSV in a dark styled popup."""
        try:
            df_all = pd.read_csv(csv_path)
        except Exception:
            return

        recent = df_all.tail(5)

        pop = tk.Toplevel(window)
        pop.title(f"Recent Attendance — {subject_name}")
        pop.configure(bg=BG)
        pop.resizable(False, False)

        # Header
        ph = tk.Frame(pop, bg=CARD, height=60,
                      highlightbackground=BORDER, highlightthickness=1)
        ph.pack(fill="x")
        ph.pack_propagate(False)
        tk.Label(ph, text=f"📄  {subject_name}  —  Last {len(recent)} Records",
                 bg=CARD, fg=TEXT, font=("Helvetica", 13, "bold")).place(x=14, y=8)
        tk.Label(ph, text=f"Total records in file: {len(df_all)}",
                 bg=CARD, fg=SUBTEXT, font=("Helvetica", 9)).place(x=16, y=36)

        tbl = tk.Frame(pop, bg=BG, padx=20, pady=16)
        tbl.pack()

        cols = list(recent.columns)
        col_widths = [12, 18, 14, 12]

        # Header row
        for c, (col, w) in enumerate(zip(cols, col_widths)):
            tk.Label(tbl, text=col.upper(), bg=CARD, fg=ACCENT,
                     font=("Helvetica", 10, "bold"), width=w,
                     relief="flat", pady=6,
                     highlightbackground=BORDER, highlightthickness=1).grid(
                row=0, column=c, padx=2, pady=(0, 2), sticky="ew")

        # Data rows
        for r, (_, row_data) in enumerate(recent.iterrows(), start=1):
            row_bg = ENTRY_C if r % 2 == 0 else CARD
            for c, (val, w) in enumerate(zip(row_data, col_widths)):
                tk.Label(tbl, text=str(val), bg=row_bg, fg=TEXT,
                         font=("Helvetica", 10), width=w, pady=5,
                         relief="flat",
                         highlightbackground=BORDER, highlightthickness=1).grid(
                    row=r, column=c, padx=2, pady=1, sticky="ew")

        # Close button
        cf = tk.Frame(pop, bg="#6e40c9", cursor="hand2")
        cf.pack(pady=(0, 16))
        cl = tk.Label(cf, text="✕  Close", bg="#6e40c9", fg=TEXT,
                      font=("Helvetica", 11, "bold"), padx=20, pady=8)
        cl.pack()
        for w in (cf, cl):
            w.bind("<Enter>",    lambda e: [cf.configure(bg="#8957e5"), cl.configure(bg="#8957e5")])
            w.bind("<Leave>",    lambda e: [cf.configure(bg="#6e40c9"), cl.configure(bg="#6e40c9")])
            w.bind("<Button-1>", lambda e: pop.destroy())

    # ── Auto Attendance popup ─────────────────────────────────────────────────
    windo = tk.Toplevel(window)
    windo.title("Auto Attendance")
    windo.geometry("500x380")
    windo.configure(bg=BG)
    windo.resizable(False, False)
    windo.grab_set()

    # Header
    hdr = tk.Frame(windo, bg=CARD, height=64,
                   highlightbackground=BORDER, highlightthickness=1)
    hdr.pack(fill="x")
    hdr.pack_propagate(False)
    tk.Label(hdr, text="✅  Automatic Attendance",
             bg=CARD, fg=TEXT, font=("Helvetica", 15, "bold")).place(x=16, y=10)
    tk.Label(hdr, text="Camera runs for 3 seconds and marks present students",
             bg=CARD, fg=SUBTEXT, font=("Helvetica", 9)).place(x=18, y=38)

    # Card body
    body_f = tk.Frame(windo, bg=BG)
    body_f.pack(fill="both", expand=True, padx=24, pady=20)

    # Subject label + entry
    tk.Label(body_f, text="Subject Name", bg=BG, fg=SUBTEXT,
             font=("Helvetica", 9)).pack(anchor="w")
    tx = tk.Entry(body_f, width=36,
                  bg=ENTRY_C, fg=TEXT, insertbackground=TEXT,
                  font=("Helvetica", 14), relief="flat",
                  highlightbackground=BORDER, highlightthickness=1)
    tx.pack(fill="x", pady=(4, 16), ipady=8)
    tx.focus()

    # Status label
    Notifica = tk.Label(body_f, text="", bg=BG, fg=SUBTEXT,
                        font=("Helvetica", 10), wraplength=440, justify="left")
    Notifica.pack(anchor="w", pady=(0, 12))

    tk.Frame(body_f, bg=BORDER, height=1).pack(fill="x", pady=(0, 16))

    # Buttons row — Frame+Label for macOS color support
    btn_row = tk.Frame(body_f, bg=BG)
    btn_row.pack(fill="x")

    def _sub_btn(parent, icon, text, cmd, bg_c, hov_c):
        outer = tk.Frame(parent, bg=bg_c, cursor="hand2")
        outer.pack(side="left", padx=(0, 10))
        inner = tk.Label(outer, text=f"{icon}  {text}", bg=bg_c, fg=TEXT,
                         font=("Helvetica", 11, "bold"), padx=16, pady=10)
        inner.pack()
        def _e(e): outer.configure(bg=hov_c); inner.configure(bg=hov_c)
        def _l(e): outer.configure(bg=bg_c);  inner.configure(bg=bg_c)
        for w in (outer, inner):
            w.bind("<Enter>", _e); w.bind("<Leave>", _l)
            w.bind("<Button-1>", lambda e: cmd())

    _sub_btn(btn_row, "▶", "Start Attendance (3 sec)",
             Fillattendances, "#6e40c9", "#8957e5")

    def _view_recent():
        sub = tx.get().strip()
        if not sub:
            return
        path = "Attendance/" + sub + ".csv"
        if not os.path.isfile(path):
            Notifica.configure(text=f"No file found for '{sub}' yet.", fg=YELLOW)
            return
        _show_recent(path, sub)

    _sub_btn(btn_row, "📂", "View Sheets", _view_recent, ENTRY_C, "#3d444d")

    windo.mainloop()


def admin_panel():
    # ── Login screen ──────────────────────────────────────────────────────────
    login = tk.Toplevel(window)
    login.title("Admin Login")
    login.geometry("460x380")
    login.configure(bg=BG)
    login.resizable(False, False)
    login.grab_set()

    lhdr = tk.Frame(login, bg=CARD, height=70,
                    highlightbackground=BORDER, highlightthickness=1)
    lhdr.pack(fill="x"); lhdr.pack_propagate(False)
    tk.Label(lhdr, text="🔐  Admin Login", bg=CARD, fg=TEXT,
             font=("Helvetica", 15, "bold")).place(x=16, y=10)
    tk.Label(lhdr, text="Siddharth Prajapati  •  Restricted Access",
             bg=CARD, fg=SUBTEXT, font=("Helvetica", 9)).place(x=18, y=42)

    lfrm = tk.Frame(login, bg=BG, padx=32, pady=20)
    lfrm.pack(fill="both", expand=True)
    err_lbl = tk.Label(lfrm, text="", bg=BG, fg=RED,
                       font=("Helvetica", 10, "bold"))
    err_lbl.pack(anchor="w", pady=(0, 8))
    tk.Label(lfrm, text="Username", bg=BG, fg=SUBTEXT,
             font=("Helvetica", 9)).pack(anchor="w")
    un_e = tk.Entry(lfrm, bg=ENTRY_C, fg=TEXT, insertbackground=TEXT,
                    font=("Helvetica", 13), relief="flat",
                    highlightbackground=BORDER, highlightthickness=1)
    un_e.pack(fill="x", pady=(4, 12), ipady=8); un_e.focus()
    tk.Label(lfrm, text="Password", bg=BG, fg=SUBTEXT,
             font=("Helvetica", 9)).pack(anchor="w")
    pw_e = tk.Entry(lfrm, show="●", bg=ENTRY_C, fg=TEXT,
                    insertbackground=TEXT, font=("Helvetica", 13),
                    relief="flat", highlightbackground=BORDER, highlightthickness=1)
    pw_e.pack(fill="x", pady=(4, 20), ipady=8)

    try:
        from admin_config import ADMIN_USERNAME, ADMIN_PASSWORD
    except ImportError:
        ADMIN_USERNAME = "admin"
        ADMIN_PASSWORD = "admin"

    def _open_dash(event=None):
        if un_e.get().strip() == ADMIN_USERNAME and \
           pw_e.get().strip() == ADMIN_PASSWORD:
            login.destroy()
            _admin_dashboard()
        else:
            err_lbl.configure(text="❌  Incorrect username or password")
            pw_e.delete(0, END)

    login.bind("<Return>", _open_dash)
    br = tk.Frame(lfrm, bg=BG); br.pack(fill="x")
    for icon, lbl, cmd, bg_c, hov_c in [
        ("🔓", "Login",  _open_dash,    BLUE,      HOV_B),
        ("✕",  "Cancel", login.destroy, "#3d444d", "#57606a"),
    ]:
        oo = tk.Frame(br, bg=bg_c, cursor="hand2"); oo.pack(side="left", padx=(0, 10))
        ii = tk.Label(oo, text=f"{icon}  {lbl}", bg=bg_c, fg=TEXT,
                      font=("Helvetica", 11, "bold"), padx=18, pady=10); ii.pack()
        def _he(e, o=oo, i=ii, h=hov_c): o.configure(bg=h); i.configure(bg=h)
        def _hl(e, o=oo, i=ii, b=bg_c):  o.configure(bg=b); i.configure(bg=b)
        for w in (oo, ii):
            w.bind("<Enter>", _he); w.bind("<Leave>", _hl)
            w.bind("<Button-1>", lambda e, c=cmd: c())
    login.mainloop()


def _admin_dashboard():
    """Admin control panel — opened after successful login."""
    dash = tk.Toplevel(window)
    dash.title("Admin Dashboard")
    dash.geometry("940x640")
    dash.configure(bg=BG)
    dash.grab_set()

    # Header
    dh = tk.Frame(dash, bg=CARD, height=64,
                  highlightbackground=BORDER, highlightthickness=1)
    dh.pack(fill="x"); dh.pack_propagate(False)
    tk.Label(dh, text="⚙️  Admin Dashboard", bg=CARD, fg=TEXT,
             font=("Helvetica", 15, "bold")).place(x=16, y=10)
    tk.Label(dh, text="Register students  •  Train model  •  Manage roster",
             bg=CARD, fg=SUBTEXT, font=("Helvetica", 9)).place(x=18, y=38)

    db = tk.Frame(dash, bg=BG)
    db.pack(fill="both", expand=True, padx=16, pady=14)

    # ── LEFT col: Register + Train ────────────────────────────────────────────
    left = tk.Frame(db, bg=BG)
    left.pack(side="left", fill="y", padx=(0, 14))

    rc = tk.Frame(left, bg=CARD, padx=20, pady=18,
                  highlightbackground=BORDER, highlightthickness=1)
    rc.pack(fill="x", pady=(0, 12))
    tk.Label(rc, text="📸  Register New Student", bg=CARD, fg=TEXT,
             font=("Helvetica", 13, "bold")).pack(anchor="w")
    tk.Frame(rc, bg=BORDER, height=1).pack(fill="x", pady=(8, 14))

    def _val(P, d):
        if d == '1' and not P.isdigit(): return False
        return True

    tk.Label(rc, text="Enrollment Number", bg=CARD, fg=SUBTEXT,
             font=("Helvetica", 9)).pack(anchor="w")
    enr_e = tk.Entry(rc, validate="key", bg=ENTRY_C, fg=TEXT,
                     insertbackground=TEXT, font=("Helvetica", 13), relief="flat",
                     highlightbackground=BORDER, highlightthickness=1, width=28)
    enr_e['validatecommand'] = (enr_e.register(_val), '%P', '%d')
    enr_e.pack(fill="x", pady=(4, 10), ipady=7)
    tk.Label(rc, text="Student Name", bg=CARD, fg=SUBTEXT,
             font=("Helvetica", 9)).pack(anchor="w")
    name_e = tk.Entry(rc, bg=ENTRY_C, fg=TEXT, insertbackground=TEXT,
                      font=("Helvetica", 13), relief="flat",
                      highlightbackground=BORDER, highlightthickness=1, width=28)
    name_e.pack(fill="x", pady=(4, 12), ipady=7)
    reg_st = tk.Label(rc, text="", bg=CARD, fg=ACCENT,
                      font=("Helvetica", 9), wraplength=260)
    reg_st.pack(anchor="w", pady=(0, 10))

    def _take():
        enr = enr_e.get().strip(); nm = name_e.get().strip()
        if not enr or not nm:
            reg_st.configure(text="❌ Fill both fields.", fg=RED); return
        txt.delete(0, END); txt.insert(0, enr)
        txt2.delete(0, END); txt2.insert(0, nm)
        reg_st.configure(text="📸 Camera opening…", fg=YELLOW); dash.update()
        take_img()
        reg_st.configure(text=f"✅ Saved for {nm}", fg=ACCENT)
        enr_e.delete(0, END); name_e.delete(0, END)
        _refresh()

    cap_o = tk.Frame(rc, bg=ACCENT, cursor="hand2"); cap_o.pack(anchor="w")
    cap_i = tk.Label(cap_o, text="📸  Capture Images", bg=ACCENT, fg=TEXT,
                     font=("Helvetica", 11, "bold"), padx=14, pady=8); cap_i.pack()
    for w in (cap_o, cap_i):
        w.bind("<Enter>",    lambda e: [cap_o.configure(bg=HOV_G), cap_i.configure(bg=HOV_G)])
        w.bind("<Leave>",    lambda e: [cap_o.configure(bg=ACCENT), cap_i.configure(bg=ACCENT)])
        w.bind("<Button-1>", lambda e: _take())

    tc = tk.Frame(left, bg=CARD, padx=20, pady=18,
                  highlightbackground=BORDER, highlightthickness=1)
    tc.pack(fill="x")
    tk.Label(tc, text="🧠  Train Recognition Model", bg=CARD, fg=TEXT,
             font=("Helvetica", 13, "bold")).pack(anchor="w")
    tk.Frame(tc, bg=BORDER, height=1).pack(fill="x", pady=(8, 10))
    tk.Label(tc, text="Run after adding new students.", bg=CARD, fg=SUBTEXT,
             font=("Helvetica", 9)).pack(anchor="w", pady=(0, 10))
    tr_st = tk.Label(tc, text="", bg=CARD, fg=ACCENT, font=("Helvetica", 9))
    tr_st.pack(anchor="w", pady=(0, 10))

    def _train():
        tr_st.configure(text="🔄 Training…", fg=YELLOW); dash.update()
        trainimg()
        tr_st.configure(text="✅ Model trained!", fg=ACCENT)
        _log("Admin retrained the model")

    tr_o = tk.Frame(tc, bg=BLUE, cursor="hand2"); tr_o.pack(anchor="w")
    tr_i = tk.Label(tr_o, text="🧠  Train Model", bg=BLUE, fg=TEXT,
                    font=("Helvetica", 11, "bold"), padx=14, pady=8); tr_i.pack()
    for w in (tr_o, tr_i):
        w.bind("<Enter>",    lambda e: [tr_o.configure(bg=HOV_B), tr_i.configure(bg=HOV_B)])
        w.bind("<Leave>",    lambda e: [tr_o.configure(bg=BLUE), tr_i.configure(bg=BLUE)])
        w.bind("<Button-1>", lambda e: _train())

    # ── RIGHT col: Student list with Remove ───────────────────────────────────
    ra = tk.Frame(db, bg=CARD, padx=18, pady=16,
                  highlightbackground=BORDER, highlightthickness=1)
    ra.pack(side="left", fill="both", expand=True)
    rh = tk.Frame(ra, bg=CARD); rh.pack(fill="x")
    tk.Label(rh, text="👥  Registered Students", bg=CARD, fg=TEXT,
             font=("Helvetica", 13, "bold")).pack(side="left")
    cnt_lbl = tk.Label(rh, text="", bg=CARD, fg=SUBTEXT,
                       font=("Helvetica", 9)); cnt_lbl.pack(side="right")
    tk.Frame(ra, bg=BORDER, height=1).pack(fill="x", pady=(8, 0))

    canv = tk.Canvas(ra, bg=CARD, highlightthickness=0)
    vsb  = tk.Scrollbar(ra, orient="vertical", command=canv.yview)
    sf   = tk.Frame(canv, bg=CARD)
    sf.bind("<Configure>", lambda e: canv.configure(scrollregion=canv.bbox("all")))
    canv.create_window((0, 0), window=sf, anchor="nw")
    canv.configure(yscrollcommand=vsb.set)
    canv.pack(side="left", fill="both", expand=True, pady=(8, 0))
    vsb.pack(side="right", fill="y")

    for c, (h, w) in enumerate(zip(
            ["ENROLLMENT", "NAME", "REG. DATE", "REMOVE"], [13, 18, 14, 10])):
        tk.Label(sf, text=h, bg=ENTRY_C, fg=ACCENT,
                 font=("Helvetica", 9, "bold"), width=w, pady=5,
                 relief="flat").grid(row=0, column=c, padx=1, pady=(0, 2), sticky="ew")

    def _refresh():
        for w in sf.winfo_children():
            info = w.grid_info()
            if info and int(info.get("row", 0)) > 0:
                w.destroy()
        try:
            df_s = pd.read_csv("StudentDetails/StudentDetails.csv",
                               names=["Enrollment", "Name", "Date", "Time"])
        except Exception:
            cnt_lbl.configure(text="No students yet"); return
        cnt_lbl.configure(text=f"{len(df_s)} enrolled")
        for r, (_, row) in enumerate(df_s.iterrows(), start=1):
            rbg = ENTRY_C if r % 2 == 0 else CARD
            enr_v = str(row["Enrollment"])
            nm_v  = str(row["Name"])
            dt_v  = str(row["Date"])
            for c, (val, w) in enumerate(zip([enr_v, nm_v, dt_v], [13, 18, 14])):
                tk.Label(sf, text=val, bg=rbg, fg=TEXT,
                         font=("Helvetica", 10), width=w, pady=4,
                         relief="flat").grid(row=r, column=c, padx=1, pady=1, sticky="ew")

            def _del(enr=enr_v, nm=nm_v):
                try:
                    df_all = pd.read_csv("StudentDetails/StudentDetails.csv",
                                         names=["Enrollment", "Name", "Date", "Time"])
                    df_all = df_all[df_all["Enrollment"].astype(str) != enr]
                    df_all.to_csv("StudentDetails/StudentDetails.csv",
                                  index=False, header=False)
                except Exception as ex:
                    print(f"CSV error: {ex}")
                deleted = 0
                for img in os.listdir("TrainingImage"):
                    parts = img.split(".")
                    if len(parts) >= 3 and parts[1] == enr:
                        try: os.remove(os.path.join("TrainingImage", img)); deleted += 1
                        except Exception: pass
                _log(f"Removed: {nm} [{enr}] — {deleted} images deleted")
                _refresh()

            rb_o = tk.Frame(sf, bg=RED, cursor="hand2")
            rb_o.grid(row=r, column=3, padx=1, pady=1, sticky="ew")
            rb_i = tk.Label(rb_o, text="✕ Remove", bg=RED, fg=TEXT,
                            font=("Helvetica", 9, "bold"), padx=6, pady=4)
            rb_i.pack()
            for w in (rb_o, rb_i):
                w.bind("<Enter>",    lambda e, o=rb_o, i=rb_i: [o.configure(bg=HOV_R), i.configure(bg=HOV_R)])
                w.bind("<Leave>",    lambda e, o=rb_o, i=rb_i: [o.configure(bg=RED), i.configure(bg=RED)])
                w.bind("<Button-1>", lambda e, fn=_del: fn())

    _refresh()
    dash.mainloop()





# For train the model
def trainimg():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    global detector
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    try:
        global faces, Id
        faces, Id = getImagesAndLabels("TrainingImage")
    except Exception as e:
        l = 'please make "TrainingImage" folder & put Images'
        Notification.configure(text=l, bg="SpringGreen3",
                               width=50, font=('times', 18, 'bold'))
        Notification.place(x=350, y=400)

    recognizer.train(faces, np.array(Id))
    try:
        recognizer.save("TrainingImageLabel/Trainer.yml")
    except Exception as e:
        q = 'Please make "TrainingImageLabel" folder'
        Notification.configure(text=q, bg="SpringGreen3",
                               width=50, font=('times', 18, 'bold'))
        Notification.place(x=350, y=400)

    res = "Model Trained"  # +",".join(str(f) for f in Id)
    Notification.configure(text=res, bg="olive drab",
                           width=50, font=('times', 18, 'bold'))
    Notification.place(x=250, y=400)


def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faceSamples = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        if imagePath.endswith(".jpg"):
        # loading the image and converting it to gray scale
            pilImage = Image.open(imagePath).convert('L')
            # Now we are converting the PIL image into numpy array
            imageNp = np.array(pilImage, 'uint8')
            # getting the Id from the image

            Id = int(os.path.split(imagePath)[-1].split(".")[1])
            # extract the face from the training image sample
            faces = detector.detectMultiScale(imageNp)
            # If a face is there then append that in the list as well as Id of it
            for (x, y, w, h) in faces:
                faceSamples.append(imageNp[y:y + h, x:x + w])
                Ids.append(Id)
    return faceSamples, Ids


# ── Quit Handler ──────────────────────────────────────────────────────────────
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit FAMS?"):
        window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)

# ══════════════════════════════════════════════════════════════════════════════
#  HEADER BAR
# ══════════════════════════════════════════════════════════════════════════════
header = tk.Frame(window, bg=CARD, height=72,
                  highlightbackground=BORDER, highlightthickness=1)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(header, text="🎓", bg=CARD, fg=TEXT,
         font=("Helvetica", 28)).place(x=18, y=14)
tk.Label(header, text="Face Recognition Attendance System",
         bg=CARD, fg=TEXT, font=("Helvetica", 18, "bold")).place(x=68, y=10)
tk.Label(header, text="AI-Powered  •  Siddharth Prajapati",
         bg=CARD, fg=SUBTEXT, font=("Helvetica", 10)).place(x=70, y=42)

clock_lbl = tk.Label(header, bg=CARD, fg=SUBTEXT, font=("Helvetica", 11))
clock_lbl.place(relx=1.0, x=-20, rely=0.5, anchor="e")
def _tick():
    clock_lbl.configure(
        text=datetime.datetime.now().strftime("%a, %d %b %Y   %I:%M:%S %p"))
    window.after(1000, _tick)
_tick()

# ══════════════════════════════════════════════════════════════════════════════
#  MAIN BODY  (left card + right panel)
# ══════════════════════════════════════════════════════════════════════════════
body = tk.Frame(window, bg=BG)
body.pack(fill="both", expand=True, padx=20, pady=14)

# ── LEFT CARD: Today info ────────────────────────────────────────────────────
left_card = tk.Frame(body, bg=CARD, padx=26, pady=22,
                     highlightbackground=BORDER, highlightthickness=1)
left_card.pack(side="left", fill="y")

tk.Label(left_card, text="📅  Today's Session",
         bg=CARD, fg=TEXT, font=("Helvetica", 14, "bold")).pack(anchor="w")
tk.Frame(left_card, bg=BORDER, height=1).pack(fill="x", pady=(8, 18))

tk.Label(left_card, text=datetime.date.today().strftime("%A"),
         bg=CARD, fg=ACCENT, font=("Helvetica", 22, "bold")).pack(anchor="w")
tk.Label(left_card, text=datetime.date.today().strftime("%d %B %Y"),
         bg=CARD, fg=TEXT, font=("Helvetica", 13)).pack(anchor="w", pady=(0, 20))

tk.Frame(left_card, bg=BORDER, height=1).pack(fill="x", pady=(0, 18))

tk.Label(left_card, text="How to use",
         bg=CARD, fg=SUBTEXT, font=("Helvetica", 9, "bold")).pack(anchor="w")
for step in [
    "1️⃣  Click Auto Attendance",
    "2️⃣  Enter subject name",
    "3️⃣  Look at the camera (3 sec)",
    "4️⃣  Attendance saved automatically",
]:
    tk.Label(left_card, text=step, bg=CARD, fg=TEXT,
             font=("Helvetica", 10), justify="left").pack(anchor="w", pady=2)

tk.Frame(left_card, bg=BORDER, height=1).pack(fill="x", pady=(18, 10))
tk.Label(left_card, text="🔐  Admin access for registration",
         bg=CARD, fg=SUBTEXT, font=("Helvetica", 9),
         wraplength=200, justify="left").pack(anchor="w")

# Dummy txt/txt2/Notification so core functions don't break
txt  = tk.Entry(left_card); txt.pack_forget()
txt2 = tk.Entry(left_card); txt2.pack_forget()
Notification = tk.Label(left_card, text="", bg=CARD, fg=ACCENT,
                        font=("Helvetica", 10), wraplength=220)
Notification.pack(anchor="w", pady=(8, 0))

def clear():  txt.delete(0, END)
def clear1(): txt2.delete(0, END)

# ── RIGHT PANEL ───────────────────────────────────────────────────────────────
right = tk.Frame(body, bg=BG)
right.pack(side="left", fill="both", expand=True, padx=(16, 0))

# Stat cards row
stats_row = tk.Frame(right, bg=BG)
stats_row.pack(fill="x", pady=(0, 12))

def stat_card(parent, icon, val, lbl, color):
    f = tk.Frame(parent, bg=CARD, padx=18, pady=12,
                 highlightbackground=BORDER, highlightthickness=1)
    f.pack(side="left", expand=True, fill="both", padx=(0, 10))
    tk.Label(f, text=icon, bg=CARD, fg=color, font=("Helvetica", 22)).pack()
    tk.Label(f, text=val,  bg=CARD, fg=TEXT,  font=("Helvetica", 20, "bold")).pack()
    tk.Label(f, text=lbl,  bg=CARD, fg=SUBTEXT, font=("Helvetica", 9)).pack()

try:
    with open("StudentDetails/StudentDetails.csv") as _f:
        _count = sum(1 for _ in _f)
except Exception:
    _count = 0

stat_card(stats_row, "👥", str(_count), "Registered Students", BLUE)
stat_card(stats_row, "📅", datetime.date.today().strftime("%d %b"), "Today", ACCENT)
stat_card(stats_row, "⚡", "3 sec", "Recognition Window", YELLOW)

# Log card
log_card = tk.Frame(right, bg=CARD, padx=18, pady=14,
                    highlightbackground=BORDER, highlightthickness=1)
log_card.pack(fill="both", expand=True)
tk.Label(log_card, text="📊  System Log",
         bg=CARD, fg=TEXT, font=("Helvetica", 13, "bold")).pack(anchor="w")
tk.Frame(log_card, bg=BORDER, height=1).pack(fill="x", pady=(6, 10))

log_box = tk.Text(log_card, bg=ENTRY_C, fg=TEXT, font=("Courier", 10),
                  height=8, relief="flat", state="disabled",
                  insertbackground=TEXT, wrap="word",
                  highlightbackground=BORDER, highlightthickness=1)
log_box.pack(fill="both", expand=True)

def _log(msg):
    log_box.configure(state="normal")
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    log_box.insert("end", f"[{ts}]  {msg}\n")
    log_box.see("end")
    log_box.configure(state="disabled")

_log("FAMS started. Ready.")

# ══════════════════════════════════════════════════════════════════════════════
#  BOTTOM ACTION BAR
# ══════════════════════════════════════════════════════════════════════════════
btn_bar = tk.Frame(window, bg=CARD, height=88,
                   highlightbackground=BORDER, highlightthickness=1)
btn_bar.pack(fill="x", side="bottom")
btn_bar.pack_propagate(False)

btn_inner = tk.Frame(btn_bar, bg=CARD)
btn_inner.place(relx=0.5, rely=0.5, anchor="center")

# macOS-compatible colored button using Frame + Label
def _make_action_btn(parent, icon, label, cmd, bg_color, hov_color):
    outer = tk.Frame(parent, bg=bg_color, padx=2, pady=2)
    outer.pack(side="left", padx=8)

    inner = tk.Frame(outer, bg=bg_color, cursor="hand2")
    inner.pack()

    lbl_icon = tk.Label(inner, text=icon, bg=bg_color, fg=TEXT,
                        font=("Helvetica", 18))
    lbl_icon.pack(pady=(8, 0))

    lbl_text = tk.Label(inner, text=label, bg=bg_color, fg=TEXT,
                        font=("Helvetica", 11, "bold"),
                        width=18, pady=6)
    lbl_text.pack()

    def on_enter(e):
        outer.configure(bg=hov_color)
        inner.configure(bg=hov_color)
        lbl_icon.configure(bg=hov_color)
        lbl_text.configure(bg=hov_color)

    def on_leave(e):
        outer.configure(bg=bg_color)
        inner.configure(bg=bg_color)
        lbl_icon.configure(bg=bg_color)
        lbl_text.configure(bg=bg_color)

    def on_click(e):
        cmd()

    for w in (outer, inner, lbl_icon, lbl_text):
        w.bind("<Enter>",   on_enter)
        w.bind("<Leave>",   on_leave)
        w.bind("<Button-1>", on_click)

    return outer

_make_action_btn(btn_inner, "✅", "Auto Attendance",    subjectchoose, "#6e40c9", "#8957e5")
_make_action_btn(btn_inner, "✏️",  "Manual Attendance", manually_fill, "#9e6a03", "#d29922")
_make_action_btn(btn_inner, "🔐", "Admin Panel",        admin_panel,   "#3d444d", "#57606a")

window.mainloop()
