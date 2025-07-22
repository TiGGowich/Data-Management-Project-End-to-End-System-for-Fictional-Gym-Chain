#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 15 19:54:57 2025

@author: xinmengyang
"""

import random
from datetime import datetime, timedelta
from faker import Faker
import pandas as pd
import numpy as np

fake = Faker()

# Constants
START_DATE = datetime(2022, 1, 1)
END_DATE = datetime(2024, 12, 31, 23, 59, 59)

generated_emails = set()
generated_phones = set()

def generate_long_tail_date(start_date, end_date):
    """
    Generate a join date with a long-tail distribution between start_date and end_date.
    """
    days_range = (end_date - start_date).days
    long_tail_day = int(np.random.exponential(scale=days_range / 3.0))
    long_tail_day = min(long_tail_day, days_range)
    return start_date + timedelta(days=long_tail_day)


def generate_unique_email():
    """
    Generate a unique, realistic-looking email address.
    """
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'icloud.com']
    
    while True:
        username_length = random.randint(6, 12)
        username = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=username_length))
        domain = random.choice(domains)
        email = f"{username}@{domain}"
        
        if email not in generated_emails:
            generated_emails.add(email)
            return email

def generate_unique_uk_phone_number():
    """
    Generate a unique UK phone number with 10 digits (starting with '0' for mobile numbers).
    """
    while True:
        phone = "07" + ''.join(str(random.randint(0, 9)) for _ in range(9))  # UK mobile numbers start with '0'
        
        if phone not in generated_phones:
            generated_phones.add(phone)
            return str(phone)

def generate_left_skewed_birth_date(start_date, end_date, skew_strength=5):
    """
    Generate left-skewed date_of_birth between start_date and end_date.
    
    skew_strength: larger value => more skewed towards end_date (younger people)
    """
    days_range = (end_date - start_date).days
    
    # beta distribution: alpha < beta creates left skew (bias toward end_date)
    alpha = 1
    beta = skew_strength

    # Draw a number between 0 and 1, skewed toward 1 (end_date)
    rand = np.random.beta(alpha, beta)

    # Convert to a day offset
    skewed_day = int(rand * days_range)

    return start_date + timedelta(days=skewed_day)

def generate_members_by_branch(branches_df, min_members=250, max_members=400):
    """
    Generate members for each branch.
    """
    members = []
    member_id = 1

    for _, branch in branches_df.iterrows():
        branch_id = branch['branch_id']
        num_members = random.randint(min_members, max_members)

        for _ in range(num_members):
            gender = random.choice(['M', 'F'])
            first_name = fake.first_name_male() if gender == 'M' else fake.first_name_female()
            last_name = fake.last_name()
            date_of_birth = generate_left_skewed_birth_date(
                start_date=datetime(1945, 1, 1),
                end_date=datetime(2005, 12, 31),
                skew_strength=4  # skew_strength controls how skewed toward the recent date
            )
            branch_opening_date = pd.to_datetime(branch['opening_date'])  
            join_date = generate_long_tail_date(branch_opening_date, END_DATE)
            email = generate_unique_email()
            phone = generate_unique_uk_phone_number()

            members.append({
                "member_id": member_id,
                "branch_id": branch_id,
                "first_name": first_name,
                "last_name": last_name,
                "date_of_birth": date_of_birth,
                "gender": gender,
                "email": email,
                "phone": phone,
                "join_date": join_date
            })

            member_id += 1

    members_df = pd.DataFrame(members)
    return members_df

def generate_payments_by_members(members_df, memberships_df):
    """
    Generate payments for members linked to their branch.
    """
    payments = []
    payment_id = 1

    for _, member in members_df.iterrows():
        current_end = None
        renewal_probability = random.uniform(0.7, 0.8)

        membership = memberships_df.sample(1).iloc[0]
        duration = int(membership['membership_duration'])
        payment_amount = membership['membership_price']
        membership_id = membership['membership_type_id']
        payment_methods = ['Credit Card', 'Cash', 'Paypal', 'Debit Card']
        weights = [0.29, 0.13, 0.24, 0.34]
        payment_method = random.choices(payment_methods, weights=weights, k=1)[0]
        payment_date = min(member['join_date'], END_DATE)
        start_date = min(payment_date, END_DATE)
        end_date = start_date + timedelta(days=duration)

        payments.append({
            "payment_id": payment_id,
            "member_id": member["member_id"],
            "membership_id": membership_id,
            "start_date": start_date,
            "end_date": end_date,
            "payment_date": payment_date,
            "payment_amount": payment_amount,
            "payment_method": payment_method,
            "branch_id": member["branch_id"],
            "duration_days": duration
        })

        payment_id += 1
        current_end = end_date

        while True:
            if random.random() > renewal_probability:
                break

            membership = memberships_df.sample(1).iloc[0]
            duration = int(membership['membership_duration'])
            payment_amount = membership['membership_price']
            membership_id = membership['membership_type_id']
            payment_method = random.choice(['Credit Card', 'Cash', 'Paypal', 'Debit Card'])

            if random.random() < 0.8:
                window_start = current_end - timedelta(days=7)
                window_end = current_end + timedelta(days=30)
                payment_date = fake.date_between_dates(
                    date_start=window_start,
                    date_end=window_end
                )
            else:
                delay_days = random.randint(30, 180)
                payment_date = current_end + timedelta(days=delay_days)

            payment_date = pd.Timestamp(payment_date)
            if payment_date > END_DATE:
                break

            effective_start_date = max(current_end + timedelta(days=1), payment_date)
            start_date = min(effective_start_date, END_DATE)
            end_date = start_date + timedelta(days=duration)

            payments.append({
                "payment_id": payment_id,
                "member_id": member["member_id"],
                "membership_id": membership_id,
                "start_date": start_date,
                "end_date": end_date,
                "payment_date": payment_date,
                "payment_amount": payment_amount,
                "payment_method": payment_method,
                "branch_id": member["branch_id"],
                "duration_days": duration
            })

            payment_id += 1
            current_end = end_date

    payments_df = pd.DataFrame(payments)
    return payments_df

def generate_check_ins_by_payments(payments_df):
    """
    Generate non-overlapping check-ins for each payment record, linked to the member and branch.
    Adds seasonality, weekday variations, and time slot peak patterns, with branch-specific differences.
    """
    check_ins = []
    check_in_id = 1

    # --- Branch-specific null rating probabilities ---
    branch_null_probability = {
        branch_id: random.uniform(0.5, 0.6) for branch_id in range(1, 8)
    }

    # --- Branch-specific rating distributions ---
    branch_rating_distribution = {
        4: ([5, 4, 3, 2, 1], [0.65, 0.3, 0.04, 0.009, 0.001]),
        1: ([5, 4, 3, 2, 1], [0.4, 0.4, 0.15, 0.04, 0.01]),
        5: ([5, 4, 3, 2, 1], [0.3, 0.4, 0.2, 0.09, 0.01]),
        2: ([5, 4, 3, 2, 1], [0.2, 0.45, 0.25, 0.08, 0.02]),
        6: ([5, 4, 3, 2, 1], [0.15, 0.3, 0.3, 0.15, 0.1]),
        3: ([5, 4, 3, 2, 1], [0.1, 0.25, 0.3, 0.25, 0.1]),
        7: ([5, 4, 3, 2, 1], [0.05, 0.1, 0.2, 0.4, 0.25]),
    }

    # --- Seasonal activity multipliers ---
    def get_seasonal_multiplier(date, branch_id):
        """Simulate branch-specific seasonality."""
        month = date.month
        base_multiplier = {
            1: 1.3, 2: 1.3, 3: 1.2,
            4: 0.9, 5: 1.1, 6: 1.2,
            7: 0.7, 8: 0.7, 9: 1.1,
            10: 1.0, 11: 0.8, 12: 0.8
        }.get(month, 1.0)

        # Add branch-specific noise
        noise = random.uniform(0.90, 1.08)
        if branch_id in [4, 5]:  
            noise *= 1.08
        elif branch_id in [6, 7]:  
            noise *= 0.90

        return base_multiplier * noise

    # --- Weekday activity multipliers ---
    def get_weekday_multiplier(date, branch_id):
        """Simulate day-of-week differences per branch."""
        weekday = date.weekday()  # 0 = Monday, 6 = Sunday
        base_multipliers = {
            0: 1.2,  # Monday
            1: 1.1,  # Tuesday
            2: 1.1,  # Wednesday
            3: 1.0,  # Thursday
            4: 0.7,  # Friday
            5: 0.9,  # Saturday
            6: 1.0   # Sunday
        }
        multiplier = base_multipliers.get(weekday, 1.0)

        # Branch differences
        if branch_id in [3, 7]:  
            if weekday in [5, 6]:
                multiplier *= 1.1
        elif branch_id == 1:  
            if weekday == 4:
                multiplier *= 1.2

        return multiplier

    # --- Time of day slot selection ---
    def generate_peak_check_in_time(visit_date, branch_id):
        """Simulate peak/off-peak time selection with branch variation."""
        base_slots = [
            {"start": 6, "end": 8, "weight": 10},    # Morning
            {"start": 9, "end": 11, "weight": 8},    # Mid morning
            {"start": 11, "end": 13, "weight": 12},  # Lunch time
            {"start": 14, "end": 17, "weight": 15},  # Afternoon
            {"start": 18, "end": 21, "weight": 40},  # Evening
            {"start": 21, "end": 23, "weight": 10},  # Late evening
            {"start": 0, "end": 5, "weight": 5}      # Night owls
        ]

        # Branch-specific tweaks
        if branch_id in [1, 4]:
            base_slots[4]["weight"] += 5  # Evening even more busy
        elif branch_id == 7:
            base_slots[5]["weight"] += 5  # Late evening activity

        weights = [slot["weight"] for slot in base_slots]
        chosen_slot = random.choices(base_slots, weights=weights, k=1)[0]

        hour = random.randint(chosen_slot["start"], chosen_slot["end"])
        minute = random.choice([0, 15, 30, 45])
        second = random.randint(0, 59)

        check_in_time = datetime.combine(visit_date, datetime.min.time()) + timedelta(hours=hour, minutes=minute, seconds=second)
        return check_in_time

    # --- Group payments by member ---
    payments_by_member = payments_df.groupby("member_id")

    for member_id, member_payments in payments_by_member:
        member_payments_sorted = member_payments.sort_values(by="start_date")

        for _, payment in member_payments_sorted.iterrows():
            start_date = payment["start_date"]
            end_date = payment["end_date"]
            duration_days = payment["duration_days"]
            branch_id = payment["branch_id"]

            # Base visits per duration period
            if duration_days <= 30:
                base_visits = 20
            elif duration_days <= 90:
                base_visits = 60
            else:
                base_visits = 150

            # Seasonal + random variation for visit count
            seasonal_multiplier = get_seasonal_multiplier(start_date, branch_id)
            raw_visits = int(np.random.normal(loc=base_visits, scale=base_visits * 0.4))
            num_visits = int(max(1, raw_visits * seasonal_multiplier))

            # Generate candidate visit dates
            candidate_dates = [
                fake.date_between_dates(date_start=start_date, date_end=min(end_date, END_DATE))
                for _ in range(num_visits * 2)  # Oversample, then filter later
            ]

            # Weight dates by weekday activity
            date_weights = [get_weekday_multiplier(d, branch_id) for d in candidate_dates]

            # Sample final visit dates with weights
            visit_dates = random.choices(candidate_dates, weights=date_weights, k=num_visits)
            visit_dates.sort()

            # Track visits per day
            visits_by_date = {}
            for date in visit_dates:
                visits_by_date.setdefault(date, 0)
                visits_by_date[date] += 1

            # For each visit date
            for visit_date, visit_count in visits_by_date.items():
                prob = random.random()
                if prob < 0.98:
                    max_visits_today = random.randint(1, 2)
                else:
                    max_visits_today = random.randint(3, 5)

                actual_visits_today = min(visit_count, max_visits_today)

                last_checkout_time = None
                for _ in range(actual_visits_today):
                    check_in_time = generate_peak_check_in_time(visit_date, branch_id)

                    # Workout duration logic
                    prob_duration = random.random()
                    if prob_duration < 0.9:
                        workout_duration_second = random.randint(1800, 9000)
                    elif prob_duration < 0.95:
                        workout_duration_second = random.randint(1, 1800)
                    else:
                        workout_duration_second = random.randint(9000, 18000)

                    check_out_time = check_in_time + timedelta(seconds=workout_duration_second)
                    if check_out_time > END_DATE:
                        check_out_time = END_DATE

                    # Rating logic
                    null_probability = branch_null_probability.get(branch_id, 0.55)
                    if random.random() < null_probability:
                        overall_rating = None
                    else:
                        ratings, weights = branch_rating_distribution.get(
                            branch_id,
                            ([5, 4, 3, 2, 1], [0.3, 0.4, 0.2, 0.08, 0.02])
                        )
                        overall_rating = random.choices(ratings, weights=weights, k=1)[0]

                    # Append record
                    check_ins.append({
                        "check_in_id": check_in_id,
                        "member_id": member_id,
                        "check_in_time": check_in_time,
                        "check_out_time": check_out_time,
                        "overall_rating": overall_rating,
                        "branch_id": branch_id
                    })

                    check_in_id += 1

    check_ins_df = pd.DataFrame(check_ins)
    return check_ins_df


if __name__ == "__main__":
    branches_df = pd.read_csv('Branch.csv')
    memberships_df = pd.read_csv('Membership_Type.csv')

    members_df = generate_members_by_branch(branches_df)

    payments_df = generate_payments_by_members(members_df, memberships_df)

    check_ins_df = generate_check_ins_by_payments(payments_df)

    members_df["date_of_birth"] = pd.to_datetime(members_df["date_of_birth"]).dt.date
    members_df["join_date"] = pd.to_datetime(members_df["join_date"]).dt.date
    payments_df["payment_date"]=pd.to_datetime(payments_df["payment_date"]).dt.date
    payments_df["start_date"]=pd.to_datetime(payments_df["start_date"]).dt.date
    payments_df["end_date"]=pd.to_datetime(payments_df["end_date"]).dt.date

members_df.to_csv('0members.csv', index=False)

payments_df.to_csv('0payments.csv', index=False)

check_ins_df.to_csv('0check_ins.csv', index=False)
