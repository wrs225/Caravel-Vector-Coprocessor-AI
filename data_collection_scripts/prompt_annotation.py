import os
import csv
from colorama import Fore, Style

# Get the current working directory
cwd = os.getcwd()

# Get all folders in the current working directory
folders = [f for f in os.listdir(cwd) if os.path.isdir(os.path.join(cwd, f))]

for folder in folders:
    # Get the CSV file in the folder
    csv_file = [f for f in os.listdir(os.path.join(cwd, folder)) if f.endswith(".csv")][
        0
    ]
    csv_file_path = os.path.join(cwd, folder, csv_file)

    # Read the CSV file and store the rows
    with open(csv_file_path, "r") as csvfile:
        reader = csv.reader(csvfile)
        rows = [row for row in reader]

    if rows:
        rows[0].append("annotation")

    with open(csv_file_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)
    # Iterate over the files in the folder
    print(rows[0])
    for i in range(len(rows)):
        print(rows[i])
        file_path = os.path.join(cwd, folder, f"prompt_{i}.txt")
        print(file_path)
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                print(Fore.GREEN + file.read() + Style.RESET_ALL)
            print(
                Fore.YELLOW
                + "Please enter your annotation for this file: "
                + Style.RESET_ALL,
                end="",
            )
            annotation = input()
            if annotation == None:
                annotation = "none"
            rows[i + 1].append(annotation)

        # Write the updated rows back to the CSV file
        with open(csv_file_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rows)
