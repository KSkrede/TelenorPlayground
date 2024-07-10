import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, time

# Load the CSV data
data = pd.read_csv('output.csv')

# Combine Date and Time columns to form datetime columns
data['Meeting Date'] = pd.to_datetime(data['Meeting Date'], format='%d.%m.%Y')
data['Start Time'] = data.apply(lambda row: datetime.combine(row['Meeting Date'], datetime.strptime(row['Meeting Start Time'], '%H:%M:%S').time()), axis=1)
data['End Time'] = data.apply(lambda row: datetime.combine(row['Meeting Date'], datetime.strptime(row['Meeting End Time'], '%H:%M:%S').time()), axis=1)

# Define working hours and lunch break
work_start_time = time(8, 0, 0)
lunch_start_time = time(11, 0, 0)
lunch_end_time = time(12, 0, 0)
work_end_time = time(16, 0, 0)

# Create a list of all weekdays in the date range
all_dates = pd.date_range(start=data['Meeting Date'].min(), end=data['Meeting Date'].max(), freq='B')

# Initialize deep focus times dictionary
deep_focus_dict = {day: 7 for day in all_dates}

# Process the data to find deep focus periods each day
for day, day_data in data.groupby(data['Meeting Date']):
    # Skip weekends (just to be sure, though we should not have them in `all_dates`)
    if day.weekday() >= 5:  # 5 is Saturday, 6 is Sunday
        continue
    
    # Sort by start time
    day_data = day_data.sort_values(by='Start Time')
    
    # Initialize variables
    deep_focus_time = timedelta(0)
    last_end_time = datetime.combine(day, work_start_time)
    end_of_working_day = datetime.combine(day, work_end_time)
    lunch_start = datetime.combine(day, lunch_start_time)
    lunch_end = datetime.combine(day, lunch_end_time)
    
    for _, row in day_data.iterrows():
        start_time = max(row['Start Time'], datetime.combine(day, work_start_time))
        end_time = min(row['End Time'], end_of_working_day)
        
        if start_time >= end_of_working_day:
            break
        
        if last_end_time < start_time:
            # If the gap crosses the lunch break, split the gap
            if last_end_time < lunch_start and start_time > lunch_end:
                gap_before_lunch = lunch_start - last_end_time
                gap_after_lunch = start_time - lunch_end
                if gap_before_lunch > timedelta(minutes=30):
                    deep_focus_time += gap_before_lunch - timedelta(minutes=30)
                if gap_after_lunch > timedelta(minutes=30):
                    deep_focus_time += gap_after_lunch - timedelta(minutes=30)
            else:
                gap = start_time - last_end_time
                if gap > timedelta(minutes=30):
                    deep_focus_time += gap - timedelta(minutes=30)
        
        last_end_time = max(last_end_time, end_time)
    
    # If there is time left in the working day after the last meeting
    if last_end_time < end_of_working_day:
        if last_end_time < lunch_start:
            gap_before_lunch = lunch_start - last_end_time
            if gap_before_lunch > timedelta(minutes=30):
                deep_focus_time += gap_before_lunch - timedelta(minutes=30)
            gap_after_lunch = end_of_working_day - lunch_end
            if gap_after_lunch > timedelta(minutes=30):
                deep_focus_time += gap_after_lunch - timedelta(minutes=30)
        elif last_end_time > lunch_end:
            gap = end_of_working_day - last_end_time
            if gap > timedelta(minutes=30):
                deep_focus_time += gap - timedelta(minutes=30)
    
    # Convert deep focus time to minutes and add to the deep focus dictionary
    deep_focus_dict[day] = deep_focus_time.total_seconds() // 60  # Convert to minutes (integer)

# Convert dictionary to DataFrame for visualization
deep_focus_df = pd.DataFrame(list(deep_focus_dict.items()), columns=['Date', 'Deep Focus Minutes'])

# Export deep_focus_df to file
deep_focus_df = deep_focus_df.sort_values(by='Date')

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(deep_focus_df['Date'], deep_focus_df['Deep Focus Minutes'] / 60, marker='o', linestyle='')
plt.title('Deep Focus Time by Day (08:00 - 16:00, excluding 11:00 - 12:00 lunch break)')
plt.xlabel('Date')
plt.ylabel('Deep Focus Hours')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
