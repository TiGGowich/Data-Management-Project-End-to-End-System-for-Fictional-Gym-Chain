#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 15 20:20:57 2025

@author: xinmengyang
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime

# ------------------------------
# 1. Load input data
# ------------------------------
sessions_df = pd.read_csv('0class_sessions_df.csv')
members_df = pd.read_csv('0members.csv')
checkins_df = pd.read_csv('0check_ins.csv')
classes_df = pd.read_csv('0Class.csv')


class_type_attendance = {
    "Cardio":     {"min_rate": 0.8, "max_rate": 0.98}, 
    "Strength":     {"min_rate": 0.6, "max_rate": 0.85},  
    "Flexibility":  {"min_rate": 0.7, "max_rate": 0.95},
    "Stretching":  {"min_rate": 0.65, "max_rate": 0.9},
    "Default": {"min_rate": 0.7, "max_rate": 0.98}
}
# ------------------------------
# 2. Filter 'Completed' sessions
# ------------------------------
completed_sessions = sessions_df[sessions_df['status'].str.lower() == 'completed'].copy()

# ------------------------------
# 3. Convert datetime columns
# ------------------------------
completed_sessions['session_start_dt'] = pd.to_datetime(completed_sessions['start_time'])
completed_sessions['session_end_dt'] = pd.to_datetime(completed_sessions['end_time'])
checkins_df['check_in_time'] = pd.to_datetime(checkins_df['check_in_time'])
checkins_df['check_out_time'] = pd.to_datetime(checkins_df['check_out_time'])

# Add date columns
completed_sessions['session_date'] = completed_sessions['session_start_dt'].dt.date

# ------------------------------
# 4. Merge check-ins with members
# ------------------------------
member_checkins = checkins_df.merge(
    members_df[['member_id', 'branch_id']],
    on='member_id',
    suffixes=('', '_member')
)

# ------------------------------
# 5. Process sessions by date
# ------------------------------
attendees_list = []

# Group sessions by date
date_groups = completed_sessions.groupby('session_date')

for date, date_sessions in date_groups:
    # Sort sessions by start time
    sorted_sessions = date_sessions.sort_values('session_start_dt')
    
    # Track member availability
    member_status = {}  # {member_id: {'count': int, 'time_slots': [(start, end)]}}
    
    for _, session in sorted_sessions.iterrows():
        branch_id = session['branch_id']
        session_start = session['session_start_dt']
        session_end = session['session_end_dt']
        session_id = session['session_id']
        capacity = session['capacity']
        
        # 1. Find eligible members with valid check-in times
        eligible = member_checkins[
            (member_checkins['branch_id'] == branch_id) &
            (member_checkins['check_in_time'] <= session_start) &
            (member_checkins['check_out_time'] >= session_end)
        ].copy()
        
        if eligible.empty:
            continue
        
        # 2. Filter members with available time slots
        available_members = []
        for member_id in eligible['member_id'].unique():
            member_records = eligible[eligible['member_id'] == member_id]
            
            # Check daily limit
            current_status = member_status.get(member_id, {'count': 0, 'time_slots': []})
            if current_status['count'] >= 5:
                continue
                
            # Check time conflict
            conflict = False
            for slot in current_status['time_slots']:
                if not (session_end <= slot[0] or session_start >= slot[1]):
                    conflict = True
                    break
            if not conflict:
                available_members.append(member_id)
        
        # 3. Calculate attendance
        # attendance_rate = random.uniform(0.7, 0.98)
        

        session_class_mapping = sessions_df[['session_id', 'class_id']].drop_duplicates()
        current_class_id = session['class_id']
        class_type = classes_df[classes_df['class_id'] == current_class_id]['type'].values[0]
        
       
        config = class_type_attendance.get(class_type, class_type_attendance["Default"])
        attendance_rate = random.uniform(config["min_rate"], config["max_rate"])
        
        attendee_count = max(1, min(
            int(capacity * attendance_rate),
            len(available_members)
        ))
        
        if attendee_count == 0:
            continue
        
        # 4. Select attendees with preference for less active members
        selected = random.sample(available_members, attendee_count)
        
        # 5. Update member status
        for member_id in selected:
            if member_id not in member_status:
                member_status[member_id] = {
                    'count': 1,
                    'time_slots': [(session_start, session_end)]
                }
            else:
                member_status[member_id]['count'] += 1
                member_status[member_id]['time_slots'].append((session_start, session_end))
        
        session_class_mapping = sessions_df[['session_id', 'class_id']].drop_duplicates()

        # 在处理每个session时：
        session_attendees = eligible[eligible['member_id'].isin(selected)].drop_duplicates('member_id')
        session_attendees['session_id'] = session_id
        session_attendees['class_id'] = session['class_id'] 
        session_attendees['session_start'] = session_start
        session_attendees['session_end'] = session_end
        session_attendees['attendance_rate'] = attendance_rate
        attendees_list.append(session_attendees)

# ------------------------------
# 6. Combine all attendance records
# ------------------------------
attendance_records = pd.concat(attendees_list, ignore_index=True)

# ------------------------------
# 7. Enforce capacity constraints
# ------------------------------
session_capacities = completed_sessions.set_index('session_id')['capacity'].to_dict()

final_records = []
for session_id, group in attendance_records.groupby('session_id'):
    capacity = session_capacities.get(session_id, len(group))
    final_records.append(group.head(capacity))

attendance_records = pd.concat(final_records, ignore_index=True)

# ------------------------------
# 8. Assign ratings with nulls
# ------------------------------
def assign_ratings(df):
    result = []
    for branch_id, group in df.groupby('branch_id'):
        null_ratio = random.uniform(0.4, 0.5)
        group['rating'] = np.random.randint(1, 6, group.shape[0])
        null_indices = group.sample(frac=null_ratio).index
        group.loc[null_indices, 'rating'] = np.nan
        result.append(group)
    return pd.concat(result)

attendance_records = assign_ratings(attendance_records)

def assign_ranking_with_bias(df):   
    unique_branches = df['branch_id'].unique()
    branch_biases = {branch_id: np.random.uniform(-0.5, 0.5) for branch_id in unique_branches}
    
    unique_classes = df['class_id_x'].unique()
    #class_biases = {class_id: np.random.uniform(-1.0, 1.0) for class_id in unique_classes}
    class_biases = {}
    for class_id in unique_classes:
        if random.random() < 0.3:
            class_biases[class_id] = np.random.uniform(-3.0, 3.0)
        else:
            class_biases[class_id] = np.random.uniform(-1.5, 1.5)
    
        result_dfs = []
    
    for branch_id, group in df.groupby('branch_id'):
        total = len(group)
        branch_bias = branch_biases[branch_id]
        null_ratio = random.uniform(0.4, 0.5)
        null_count = int(total * null_ratio)
        

        ratings = []
        for idx, row in group.iterrows():
            att_rate = row['attendance_rate']
            class_id = row['class_id_x']
            
            if att_rate >= 0.8:
                base_mean = 3.5 + (att_rate - 0.8) * 2.0 / 0.2  # 0.8→3.5分，0.9→4.5分
            elif att_rate >= 0.6:
                base_mean = 2.5 + (att_rate - 0.6) * 1.0 / 0.2  # 0.6→2.5分，0.8→3.5分
            else:
                base_mean = 1.5 + (att_rate - 0.5) * 1.0 / 0.1  # 0.5→1.5分，0.6→2.5分
            

            adjusted_mean = base_mean + branch_bias + class_biases[class_id]
            #class_type = classes_df[classes_df['class_id'] == class_id]['class_type'].values[0]
            #type_effect = class_type_effect.get(class_type, 0.0)
            #adjusted_mean = base_mean + branch_bias + class_biases[class_id] + type_effect
            
            adjusted_mean = np.clip(adjusted_mean, 1.0, 5.0)
        
            rating = np.random.normal(loc=adjusted_mean, scale=0.8)
            rating = int(round(np.clip(rating, 1, 5)))
            ratings.append(rating)
        
        rated_group = group.copy()
        rated_group['rating'] = ratings
        
        # null_indices = rated_group.sample(n=null_count, random_state=42).index
        # rated_group.loc[null_indices, 'rating'] = np.nan
        if not rated_group.empty:
            bins = pd.cut(rated_group['rating'], bins=[1,2,3,4,5], labels=False)
            null_indices = rated_group.groupby(bins).sample(frac=null_ratio, random_state=42).index
            rated_group.loc[null_indices, 'rating'] = np.nan
        
        result_dfs.append(rated_group)
    
    return pd.concat(result_dfs, ignore_index=True)


attendance_records = attendance_records.merge(
    session_class_mapping,
    on='session_id',
    how='left',
    validate='many_to_one'  
)


attendance_records = assign_ranking_with_bias(attendance_records)

attendance_records[['member_id', 'session_id', 'rating']].to_csv('0Class_Attendance.csv', index=False)

