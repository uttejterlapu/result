import requests
from bs4 import BeautifulSoup
import urllib3
import csv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
base_url = "https://onlinecertificates.gitam.edu/View_Result_Grid2.aspx?QT=QRCODE$VU21CSEN0400"

# List to store the results
results = []

for i in range(1, 265):
    url = f"{base_url}{str(i).zfill(3)}$5$nov$2023$R$"
    response = requests.get(url, verify=False)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        lblname_tag = soup.find("span", {"id": "lblname"})
        lblgpa_tag = soup.find("span", {"id": "lblgpa"})
        lblcgpa_tag = soup.find("span", {"id": "lblcgpa"})

        # Check if the name is not equal to "lblname"
        if lblname_tag and lblname_tag.text != "lblname":
            # Store the results in a dictionary
            result_data = {
                "Roll Number": str(i).zfill(3),
                "Name": lblname_tag.text if lblname_tag else "N/A",
                "GPA": lblgpa_tag.text if lblgpa_tag else "N/A",
                "CGPA": lblcgpa_tag.text if lblcgpa_tag else "N/A",
                "URL": url
            }

            # Append the result to the list
            results.append(result_data)

    else:
        print(f"Failed to retrieve the page for URL {url}. Status code: {response.status_code}")

# Write the filtered results to a CSV file
csv_file_path = "filtered_results_with_url.csv"
fieldnames = ["Roll Number", "Name", "GPA", "CGPA", "URL"]

with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    # Write the header row
    writer.writeheader()

    # Write the filtered results
    writer.writerows(results)

print(f"Filtered results with URL written to {csv_file_path}")
