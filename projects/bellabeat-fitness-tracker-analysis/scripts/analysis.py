import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set aesthetic style for plots
sns.set_theme(style="whitegrid")

# Load datasets
data_dir = '../data/'
daily_activity = pd.read_csv(os.path.join(data_dir, 'dailyActivity_merged.csv'))
sleep_day = pd.read_csv(os.path.join(data_dir, 'sleepDay_merged.csv'))

# Data Cleaning & Transformation
# Convert ActivityDate to datetime
daily_activity['ActivityDate'] = pd.to_datetime(daily_activity['ActivityDate'])
sleep_day['SleepDay'] = pd.to_datetime(sleep_day['SleepDay'])

# Check for duplicates
print(f"Daily Activity Duplicates: {daily_activity.duplicated().sum()}")
print(f"Sleep Day Duplicates: {sleep_day.duplicated().sum()}")

# Drop duplicates in sleep_day
sleep_day = sleep_day.drop_duplicates()

# Merge datasets on Id and Date
# For sleep_day, the date column is SleepDay. For daily_activity, it's ActivityDate.
daily_activity['Date'] = daily_activity['ActivityDate']
sleep_day['Date'] = sleep_day['SleepDay']

merged_data = pd.merge(daily_activity, sleep_day, on=['Id', 'Date'], how='inner')

# Feature Engineering
# Calculate total active minutes
merged_data['TotalActiveMinutes'] = merged_data['VeryActiveMinutes'] + merged_data['FairlyActiveMinutes'] + merged_data['LightlyActiveMinutes']

# Categorize users by activity level
def activity_category(steps):
    if steps < 5000:
        return 'Sedentary'
    elif steps < 7500:
        return 'Lightly Active'
    elif steps < 10000:
        return 'Fairly Active'
    else:
        return 'Very Active'

merged_data['UserType'] = merged_data['TotalSteps'].apply(activity_category)

# Analysis & Visualizations
output_dir = '../visualizations/'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 1. Total Steps vs Calories
plt.figure(figsize=(10, 6))
sns.scatterplot(data=merged_data, x='TotalSteps', y='Calories', hue='UserType', palette='viridis')
plt.title('Relationship between Total Steps and Calories Burned')
plt.xlabel('Total Steps')
plt.ylabel('Calories')
plt.savefig(os.path.join(output_dir, 'steps_vs_calories.png'))
plt.close()

# 2. Total Minutes Asleep vs Total Time in Bed
plt.figure(figsize=(10, 6))
sns.regplot(data=merged_data, x='TotalTimeInBed', y='TotalMinutesAsleep', scatter_kws={'alpha':0.5})
plt.title('Total Time in Bed vs Total Minutes Asleep')
plt.xlabel('Total Time in Bed (min)')
plt.ylabel('Total Minutes Asleep (min)')
plt.savefig(os.path.join(output_dir, 'bed_vs_sleep.png'))
plt.close()

# 3. Distribution of User Types
plt.figure(figsize=(8, 8))
user_type_counts = merged_data['UserType'].value_counts()
plt.pie(user_type_counts, labels=user_type_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
plt.title('Distribution of User Activity Levels')
plt.savefig(os.path.join(output_dir, 'user_type_distribution.png'))
plt.close()

# 4. Average Steps by Day of the Week
merged_data['DayOfWeek'] = merged_data['Date'].dt.day_name()
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
avg_steps_day = merged_data.groupby('DayOfWeek')['TotalSteps'].mean().reindex(day_order)

plt.figure(figsize=(10, 6))
sns.barplot(x=avg_steps_day.index, y=avg_steps_day.values, palette='magma')
plt.title('Average Total Steps by Day of the Week')
plt.xlabel('Day of the Week')
plt.ylabel('Average Steps')
plt.savefig(os.path.join(output_dir, 'avg_steps_by_day.png'))
plt.close()

# Summary Statistics for README
summary_stats = merged_data.describe()
summary_stats.to_csv('../docs/summary_statistics.csv')

print("Analysis complete. Visualizations and summary statistics saved.")
