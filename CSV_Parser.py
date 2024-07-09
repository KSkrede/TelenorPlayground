import csv

# Define the input and output file paths
input_file = 'input.csv'
output_file = 'output.csv'

# Read the input CSV file and parse the necessary data
parsed_data = []
with open(input_file, mode='r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        start_time = row["Start Time"]
        end_time = row["End Time"]
        date = row["Start Date"]
        # Count the number of attendees
        required_attendees = row["Required Attendees"].split(';') if row["Required Attendees"] else []
        optional_attendees = row["Optional Attendees"].split(';') if row["Optional Attendees"] else []
        total_attendees = len(required_attendees) + len(optional_attendees)
        parsed_data.append([start_time, end_time, date, total_attendees])

# Write the parsed data to a new CSV file
with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(["Meeting Start Time", "Meeting End Time", "Meeting Date", "Number of Attendees"])
    writer.writerows(parsed_data)

print(f"Parsed data has been written to {output_file}")
