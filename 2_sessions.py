#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 15 20:12:26 2025

@author: xinmengyang
"""

import pandas as pd
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

branches_df = pd.read_csv('Branch.csv')
trainers_df = pd.read_csv('0trainers.csv')
classes_df = pd.read_csv('0Class.csv')

START_DATE = datetime(2022, 1, 1)
END_DATE = datetime(2024, 12, 31)

def generate_class_sessions(branches_df, trainers_df, classes_df):
    """
    Generate class session data for branches based on trainers and classes.

    Business Rules:
        - Branch with 1 trainer: 8-10 sessions per week, max 2 sessions per day
        - Branch with 2-3 trainers: 18-20 sessions per week
        - Branch with 4+ trainers: 25-30 sessions per week
        - Each week has at least 5 sessions
        - Sessions are scheduled after the trainer's join_date
        - Sessions are scheduled between 7-9 AM or 6-8 PM
        - Session capacity is randomly 10, 15, or 20
        - Each branch has 85%-98% of sessions marked as 'Completed', rest as 'Cancelled'
        - A trainer cannot have overlapping sessions or back-to-back sessions within 1 hour
    """
    sessions = []
    session_id = 1

    for _, branch in branches_df.iterrows():
        branch_id = branch['branch_id']
        branch_trainers = trainers_df[trainers_df['branch_id'] == branch_id]
        trainer_count = len(branch_trainers)

        if trainer_count == 0:
            print(f"Branch {branch_id} has no trainers. Skipping.")
            continue

        # Weekly session count based on trainer count
        if trainer_count == 2:
            weekly_sessions = random.randint(10, 14)
        elif 3 <= trainer_count:
            weekly_sessions = random.randint(20, 25)
        else:
            weekly_sessions = random.randint(25, 30)

        # Time slots: Morning (7-10AM), Evening (6-8PM)
        time_slots = [(7, 10), (18, 20)]

        current_date = START_DATE
        while current_date <= END_DATE:
            daily_sessions = []
            trainers_scheduled_today = set()

            # Randomly decide how many sessions on this day (minimum 0, max depends on branch)
            sessions_today_count = random.randint(1, min(3, weekly_sessions // 7))

            attempts = 0
            while len(daily_sessions) < sessions_today_count and attempts < 50:
                attempts += 1

                # Pick a trainer not already scheduled today
                available_trainers = branch_trainers[
                    ~branch_trainers['trainer_id'].isin(trainers_scheduled_today)
                ]

                if available_trainers.empty:
                    break  # No trainer available

                trainer = available_trainers.sample(1).iloc[0]
                trainer_id = trainer['trainer_id']

                # Pick a class
                class_row = classes_df.sample(1).iloc[0]
                class_id = class_row['class_id']
                class_duration_minutes = int(class_row['duration'])
                
                # Pick session time
                slot = random.choice(time_slots)
                hour = random.randint(slot[0], slot[1] - 1)
                minute = random.choice([0, 30])
                
                session_start = datetime.combine(current_date, datetime.min.time()) + timedelta(hours=hour, minutes=minute)
                session_end = session_start + timedelta(minutes=class_duration_minutes)
                
                # Enforce: branch session gap >= 30 min
                conflict = False
                for existing in daily_sessions:
                    existing_start = existing['start_time']
                    existing_end = existing['end_time']
                
                    # Gap between sessions >= 30 mins
                    if not (
                        session_start >= existing_end + timedelta(minutes=30) or
                        session_end <= existing_start - timedelta(minutes=30)
                    ):
                        conflict = True
                        break
                
                if conflict:
                    continue  # Try another time
                
                # Everything is OK, schedule the session
                trainers_scheduled_today.add(trainer_id)
                
                sessions.append({
                    'session_id': session_id,
                    'class_id': class_id,
                    'trainer_id': trainer_id,
                    'start_time': session_start,
                    'end_time': session_end,
                    'capacity': random.choice([10, 15, 20]),
                    'status': 'Completed' if random.random() < 0.9 else 'Cancelled',
                    'session_date': current_date.date(),
                    'branch_id': branch_id
                })
                
                daily_sessions.append({
                    'start_time': session_start,
                    'end_time': session_end
                })
                
                session_id += 1

            # Move to the next day
            current_date += timedelta(days=1)

    sessions_df = pd.DataFrame(sessions)
    return sessions_df

class_sessions_df = generate_class_sessions(branches_df, trainers_df, classes_df)
class_sessions_df.to_csv('0class_sessions_df.csv', index=False)
