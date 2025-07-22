#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 15 20:30:59 2025

@author: xinmengyang
"""

import pandas as pd

sessions_df = pd.read_csv('0class_sessions_df.csv')
print(sessions_df.columns.tolist())
rename_dict = {
    "capacity": "max_capacity"
}
sessions_df = sessions_df.rename(columns=rename_dict)
sessions_df = sessions_df.drop(columns=['session_date', 'branch_id'])
sessions_df.to_csv('Class_Sessions.csv', index=False)


members_df = pd.read_csv('0members.csv')
print(members_df.columns.tolist())
mrename_dict = {
    'first_name':'member_first_name', 
    'last_name':'member_last_name',
    'date_of_birth':'member_date_of_birth', 
    'gender':'member_gender',
    'join_date':'member_join_date'
}
members_df = members_df.rename(columns=mrename_dict)
members_df.to_csv('Members.csv', index=False)


checkins_df = pd.read_csv('0check_ins.csv')
print(checkins_df.columns.tolist())
ckrename_dict = {
    'check_in_id':'checkin_id',
    'check_in_time':'checkin_stamp',
    'check_out_time':'checkout_stamp',
    'overall_rating':'visit_rating'
}
checkins_df = checkins_df.rename(columns=ckrename_dict)
checkins_df = checkins_df.drop(columns=['branch_id'])
checkins_df['visit_rating'] = checkins_df['visit_rating'].astype('Int64')  
checkins_df.to_csv('CheckIns.csv', index=False)


trainers_df = pd.read_csv('0trainers.csv')
print(trainers_df.columns.tolist())
trename_dict = {
    'first_name':'trainer_first_name',
    'last_name':'trainer_last_name', 
    'gender':'trainer_gender', 
    'date_of_birth':'trainer_date_of_birth',     
    'join_date':'trainer_join_date'
}
trainers_df = trainers_df.rename(columns=trename_dict)
trainers_df.to_csv('Trainers.csv', index=False)


memberships_df = pd.read_csv('0payments.csv')
print(memberships_df.columns.tolist())
prename_dict = {
    'payment_id':'membership_id',
    'membership_id':'membership_type_id', 
    'start_date':'membership_start_date', 
    'end_date':'membership_end_date'
}
memberships_df = memberships_df.rename(columns=prename_dict)
memberships_df = memberships_df.drop(columns=['branch_id', 'duration_days'])
memberships_df.to_csv('Memberships.csv', index=False)


Class_Attendance_df = pd.read_csv('0Class_Attendance.csv')
arename_dict = {'rating':'class_rating'}
Class_Attendance_df = Class_Attendance_df.rename(columns=arename_dict)
Class_Attendance_df['class_rating'] = Class_Attendance_df['class_rating'].astype('Int64')  
Class_Attendance_df.to_csv('Class_Attendance.csv', index=False)

classes_df = pd.read_csv('0Class.csv')
print(classes_df.columns.tolist())
clrename_dict = {
    'name':'class_name',
    'type':'class_type', 
    'duration':'class_duration'
}
classes_df = classes_df.rename(columns=clrename_dict)
classes_df.to_csv('Class.csv', index=False)



