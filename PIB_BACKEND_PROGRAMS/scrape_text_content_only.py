import requests
from bs4 import BeautifulSoup

# Replace 'https://example.com' with the URL of the website you want to scrape
url = 'https://www.indiatoday.in/india'

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find and extract all text content
    text_content = soup.get_text()

    # Print or save the extracted text content

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text_content.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    print(text)

else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")