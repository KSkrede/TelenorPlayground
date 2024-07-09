import os
import csv
import xml.etree.ElementTree as ET
from datetime import datetime

# Define the input and output file paths
input_file = 'input.csv'
output_file = 'output.csv'


appointments = []
filename = "Calendar.xml"
fieldnames = [
    "Meeting Start Time",
    "Meeting End Time",
    "Meeting Date",
    "Number of Attendees",
]

try:
    tree = ET.parse(filename)
except Exception as e:
    print(f"{filename} couldn't be parsed: {e}")
    exit()

root = tree.getroot()
for appointment in root.iter("appointment"):
    to_append = {}
    if appointment.find("OPFCalendarEventCopyStartTime") is not None:
        start_time_str = appointment.find("OPFCalendarEventCopyStartTime").text
        start_time = datetime.fromisoformat(start_time_str)
        to_append["Meeting Start Time"] = start_time.strftime("%H:%M:%S")
        to_append["Meeting Date"] = start_time.strftime("%d.%m.%Y")
    if appointment.find("OPFCalendarEventCopyEndTime") is not None:
        end_time_str = appointment.find("OPFCalendarEventCopyEndTime").text
        end_time = datetime.fromisoformat(end_time_str)
        to_append["Meeting End Time"] = end_time.strftime("%H:%M:%S")
    to_append["Number of Attendees"] = 0
    attendeeList = appointment.find("OPFCalendarEventCopyAttendeeList")
    if attendeeList is not None:
        to_append["Number of Attendees"] = len(attendeeList.findall("appointmentAttendee"))
    appointments.append(to_append)

# Write the CSV file with UTF-8 encoding
with open("output2.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fieldnames, dialect="excel-tab")
    w.writeheader()
    w.writerows(appointments)

print("operation completed")
