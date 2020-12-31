import mysql.connector
mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  passwd="",
  database="databaseproject"
)
mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE admin (id int(11) NOT NULL,username varchar(70) NOT NULL,password varchar(60) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;")
mycursor.execute("CREATE TABLE doctor (SSN int(11) NOT NULL,password varchar(200) NOT NULL,Name varchar(60) NOT NULL, email varchar(70) NOT NULL,phone varchar(60) NOT NULL,start_hour time NOT NULL,end_hour time NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;")
mycursor.execute("CREATE TABLE patient (SSN int(11) NOT NULL,password varchar(200) NOT NULL,Name varchar(70) NOT NULL,Phone varchar(50) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;")
mycursor.execute("CREATE TABLE patient_doctor (PSSN int(11) NOT NULL,DSSN int(11) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;")
mycursor.execute("CREATE TABLE patient_files (PSSN int(11) NOT NULL,Filename varchar(100) NOT NULL,FileURL varchar(100) NOT NULL,DSSN int(11) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;")
mycursor.execute("ALTER TABLE doctor ADD PRIMARY KEY (SSN);")
mycursor.execute("ALTER TABLE patient ADD PRIMARY KEY (SSN);")
mycursor.execute("ALTER TABLE patient_doctor ADD PRIMARY KEY (PSSN,DSSN), ADD KEY DSSN (DSSN);")
mycursor.execute("ALTER TABLE patient_files ADD PRIMARY KEY (FileURL), ADD KEY PSSN (PSSN), ADD KEY DSSN (DSSN);")
mycursor.execute("ALTER TABLE patient_doctor ADD CONSTRAINT patient_doctor_ibfk_1 FOREIGN KEY (PSSN) REFERENCES patient (SSN), ADD CONSTRAINT patient_doctor_ibfk_2 FOREIGN KEY (DSSN) REFERENCES doctor (SSN);")
mycursor.execute("ALTER TABLE patient_files ADD CONSTRAINT patient_files_ibfk_1 FOREIGN KEY (PSSN) REFERENCES patient (SSN),ADD CONSTRAINT patient_files_ibfk_2 FOREIGN KEY (DSSN) REFERENCES doctor (SSN);")
