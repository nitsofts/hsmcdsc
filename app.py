from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

# Helper function to scrape and format the data
def scrape_cdsc_data():
    # Define the URL of the website
    url = "https://www.cdsc.com.np/"

    # Send an HTTP request to the website with SSL certificate verification disabled
    response = requests.get(url, verify=False)

    # Parse the HTML content of the website
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")

    # Locate the div containing the "Current Public Issue" information
    div = soup.find("div", class_="fun-factor-area")

    # Extract all the "h4" elements from the "fun-custom-column" div
    h4_elements = div.find_all("h4")

    # Create a list to store the extracted data in the new format
    data = []

    # Format and add the data to the list
    for i in range(0, len(h4_elements), 2):
        item = {
            "id": str(int(i/2)),  # ID as a string
            "dataKey": h4_elements[i + 1].text.strip(),
            "dataValue": h4_elements[i].text.strip()
        }
        data.append(item)

    return data

@app.route('/get_cdsc_data', methods=['GET'])
def get_cdsc_data():
    # Call the helper function to scrape the data
    cdsc_data = scrape_cdsc_data()

    # Return the scraped data in JSON format
    return jsonify(cdsc_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
