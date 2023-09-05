# Marklines Scraper Documentation

This script allows you to scrape data from the Marklines website using Selenium and BeautifulSoup. It logs into the website, navigates through different pages, and extracts relevant data. The scraped data is saved in JSON files for each country and make.

## Prerequisites

- Python 3.x
- Chrome WebDriver for Selenium (make sure it's compatible with your Chrome browser version)
- Required Python packages: selenium, BeautifulSoup

## Usage

1. **Personalize the script**: Replace `your_personal_id` and `your_password` in the script with your actual Marklines login credentials.

2. **Running the script**:

    Open a terminal and navigate to the folder containing the script. Run the following command to execute the script:

    ```
    python script_name.py
    ```

    Replace `script_name.py` with the name of your script.

3. **Output**:

    The script will perform the following steps:

    - Log into the Marklines website using provided credentials.
    - Iterate through a list of nations and their corresponding codes to scrape data.
    - Visit different URLs for each nation to extract data.
    - For each nation, visit various links within the page to collect specific data.
    - Save the collected data as JSON files in the `output_data` folder. Each JSON file is named based on the country and make.

## Script Structure

- `MarklinesScraper` class:
  - Initializes the Selenium WebDriver and stores personal ID and password.
  - Provides methods for login and data scraping.

- `login` method:
  - Navigates to the login URL.
  - Inputs personal ID and password.
  - Logs in and waits for the page to load.

- `scrape_data_by_country` method:
  - Defines a dictionary of nation codes and names.
  - Iterates through nations, navigating to specific URLs for data extraction.
  - Collects links from the page and visits each link for detailed data extraction.

- `scrape_data` method:
  - Loads page source using Selenium.
  - Writes page source to an HTML file.
  - Reads page source from the HTML file using BeautifulSoup.
  - Extracts and processes data from the HTML content.
  - Saves the scraped data as JSON files in the `output_data` folder.

- `if __name__ == '__main__':` block:
  - Initializes the scraper with login credentials.
  - Logs in and initiates the data scraping process.

## Output Folder Structure

- The output JSON files are stored in a folder named `output_data`.
- Subfolders are created within `output_data` for each country using their respective codes.
- JSON files are saved in these subfolders with names based on the make.

## Note

- Be aware of website structure changes that may break the scraping process.
- Ensure you have the Chrome WebDriver installed and compatible with your Chrome browser version.

## Disclaimer

This script is intended for educational purposes and personal use only. Scraping websites without permission may violate their terms of service. Use responsibly and ethically.
