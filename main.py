from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time, json
import os


class MarklinesScraper:
    def __init__(self, personal_id, password):
        options = Options()
        options.add_argument('-start-maximized')
        self.driver = webdriver.Chrome(options=options)
        self.personal_id = personal_id
        self.password = password
        pass

    def login(self):
        # Navigate to the login URL
        self.driver.get("https://www.marklines.com/en/members/login")

        try:
            # Wait for the login page to load
            element_present = EC.presence_of_element_located((By.ID, 'profiles_login_login_id'))
            WebDriverWait(self.driver, 10).until(element_present)

            # Find the Personal ID and Password fields
            personal_id_field = self.driver.find_element(By.ID, 'profiles_login_login_id')
            password_field = self.driver.find_element(By.ID, 'profiles_login_password')

            # Input the Personal ID and Password
            personal_id_field.send_keys(self.personal_id)
            password_field.send_keys(self.password)

            # Find the login button and click it
            login_button = self.driver.find_element(By.ID, 'login_btn')
            login_button.click()
            time.sleep(5)
        except Exception as e:
            print(f"An error occurred: {e}")
            
        
    def scrape_data_by_country(self):
        nation_codes = {
            "United_States": "USA",
            "Canada": "CAN",
            "Mexico": "MEX",
            "Brazil": "BRA",
            "Argentina": "ARG",
            "Colombia": "COL",
            "Chile": "CHL",
            "Uruguay": "URY",
            "Germany": "DEU",
            "UK": "GBR",
            "France": "FRA",
            "Italy": "ITA",
            "Spain": "ESP",
            "Portugal": "PRT",
            "Belgium": "BEL",
            "Netherlands": "NLD",
            "Austria": "AUT",
            "Switzerland": "CHE",
            "Ireland": "IRL",
            "Sweden": "SWE",
            "Norway": "NOR",
            "Finland": "FIN",
            "Denmark": "DNK",
            "Greece": "GRC",
            "Luxembourg": "LUX",
            "Japan": "JPN",
            "China": "CHN",
            "India": "IND",
            "Thailand": "THA",
            "Korea": "KOR",
            "Indonesia": "IDN",
            "Malaysia": "MYS",
            "Vietnam": "VNM",
            "Taiwan": "TWN",
            "Singapore": "SGP",
            "Pakistan": "PAK",
            "Philippines": "PHL",
            "Myanmar": "MMR",
            "Australia": "AUS",
            "New_Zealand": "NZL",
            "Russia": "RUS",
            "Turkey": "TUR",
            "Poland": "POL",
            "Czech_Rep": "CZE",
            "Ukraine": "UKR",
            "Romania": "ROM",
            "Slovakia": "SVK",
            "Uzbekistan": "UZB",
            "Croatia": "HRV",
            "Belarus": "BLR",
            "Hungary": "HUN",
            "Slovenia": "SVN",
            "Bulgaria": "BGR",
            "Kazakhstan": "KAZ",
            "Estonia": "EST",
            "South_Africa": "ZAF",
            "Egypt": "EGY",
            "Israel": "ISR",
            "UAE": "ARE",
            "Saudi_Arabia": "SAU",
            "Kuwait": "KWT",
            "Oman": "OMN"
        }


        for country, code in nation_codes.items():
            print(f"Getting data for country - {country}")
            url = f"https://www.marklines.com/en/vehicle_sales/year?nationCode={code}&fromYear=2000&toYear=2023"
            self.driver.get(url)

            try:
                # Wait for the table to load
                element_present = EC.presence_of_element_located((By.XPATH, '//th[@class="aggregate_row_header"]'))
                WebDriverWait(self.driver, 10).until(element_present)
                

                # Get all the relevant links
                elements = self.driver.find_elements(By.XPATH, '//th[@class="aggregate_row_header"]/a')
                links = [element.get_attribute("href") for element in elements]
                
                # Visit each link
                for i, link in enumerate(links):
                    print(f"Getting link({i}) of {len(links)} for country {country}")
                    time.sleep(3)
                    self.scrape_data(link, code)
                    time.sleep(30)
                    
                    # Here you can add whatever you want to do on the individual pages
            except Exception as e:
                print(f"An error occurred during data scraping for {country}: {e}")
                
                
    def scrape_data(self, link, code):
        print(link)
        self.driver.get(link)
        # Wait for the table to load
        time.sleep(5)
        
        page_source = self.driver.page_source
        # Save the page source to an HTML file
        with open('page_source.html', 'w', encoding='utf-8') as file:
            file.write(page_source)
            
        time.sleep(5)
        with open('page_source.html', 'r', encoding='utf-8') as file:
            page_source_in = file.read()
            
        soup = BeautifulSoup(page_source_in, 'html.parser')
        # Here you can add whatever you want to do with the page source
        time.sleep(2)

        tbody_elements = soup.find_all('tbody')

        # Select the second <tbody> element
        if len(tbody_elements) >= 2:
            body = tbody_elements[1]
        else:
            print("No second <tbody> element found!")
            return

        # Initialize empty list to hold scraped data
        scraped_data = []
        make = ""
        _type = ""
        model = ""
        segment = ""

        # Loop through table rows
        for row in body.find_all('tr'):
            level_0 = row.find('th', class_='aggregate_header level-0')
            level_1 = row.find('th', class_='aggregate_header level-1')
            level_2 = row.find('th', class_='aggregate_header level-2')
            level_3 = row.find('th', class_='aggregate_header level-3')
            level_4 = row.find('th', class_='aggregate_header level-4')
            agg_head = row.find('th', class_='aggregate_row_header')
            col = row.find_all('td', class_='aggregate_column')
            hierarchy = row.find('th', class_='hierarchy-1')

            if hierarchy:
                continue

            if level_1:
                make = level_1.string

            if level_2 and _type != level_2.string:
                _type = level_2.string

            if level_3 and segment != level_3.string:
                segment = level_3.string

            if level_4 and model != level_4.string:
                model = level_4.string

            if col:
                sales = {}
                for i, n in enumerate(col):
                    if n.get_text(strip=True) == "-" or n.get_text(strip=True) == "N/A" :
                        sales[2000 + i] = 0
                    else:
                        sales[2000 + i] = int(n.get_text(strip=True).replace(",", ""))

            # Append a dictionary to the list
            scraped_data.append({
                "country": "USA",
                "make": make.replace("\n","").replace("\t",""),
                "model": model.replace("\n","").replace("\t",""),
                "type": _type.replace("\n","").replace("\t",""),
                "segment": segment.replace("\n","").replace("\t",""),
                "powertrain": agg_head.string.replace("\n","").replace("\t","") if agg_head else None,
                "sales": sales
            })
            

        # Output the scraped data as JSON
        output_folder = "output_data"  # Change this to your desired output folder
        make = make.replace("\n","").replace("\t","")
        country_filename = os.path.join(output_folder, f"{code}/{make}.json")
        print(f"{code}/{make}.json done successfully!")
        
        # Create the folder if it doesn't exist
        os.makedirs(os.path.dirname(country_filename), exist_ok=True)
        
        with open(country_filename, 'w', encoding='utf-8') as outfile:
            json.dump(scraped_data, outfile, indent=4)


if __name__ == '__main__':
    # Replace 'your_personal_id' and 'your_password' with the actual ID and password
    scraper = MarklinesScraper('your_personal_id', 'your_password')
    scraper.login()
    scraper.scrape_data_by_country()
