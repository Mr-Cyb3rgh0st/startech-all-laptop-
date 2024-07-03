import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


driver = webdriver.Chrome()


wait = WebDriverWait(driver, 60)


data = {"Title": [], "Price": [], "Product Link": []}

try:
    
    for page in range(0, 1):
        url = f"https://www.startech.com.bd/laptop-notebook/laptop?page={page}"
        driver.get(url)
        logger.info(f"Accessing page: {url}")
        
        
        items = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='p-item']")))
        logger.info(f"Found {len(items)} items on page {page}")
        
        
        for item in items:
            try:
                title = item.find_element(By.XPATH, ".//h4").text
                price = item.find_element(By.XPATH, ".//div[@class='p-item-price']//span[1]").text
                price = price.replace("৳", " BDT")
                link_element = item.find_element(By.XPATH, ".//a")
                link = link_element.get_attribute("href")
                
                data["Title"].append(title)
                data["Price"].append(price)
                data["Product Link"].append(link)
                
                logger.info(f"Extracted data - Title: {title}, Price: {price}, Link: {link}")
            except Exception as item_exception:
                logger.error(f"Error extracting data from item: {item_exception}")
        
        
        time.sleep(2)

except Exception as e:
    logger.error(f"An error occurred: {e}")

finally:

    driver.quit()


data_frame = pd.DataFrame(data)
data_frame.to_csv("startech.csv", index=False)
logger.info("Data saved to startech.csv")
