from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from datetime import date, datetime, timedelta
from discord_webhook import DiscordWebhook, DiscordEmbed
import sqlite3
import os
import requests
#import pickle # used to save and load cookies

# Check if Database Exists:
webhookError = DiscordWebhook(url="https://discord.com/api/webhooks/1199953897389826152/Lxw2-gbfR7MuPiZB9n0mOva9XNkP1RBFU2gaZvx3aPXq153MFcaPyzpY0sFJqHZqgjIg")
webhookBatch = DiscordWebhook.create_batch(urls=["https://discord.com/api/webhooks/1199953897389826152/Lxw2-gbfR7MuPiZB9n0mOva9XNkP1RBFU2gaZvx3aPXq153MFcaPyzpY0sFJqHZqgjIg", "https://discord.com/api/webhooks/1203032557159977060/QBlPTZH-CJy8kLyatxI5OKNu8wZkgDEzH041QmZiRroKzXp2DStMZkaU5WP7FLM9J0Kq"])
database_path = '/Canteen-Meal-Notifer-Vidyalaya/canteen.db'

def errorOccoured(e):
    embed = DiscordEmbed(title=f'Error', description=e, color="880808")
    webhookError.add_embed(embed)
    response = webhookError.execute()

def convert_date_format(date_str):
    return datetime.strptime(date_str, '%d/%m/%Y').strftime('%Y-%m-%d')

def format_food(food_string):
    # Split the string by new lines
    items = food_string.split('\n')
    # Capitalize each item and format as a numbered list
    formatted_items = [f"{idx + 1}) {item.title()}" for idx, item in enumerate(items)]
    # Join the list back into a single string
    formatted_string = '\n'.join(formatted_items)
    return formatted_string

def getFood():
    options = webdriver.ChromeOptions()
    #options.add_argument("--user-data-dir=/Users/aadils/Library/Application Support/Google/Chrome/Profile 1")
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')  # Bypass OS security model, MUST be the very first option
    options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get("https://nhss.onlinevidyalaya.net/Pages/StudentManagement/CanteenMenu.aspx")

    if driver.current_url == 'https://nhss.onlinevidyalaya.net/Pages/BaseFramework/Security/Login.aspx?OrgGroupId=1965' or driver.title == 'Login':
        print('Login Page')
        driver.find_element(By.ID, 'userNameTextBox').send_keys('13134b')
        driver.find_element(By.ID, 'passwordTextBox').send_keys('aadil2112')
        driver.find_element(By.ID, 'chkRememberMe').click()
        driver.find_element(By.ID, 'loginButton').click()

        driver.get("https://nhss.onlinevidyalaya.net/Pages/StudentManagement/CanteenMenu.aspx")
    else:
        print('Already Logged in')
    select_canteen = driver.find_element(By.ID, 'ctl00_CP_SelectCanteenDropDownList')
    selectCanteen = Select(select_canteen)
    selectCanteen.select_by_visible_text('NSS-CANTEEN')
    time.sleep(1)
    select_break = driver.find_element(By.ID, 'ctl00_CP_BreakTypeDropDownList')
    selectBreak = Select(select_break)
    selectBreak.select_by_visible_text('Lunch Break')
    time.sleep(0.5)
    driver.find_element(By.ID, 'ctl00_CP_SearchButton').click()

    today = date.today()
    d1 = int(today.strftime("%d")) + 1
    d2 = (today.strftime(f'{d1}/%m/%y'))
    print(d1)
    time.sleep(0.5)
    foodTable = driver.find_element(By.ID,'ctl00_CP_FoodItemMasterGridView').find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')#[d1].find_elements(By.TAG_NAME, 'td')[4].find_element(By.TAG_NAME, 'textarea').get_attribute('innerHTML')
    data = []
    for i in foodTable[1:]:
        dat1 = i.find_elements(By.TAG_NAME, 'td')[0].find_element(By.TAG_NAME, 'span').get_attribute('innerHTML')
        food1 = i.find_elements(By.TAG_NAME, 'td')[4].find_element(By.TAG_NAME, 'textarea').get_attribute('innerHTML')
        dayFood = {"date": dat1, "food": food1}
        data.append(dayFood)
    print(data)
    time.sleep(0.5)
    driver.quit()

    # Save the food to the database
    sql_insert_query = "INSERT INTO canteen (date_field, text_value) VALUES (?, ?)"
    try:
        for item in data:
            date_formatted = convert_date_format(item['date'])
            cursor.execute(sql_insert_query, (date_formatted, format_food(item['food'])))
        conn.commit()
        print(f"Successfully inserted {len(data)} records into the database.")
        return True
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        errorOccoured(e)
        conn.rollback()


# Main
        
# Check if the SQLite database exists
if not os.path.exists(database_path):
    conn = sqlite3.connect(database_path)
    print(f"Database {database_path} created successfully.")
    try:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS canteen (
                date_field DATE PRIMARY KEY,
                text_value TEXT NOT NULL
            );
        ''')
        print("Table created successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        errorOccoured(e)
else:
    conn = sqlite3.connect(database_path)
    print(f"Database {database_path} exists and connected successfully.")

# Search the database for a record with today's date
datee = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
sql_query = "SELECT * FROM canteen WHERE date_field = ?"
cursor = conn.cursor()
try:
    cursor.execute(sql_query, (datee,))
    result = cursor.fetchone()
    if result:
        print("Found a record for tmrw's date:", result)
    else:
        print("No record found for tmrw's date. Running the web scraper.")
        result = getFood()
        if result:
            cursor.execute(sql_query, (datee,))
            result = cursor.fetchone()
            print("Found a record for tmrw's date:", result)
        else:
            print("Failed to get food from the website.")
            errorOccoured("Failed to get food from the website.")
            exit()

except sqlite3.Error as e:
    print(f"An error occurred: {e}")
    errorOccoured(e)

print(result)
cursor.close()
conn.close()

if result[1] == 'HOLIDAY':
    exit()

embed = DiscordEmbed(title="Navrachana Sama Canteen Bot", description=f'''
    **Date:** {result[0]}
    **Food:** 
    {result[1]}

    Made with ❤️ by Aadil :)
''', color="03b2f8")

for i in webhookBatch:
    i.add_embed(embed)
    response = i.execute()

requests.post("http://localhost:3000/send/message", {'phone':'120363295006728236','message':f'''*Navrachana Sama Canteen Bot*

*Date:* {result[0]}
*Food:*
{result[1]}

Made with ❤️ by Aadil :)'''})
