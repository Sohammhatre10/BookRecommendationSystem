import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging

logging.basicConfig(level=logging.INFO)  # Set logging level to INFO

# Function to extract book names and URLs using Selenium
def extract_books(url, genre, max_books=100):
    logging.info(f"Extracting books for genre: {genre}")
    # Set up the Chrome driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(url)

    books = []
    last_height = driver.execute_script("return document.body.scrollHeight")

    try:
        while len(books) < max_books:
            # Scroll down to the bottom of the page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for the page to load

            # Find elements containing the book names and URLs
            elements = driver.find_elements(By.CSS_SELECTOR, 'a.bookTitle[itemprop="url"]')

            for element in elements:
                book_name_element = element.find_element(By.CSS_SELECTOR,
                                                         'span[itemprop="name"][role="heading"][aria-level="4"]')
                book_name = book_name_element.text
                book_url = element.get_attribute('href')

                if book_name and book_url:
                    books.append({'Genre': genre, 'Name': book_name, 'URL': book_url})
                    if len(books) >= max_books:
                        break

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                logging.info(f"Reached the bottom of the page for genre: {genre}")
                break  # Break the loop if no new content is loaded
            last_height = new_height
    except Exception as e:
        logging.error(f"Error occurred while scraping {genre}: {str(e)}")
    finally:
        driver.quit()

    return books

# URLs and genres to scrape
urls_genres = [
    ('https://www.goodreads.com/list/show/114163.Popular_Highly_Rated_Science_Fiction', 'Sci Fiction'),
    ('https://www.goodreads.com/list/show/19312.Horror_The_100_Best_Books', 'Horror'),
    ('https://www.goodreads.com/list/show/514.Best_Action_Adventure_Novels', 'Adventure'),
    ('https://www.goodreads.com/list/show/28259.Best_Historical_Fiction', 'Historical Fiction'),
    ('https://www.goodreads.com/list/show/2441.Best_Fantasy_Books', 'Fantasy'),
    ('https://www.goodreads.com/list/show/1356.Best_Mystery_Thriller_Books', 'Mystery & Thriller'),
    ('https://www.goodreads.com/list/show/324.Most_Heartbreaking_Book_Endings', 'Romance'),
    ('https://www.goodreads.com/list/show/50.The_Best_Epic_Fantasy_fiction', 'Epic Fantasy'),
    ('https://www.goodreads.com/list/show/6029.Best_Books_with_Strong_Female_Lead_Characters', 'Strong Female Leads'),
    ('https://www.goodreads.com/list/show/1483.Best_Science_Fiction_Fantasy_Books', 'Science Fiction & Fantasy'),
    ('https://www.goodreads.com/list/show/6.Best_Books_of_the_20th_Century', 'Classics'),
    ('https://www.goodreads.com/list/show/1375.Best_Children_s_Books_Ever', "Children's"),
    ('https://www.goodreads.com/list/show/2132.Best_Teen_Books_Ever', 'Young Adult'),
    ('https://www.goodreads.com/list/show/11741.Best_Historical_Romance_Novels', 'Historical Romance'),
    ('https://www.goodreads.com/list/show/407.Best_Books_for_Every_Man', 'Books for Every Man'),
    ('https://www.goodreads.com/list/show/29.Best_Books_of_the_21st_Century', '21st Century'),
    ('https://www.goodreads.com/list/show/18.Best_Books_Ever', 'Best Books Ever'),
    ('https://www.goodreads.com/list/show/24876.Best_Science_Books_-_Non-Fiction_Only', 'Science Non-Fiction'),
    ('https://www.goodreads.com/list/show/3147.Best_Travel_Books', 'Travel'),
    ('https://www.goodreads.com/list/show/503.The_Best_Books_of_the_Decade_2000s', '2000s'),
    ('https://www.goodreads.com/list/show/300.Best_History_Books_ancient_and_modern', 'History'),
    ('https://www.goodreads.com/list/show/16927.Best_Books_of_the_2020s', '2020s'),
    ('https://www.goodreads.com/list/show/6980.Best_Food_Memoir_Books', 'Food Memoir'),
    ('https://www.goodreads.com/list/show/13132.Best_Books_of_the_2010s', '2010s'),
    ('https://www.goodreads.com/list/show/1203.Best_Art_Books', 'Art'),
    ('https://www.goodreads.com/list/show/1873.Best_Books_About_Mental_Illness', 'Mental Illness'),
    ('https://www.goodreads.com/list/show/1722.Best_Books_About_Running', 'Running'),
    ('https://www.goodreads.com/list/show/1596.Best_Books_About_Music', 'Music'),
    ('https://www.goodreads.com/list/show/277.Best_Books_of_the_18th_Century', '18th Century'),
    ('https://www.goodreads.com/list/show/11.Best_Books_of_the_19th_Century', '19th Century'),
    ('https://www.goodreads.com/list/show/35.Best_Books_of_the_Decade_1950s', '1950s'),
    ('https://www.goodreads.com/list/show/93.Best_Books_of_the_Decade_1960s', '1960s'),
    ('https://www.goodreads.com/list/show/94.Best_Books_of_the_Decade_1970s', '1970s'),
    ('https://www.goodreads.com/list/show/92.Best_Books_of_the_Decade_1980s', '1980s'),
    ('https://www.goodreads.com/list/show/91.Best_Books_of_the_Decade_1990s', '1990s'),
    ('https://www.goodreads.com/list/show/164.Best_Books_of_the_Decade_2000s', '2000s'),
    ('https://www.goodreads.com/list/show/125.Best_Books_of_the_Decade_2010s', '2010s'),
    ('https://www.goodreads.com/list/show/213.Best_Books_of_the_Decade_2020s', '2020s'),
]

all_books = []
for url, genre in urls_genres:
    books = extract_books(url, genre)
    all_books.extend(books)

# Create a DataFrame from the list of dictionaries
df = pd.DataFrame(all_books)

# Save the DataFrame to a CSV file
csv_file_path = 'books.csv'
df.to_csv(csv_file_path, index=False)

print(f"DataFrame saved to {csv_file_path}")
