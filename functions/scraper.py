import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from ics import Calendar, Event
from datetime import datetime
import time
import json
import os

OUTPUT_DIR = "H:\PythonProject\Scraper\gemini-calendar-app\public"

def create_ics_file(calendar_name, events_data):
    c = Calendar()
    for event_data in events_data:
        e = Event()
        e.name = event_data["Event Details"].strip()
        # Parsing date which may include day range like "Jul 19 - 21, 2025"
        date_str = event_data["Date"].split("-")[0].strip()
        # Remove any non-breaking space characters
        date_str = date_str.replace("\u2013", "-").replace("\u2014", "-")
        # Add the year to the date string
        if "," not in date_str:
            date_str += ", 2025"
        # Handle date ranges like "Feb 18 - 20, 2025"
        if " " in date_str and "-" in date_str:
            parts = date_str.split(" ")
            if len(parts) > 2:
                date_str = f"{parts[0]} {parts[1]}, {parts[-1]}"

        try:
            start_date = datetime.strptime(date_str, "%b %d, %Y")
        except ValueError:
            try:
                start_date = datetime.strptime(date_str, "%B %d, %Y")
            except ValueError:
                print(f"Could not parse date: {date_str}")
                continue

        e.begin = start_date
        e.make_all_day()
        c.events.add(e)
    
    file_name = f"{calendar_name}.ics"
    file_path = os.path.join(OUTPUT_DIR, file_name)
    with open(file_path, "w") as f:
        f.writelines(c)
    return file_name

def scrape_calendar():
    driver = None
    calendars_data = []
    try:
        options = uc.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        driver = uc.Chrome(version_main=138, options=options)
        url = "https://www.uiu.ac.bd/academics/calendar/"
        driver.get(url)
        
        time.sleep(15)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        accordions = soup.find_all("div", class_="calender-item")

        for accordion in accordions:
            title_element = accordion.find("summary")
            if title_element:
                title = title_element.text.strip().replace("/", "_").replace(" ", "_")
                table = accordion.find("table")
                if table:
                    events_data = []
                    for row in table.find_all("tr"):
                        cells = row.find_all("td")
                        if len(cells) == 3:
                            event_info = {
                                "Date": cells[0].text.strip(),
                                "Day": cells[1].text.strip(),
                                "Event Details": cells[2].text.strip(),
                            }
                            events_data.append(event_info)
                    if events_data:
                        ics_file_name = create_ics_file(title, events_data)
                        calendars_data.append({
                            "name": title.replace("_", " "),
                            "file": ics_file_name
                        })
                        print(f"Created {ics_file_name}")
        
        # Write calendars_data to a JSON file
        json_output_path = os.path.join(OUTPUT_DIR, "calendars.json")
        with open(json_output_path, "w") as f:
            json.dump(calendars_data, f, indent=2)
        print(f"Created calendars.json at {json_output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    scrape_calendar()