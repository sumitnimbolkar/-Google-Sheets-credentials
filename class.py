import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
import requests

# Set up Google Sheets credentials
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# Function to scrape GMB listing details
def scrape_gmb_listing(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract details
        business_name = soup.find('span', class_='SPZz6b').text.strip() if soup.find('span', class_='SPZz6b') else ""
        address = soup.find('span', class_='LrzXr').text.strip() if soup.find('span', class_='LrzXr') else ""
        phone = soup.find('span', class_='zdqRlf').text.strip() if soup.find('span', class_='zdqRlf') else ""
        website = soup.find('a', class_='ABEey')['href'] if soup.find('a', class_='ABEey') else ""

        return business_name, address, phone, website
    except Exception as e:
        print(f"Error: {e}")
        return "", "", "", ""

# Function to update Google Sheet
def update_google_sheet(data, sheet_name):
    try:
        sheet = client.open(sheet_name).sheet1
        sheet.append_row(data)
        print("Data successfully updated in Google Sheet.")
    except Exception as e:
        print(f"Error updating Google Sheet: {e}")

# Main function
def main():
    # Define GMB listing URLs
    urls = [
        'https://www.google.com/maps/place/YourBusiness1',
        'https://www.google.com/maps/place/YourBusiness2',
        # Add more URLs as needed
    ]

    # Create or open a Google Sheet
    sheet_name = 'GMB_Listings'
    headers = ['Business Name', 'Address', 'Phone', 'Website']
    client.create(sheet_name)  # Uncomment if you want to create a new sheet

    # Update headers in Google Sheet
    update_google_sheet(headers, sheet_name)

    # Scrape and update GMB listing details
    for url in urls:
        business_name, address, phone, website = scrape_gmb_listing(url)
        data = [business_name, address, phone, website]
        update_google_sheet(data, sheet_name)

if __name__ == "__main__":
    main()
