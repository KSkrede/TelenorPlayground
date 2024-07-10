import csv
import xml.etree.ElementTree as ET
from datetime import datetime


def parse_xml(filename):
    appointments = []
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
        return None

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
        attendee_list = appointment.find("OPFCalendarEventCopyAttendeeList")
        if attendee_list is not None:
            to_append["Number of Attendees"] = len(
                attendee_list.findall("appointmentAttendee")
            )
        appointments.append(to_append)

    return appointments, fieldnames


def parse_csv(filename):
    parsed_data = []
    with open(filename, mode="r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            start_time = row.get("Start Time", "")
            end_time = row.get("End Time", "")
            date = row.get("Start Date", "")
            required_attendees = row.get("Required Attendees", "").split(";")
            optional_attendees = row.get("Optional Attendees", "").split(";")
            total_attendees = len(required_attendees) + len(optional_attendees)
            parsed_data.append(
                {
                    "Meeting Start Time": start_time,
                    "Meeting End Time": end_time,
                    "Meeting Date": date,
                    "Number of Attendees": total_attendees,
                }
            )

    fieldnames = [
        "Meeting Start Time",
        "Meeting End Time",
        "Meeting Date",
        "Number of Attendees",
    ]
    return parsed_data, fieldnames


def write_csv(output_file, data, fieldnames):
    with open(output_file, mode="w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"Output written to {output_file}")


def main(input_file, output_file):
    if input_file.lower().endswith(".xml"):
        appointments, fieldnames = parse_xml(input_file)
    elif input_file.lower().endswith(".csv"):
        appointments, fieldnames = parse_csv(input_file)
    else:
        print(f"Unsupported file format for {input_file}")
        return

    if appointments:
        write_csv(output_file, appointments, fieldnames)
    else:
        print("No data to write.")


if __name__ == "__main__":
    # input_file = 'Calendar.xml'  # Specify your input file here
    input_file = "Calendar.CSV"  # Specify your input file here
    output_file = "output.csv"  # Specify your desired output file

    main(input_file, output_file)
