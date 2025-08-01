# -*- coding: utf-8 -*-
"""DM-DDL.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1D8mQ-kzbzrWsf2sns6R30lREAWYrxhgU

# Database Implementation

STEP 1: CREATE the SQLite database;
"""

import sqlite3
import pandas as pd

conn = sqlite3.connect("gym_database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Branch (
    branch_id INTEGER PRIMARY KEY AUTOINCREMENT,
    branch_name TEXT NOT NULL UNIQUE,
    city TEXT NOT NULL,
    street_address TEXT NOT NULL UNIQUE,
    opening_date TEXT NOT NULL CHECK (opening_date LIKE '____-__-__')
);
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS Members (
    member_id INTEGER PRIMARY KEY AUTOINCREMENT,
    branch_id INTEGER NOT NULL,
    member_first_name TEXT NOT NULL,
    member_last_name TEXT NOT NULL,
    member_date_of_birth TEXT NOT NULL CHECK (member_date_of_birth LIKE '____-__-__'),
    member_gender TEXT NOT NULL CHECK (member_gender IN ('M', 'F', 'Other')),
    email TEXT NOT NULL UNIQUE CHECK (email LIKE '%@%.%'),
    phone TEXT NOT NULL UNIQUE CHECK (LENGTH(phone) = 10),
    member_join_date TEXT NOT NULL CHECK (member_join_date LIKE '____-__-__'),
    FOREIGN KEY (branch_id) REFERENCES Branch(branch_id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Trainers (
    trainer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    branch_id INTEGER NOT NULL,
    trainer_first_name TEXT NOT NULL,
    trainer_last_name TEXT NOT NULL,
    trainer_gender TEXT NOT NULL CHECK (Trainer_gender IN ('M', 'F', 'Other')),
    trainer_date_of_birth TEXT NOT NULL CHECK (Trainer_date_of_birth LIKE '____-__-__'),
    specialisation TEXT NOT NULL,
    trainer_join_date TEXT NOT NULL CHECK (Trainer_join_date LIKE '____-__-__'),
    FOREIGN KEY (branch_id) REFERENCES Branch(branch_id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Class (
    class_id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_name TEXT NOT NULL UNIQUE,
    class_type TEXT NOT NULL,
    class_duration INTEGER NOT NULL CHECK (Class_duration BETWEEN 30 AND 60)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Membership_Type (
    membership_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    membership_type TEXT NOT NULL UNIQUE,
    membership_price REAL NOT NULL CHECK (membership_price >= 0),
    membership_duration INTEGER NOT NULL CHECK (membership_duration > 0)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Memberships (
    membership_id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL,
    membership_type_id INTEGER NOT NULL,
    membership_start_date TEXT NOT NULL CHECK (membership_start_date LIKE '____-__-__'),
    membership_end_date TEXT NOT NULL CHECK (membership_end_date LIKE '____-__-__'),
    payment_date TEXT NOT NULL CHECK (payment_date LIKE '____-__-__'),
    payment_amount REAL NOT NULL CHECK (payment_amount >= 0),
    payment_method TEXT NOT NULL,
    FOREIGN KEY (member_id) REFERENCES members(member_id),
    FOREIGN KEY (membership_type_id) REFERENCES membership_Type(membership_type_id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS CheckIns (
    checkin_id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL,
    checkin_stamp TEXT NOT NULL CHECK (checkin_stamp LIKE '____-__-__ __:__:__'),
    checkout_stamp TEXT CHECK (checkout_stamp LIKE '____-__-__ __:__:__'),
    visit_rating INTEGER CHECK (visit_rating BETWEEN 1 AND 5),
    FOREIGN KEY (member_id) REFERENCES members(member_id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Class_Sessions (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_id INTEGER NOT NULL,
    trainer_id INTEGER NOT NULL,
    start_time TEXT NOT NULL CHECK (start_time LIKE '____-__-__ __:__:__'),
    end_time TEXT NOT NULL CHECK (end_time > start_time),
    max_capacity INTEGER CHECK (max_capacity > 0),
    status TEXT NOT NULL CHECK (status IN ('Completed', 'Cancelled')),
    FOREIGN KEY (class_id) REFERENCES Class(class_id),
    FOREIGN KEY (trainer_id) REFERENCES Trainers(trainer_id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Class_Attendance (
    member_id INTEGER NOT NULL,
    session_id INTEGER NOT NULL,
    class_rating INTEGER CHECK (class_rating BETWEEN 1 AND 5),
    PRIMARY KEY (member_id, session_id),
    FOREIGN KEY (member_id) REFERENCES members(member_id),
    FOREIGN KEY (session_id) REFERENCES Class_Sessions(session_id)
);
""")

conn.commit()

"""STEP 2: Check Tables Created:

"""

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

for table_name in tables:
    print(f"Table: {table_name[0]}")
    cursor.execute(f"PRAGMA table_info({table_name[0]});")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  Column: {col[1]}, Type: {col[2]}, NotNull: {col[3]}, DefaultVal: {col[4]}, PrimaryKey: {col[5]}")
    print("-" * 20)

"""STEP 3: Upload Files:

Run this box multiple times to upload the relevant csv files. Or drag the files across to the Files window from your desktop.
"""

from google.colab import files
uploaded = files.upload()
for fn in uploaded.keys():
  print('User uploaded file "{name}" with length {length} bytes'.format(
      name=fn, length=len(uploaded[fn])))

"""STEP 4: Load CSV files into the database tables:"""

branch_df = pd.read_csv('/content/Branch.csv')
members_df = pd.read_csv('/content/Members.csv')
membership_types_df = pd.read_csv('/content/Membership_Type.csv')
memberships_df = pd.read_csv('/content/Memberships.csv')
trainers_df = pd.read_csv('/content/Trainers.csv')
classes_df = pd.read_csv('/content/Class.csv')
class_sessions_df = pd.read_csv('/content/Class_Sessions.csv')
checkins_df = pd.read_csv('/content/CheckIns.csv')
class_attendance_df = pd.read_csv('/content/Class_Attendance.csv')

# 3.1 insert Branch
branch_df.to_sql('Branch', conn, if_exists='append', index=False)

# 3.2 insert Members
members_df.to_sql('Members', conn, if_exists='append', index=False)

# 3.3 insert Membership_Type
membership_types_df.to_sql('Membership_Type', conn, if_exists='append', index=False)

# 3.4 insert Memberships
memberships_df.to_sql('Memberships', conn, if_exists='append', index=False)

# 3.5 insert Trainers
trainers_df.to_sql('Trainers', conn, if_exists='append', index=False)

# 3.6 insert Class
classes_df.to_sql('Class', conn, if_exists='append', index=False)

# 3.7 insert Class_Sessions
class_sessions_df.to_sql('Class_Sessions', conn, if_exists='append', index=False)

# 3.8 insert CheckIns
checkins_df.to_sql('CheckIns', conn, if_exists='append', index=False)

# 3.9 insert Class_Attendance
class_attendance_df.to_sql('Class_Attendance', conn, if_exists='append', index=False)

conn.commit()

print("All tables imported successfully!")

"""STEP 5: Check Data has loaded"""

# Query all three tables and load into pandas DataFrames
branch_df = pd.read_sql_query("SELECT * FROM Branch", conn)
members_df = pd.read_sql_query("SELECT * FROM Members", conn)
membership_types_df = pd.read_sql_query("SELECT * FROM Membership_Type", conn)
memberships_df = pd.read_sql_query("SELECT * FROM Memberships", conn)
trainers_df = pd.read_sql_query("SELECT * FROM Trainers", conn)
classes_df = pd.read_sql_query("SELECT * FROM Class", conn)
class_sessions_df = pd.read_sql_query("SELECT * FROM Class_Sessions", conn)
checkins_df = pd.read_sql_query("SELECT * FROM CheckIns", conn)
class_attendance_df = pd.read_sql_query("SELECT * FROM Class_Attendance", conn)

# Show the first 5 lines of each DataFrame
print("Branch Table:")
print(branch_df.head(5))

print("\nMembers Table:")
print(members_df.head(5))

print("\nMembership_Type Table:")
print(membership_types_df.head(5))

print("\nMemberships Table:")
print(memberships_df.head(5))

print("\nTrainers Table:")
print(trainers_df.head(5))

print("\nClasses Table:")
print(classes_df.head(5))

print("\nClass_Sessions Table:")
print(class_sessions_df.head(5))

print("\nCheckIns Table:")
print(checkins_df.head(5))

print("\nClass_Attendance Table:")
print(class_attendance_df.head(5))

"""ONLY RUN IF YOU NEED TO DELETE THE DATA IN THE TABLES

If you run go back to STEP 4 and re-run from there.
"""

# only run if you need to reset the tables without deleting the databae and starting again.
# Delete all data from the tables
cursor.execute("PRAGMA foreign_keys = OFF")
cursor.execute("DELETE FROM Branch")
cursor.execute("DELETE FROM Members")
cursor.execute("DELETE FROM Trainers")
cursor.execute("DELETE FROM Class")
cursor.execute("DELETE FROM Membership_Type")
cursor.execute("DELETE FROM Memberships")
cursor.execute("DELETE FROM CheckIns")
cursor.execute("DELETE FROM Class_Sessions")
cursor.execute("DELETE FROM Class_Attendance")
cursor.execute("PRAGMA foreign_keys = ON")

# Commit the changes
conn.commit()

print("Database Deleted - restart.")

"""#  Below are the SQL queries."""

# Total Membership Sales by Branch (per Year)
cursor.execute("""
  SELECT
    b.branch_name,
    strftime('%Y', ms.payment_date) AS payment_year,
    COUNT(ms.payment_date) AS total_memberships_sold
  FROM Memberships ms
  JOIN Members m ON ms.member_id = m.member_id
  JOIN Branch b ON m.branch_id = b.branch_id
  WHERE strftime('%Y', ms.payment_date) IN ('2022', '2023', '2024')
  GROUP BY b.branch_name, payment_year
  ORDER BY b.branch_name, payment_year;
""")
print(cursor.fetchall())

# Trends in Membership Sales by Type
cursor.execute("""
  SELECT
    strftime('%Y', ms.payment_date) AS payment_year,
    mt.membership_type,
    COUNT(ms.payment_date) AS total_memberships
  FROM Memberships ms
  JOIN Membership_Type mt ON ms.membership_type_id = mt.membership_type_id WHERE strftime('%Y', ms.payment_date) IN ('2022', '2023', '2024')
  GROUP BY payment_year, mt.membership_type
  ORDER BY mt.membership_type, payment_year;
""")
print(cursor.fetchall())

# Total Revenue per Membership Type (per Year)
cursor.execute("""
  SELECT
    strftime('%Y', ms.payment_date) AS payment_year,
    mt.membership_type,
    SUM(ms.payment_amount) AS total_membership_revenue
  FROM Memberships ms
  JOIN Membership_Type mt ON ms.membership_type_id = mt.membership_type_id WHERE strftime('%Y', ms.payment_date) IN ('2022', '2023', '2024')
  GROUP BY payment_year, mt.membership_type
  ORDER BY payment_year, mt.membership_type;
""")
print(cursor.fetchall())

# Class Popularity by Branch
cursor.execute("""
  SELECT
    b.branch_name,
    c.class_type,
    COUNT(ca.member_id) AS total_attendance
  FROM Class_Attendance ca
  JOIN Class_Sessions cs ON ca.session_id = cs.session_id
  JOIN Class c ON cs.class_id = c.class_id
  JOIN Trainers t ON cs.trainer_id = t.trainer_id
  JOIN Branch b ON t.branch_id = b.branch_id
  WHERE strftime('%Y', cs.start_time) IN ('2022', '2023', '2024') AND cs.status = 'Completed'
  GROUP BY b.branch_name, c.class_type
  ORDER BY b.branch_name, total_attendance DESC;
""")
print(cursor.fetchall())

# Gym Attendance Patterns across Seasons
cursor.execute("""
  SELECT
    b.branch_name,
    strftime('%Y', c.checkin_stamp) AS year,
    strftime('%m', c.checkin_stamp) AS month,
    COUNT(c.checkin_id) AS total_checkins
  FROM CheckIns c
  JOIN Members m ON c.member_id = m.member_id
  JOIN Branch b ON m.branch_id = b.branch_id
  WHERE strftime('%Y', c.checkin_stamp) IN ('2022', '2023', '2024')
  GROUP BY b.branch_name, year, month
  ORDER BY b.branch_name, year, month;
""")
print(cursor.fetchall())

# Churn Trends by Branch（2022 -2024)
cursor.execute("""
  SELECT
    b.branch_name,
    strftime('%Y', ms.membership_end_date) AS membership_end_year,
    COUNT(DISTINCT m.member_id) AS churned_members
  FROM Members m
  JOIN Branch b ON m.branch_id = b.branch_id
  JOIN Memberships ms ON m.member_id = ms.member_id
  JOIN (
    SELECT
    member_id,
    MAX(strftime('%Y', membership_end_date)) AS max_end_year
      FROM Memberships
      GROUP BY member_id
    ) AS max_dates ON m.member_id = max_dates.member_id
  WHERE strftime('%Y', ms.membership_end_date) IN ('2022', '2023', '2024')
  AND strftime('%Y', ms.membership_end_date) = max_dates.max_end_year
  GROUP BY membership_end_year, b.branch_name
  ORDER BY b.branch_name, membership_end_year;
""")
print(cursor.fetchall())

# Churn Trends by Membership Type （2022 -2024）
cursor.execute("""
  SELECT
    b.membership_type,
    strftime('%Y', ms.membership_end_date) AS membership_end_year,
    COUNT(DISTINCT m.member_id) AS churned_members
  FROM Members m
  JOIN Memberships ms ON m.member_id = ms.member_id
  JOIN Membership_Type b ON ms.membership_type_id = b.membership_type_id
  JOIN (
    SELECT
    member_id,
    MAX(strftime('%Y', membership_end_date)) AS max_end_year
    FROM Memberships
    GROUP BY member_id
    ) AS max_dates ON m.member_id = max_dates.member_id
  WHERE  strftime('%Y', ms.membership_end_date) IN ('2022', '2023', '2024')
  AND strftime('%Y', ms.membership_end_date) = max_dates.max_end_year
  GROUP BY membership_end_year, b.membership_type
  ORDER BY b.membership_type, membership_end_year;
""")
print(cursor.fetchall())

# Visit Rating by Branch
cursor.execute("""
  WITH CheckinCounts AS (
      SELECT
          b.branch_name,
          ci.visit_rating,
          COUNT(ci.checkin_id) AS rating_count
      FROM CheckIns ci
      JOIN Members m ON ci.member_id = m.member_id
      JOIN Branch b ON m.branch_id = b.branch_id
      WHERE strftime('%Y', ci.checkin_stamp) IN ('2022', '2023', '2024')
        AND ci.visit_rating IS NOT NULL
      GROUP BY b.branch_name, ci.visit_rating
  ),
  BranchTotal AS (
      SELECT
          branch_name,
          count(*) AS total_checkins
      FROM CheckIns ci
      JOIN Members m ON ci.member_id = m.member_id
      JOIN Branch b ON m.branch_id = b.branch_id
      WHERE strftime('%Y', ci.checkin_stamp) IN ('2022', '2023', '2024')
        AND ci.visit_rating IS NOT NULL
      GROUP BY branch_name
  )
  SELECT
      c.branch_name,
      c.visit_rating,
      c.rating_count * 1.0 / b.total_checkins *100 AS rating_percentage
  FROM CheckinCounts c
  JOIN BranchTotal b ON c.branch_name = b.branch_name
  ORDER BY c.branch_name, c.visit_rating;
""")
print(cursor.fetchall())

# Average Visit Ranking by Branch
cursor.execute("""
  SELECT
    b.branch_name AS branch_name,
    ROUND(AVG(c.visit_rating), 3) AS avg_visit_rating
  FROM CheckIns c
  JOIN Members m ON c.member_id = m.member_id
  JOIN Branch b ON m.branch_id = b.branch_id
  WHERE strftime('%Y', c.checkin_stamp) IN ('2022', '2023', '2024')
    AND c.visit_rating IS NOT NULL
  GROUP BY b.branch_name
  ORDER BY avg_visit_rating DESC;
""")
print(cursor.fetchall())

# Average Session Attendance Rates By Branch
cursor.execute("""
  SELECT
      b.branch_name,
      ROUND(AVG(1.0 * COALESCE(attendance_count, 0) / max_capacity), 4) AS avg_attendance_rate
  FROM Class_Sessions cs
  JOIN Trainers t ON cs.trainer_id = t.trainer_id
  JOIN Branch b ON t.branch_id = b.branch_id
  LEFT JOIN (
      SELECT
          session_id,
          COUNT(*) AS attendance_count
      FROM Class_Attendance
      GROUP BY session_id
  ) ca ON cs.session_id = ca.session_id
  WHERE cs.status = 'Completed'
  GROUP BY b.branch_name;
""")
print(cursor.fetchall())

# Average Session Attendance Rates By Class
cursor.execute("""
  SELECT
      c.class_type,
      c.class_name,
      ROUND(AVG(1.0 * COALESCE(attendance_count, 0) / max_capacity), 4) AS avg_attendance_rate
  FROM Class_Sessions cs
  JOIN Class c ON cs.class_id = c.class_id
  LEFT JOIN (
      SELECT
          session_id,
          COUNT(*) AS attendance_count
      FROM Class_Attendance
      GROUP BY session_id
  ) ca ON cs.session_id = ca.session_id
  WHERE cs.status = 'Completed'
  GROUP BY c.class_id
  ORDER BY c.class_type, c.class_name;
""")
print(cursor.fetchall())

# # Average Session Rating By Class
cursor.execute("""
    SELECT
        c.class_type,
        c.class_name,
        ROUND(AVG(class_rating), 3) AS avg_session_rating
    FROM Class_Sessions cs
    JOIN Class c ON cs.class_id = c.class_id
    JOIN Class_Attendance ca ON cs.session_id = ca.session_id
    WHERE cs.status = 'Completed'
    GROUP BY c.class_type, c.class_name
    ORDER BY c.class_type, c.class_name;
""")
print(cursor.fetchall())

# Average Session Rating By Branch
cursor.execute("""
  SELECT
      b.branch_name,
      ROUND(AVG(class_rating), 4) AS avg_session_rating
  FROM Class_Sessions cs
  JOIN Trainers t ON cs.trainer_id = t.trainer_id
  JOIN Branch b ON t.branch_id = b.branch_id
  JOIN Class_Attendance ca ON cs.session_id = ca.session_id
  WHERE cs.status = 'Completed'
  GROUP BY b.branch_name;
""")
print(cursor.fetchall())