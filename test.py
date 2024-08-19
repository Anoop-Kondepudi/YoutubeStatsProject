from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime, timedelta

# Step 1: Set up the Chrome WebDriver
# Replace this with the path to your ChromeDriver executable
driver = webdriver.Chrome('C:/Program Files/Google/Chrome/Application/chrome.exe')

# Step 2: Log in to YouTube
driver.get("https://accounts.google.com/signin/v2/identifier?service=youtube")
time.sleep(3)

# Enter email
email_elem = driver.find_element_by_name("identifier")
email_elem.send_keys("mcbatmangaminghere@gmail.com")
email_elem.send_keys(Keys.RETURN)
time.sleep(2)

# Enter password (adjust waiting times if needed)
password_elem = driver.find_element_by_name("password")
password_elem.send_keys("poonA*2005")
password_elem.send_keys(Keys.RETURN)
time.sleep(5)

# Step 3: Navigate to YouTube watch history
driver.get("https://www.youtube.com/feed/history")
time.sleep(5)

# Step 4: Scroll down to load enough history (or use a more sophisticated scroll loop)
for _ in range(10):
    driver.find_element_by_tag_name('body').send_keys(Keys.END)
    time.sleep(2)

# Step 5: Scrape video titles and durations
video_elems = driver.find_elements_by_xpath("//ytd-video-renderer//span[@id='text' and contains(text(),'minutes')]")

watch_times = []

for video_elem in video_elems:
    video_text = video_elem.text  # Extract duration text
    # Assuming the text is in the format "X minutes" or "X hours Y minutes"
    time_parts = video_text.split()
    total_minutes = 0
    
    if "hours" in time_parts:
        total_minutes += int(time_parts[0]) * 60
    if "minutes" in time_parts:
        total_minutes += int(time_parts[-2])
    
    watch_times.append(total_minutes)

# Step 6: Calculate total watch time
total_watch_time_hours = sum(watch_times) / 60
print(f"Total watch time over the past 7 days: {total_watch_time_hours:.2f} hours")

driver.quit()
