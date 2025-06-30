## Canteen Meal Notifier Vidyalaya

## Overview

**Canteen Meal Notifier Vidyalaya** is a Python script designed to periodically scrape canteen menu data from the Vidyalaya website using Selenium, store the data in an SQLite database, and send notifications containing the meal details to a webhook (such as Discord or any compatible service). The script operates on a scheduled basis through a cron job, ensuring the latest canteen meal information is regularly retrieved and sent.

## Features

  -	Scrapes canteen meal data from the Vidyalaya website using Selenium.
  -	Stores the meal data in an SQLite database.
-	Sends meal information as a notification to a specified webhook.
-	Runs periodically using cron jobs for automatic updates.
-	Supports error handling with notifications sent to a designated webhook in case of failure.

## Requirements

  -	Python 3.7+
  -	Web browser driver (e.g., ChromeDriver for Google Chrome)
  -	Selenium
  -	SQLite3 (built-in with Python)
  -	Discord Webhook Python Library (optional for webhook notifications)

## Installation

  **1.	Clone the repository:**

```bash
git clone https://github.com/yourusername/canteen-meal-notifier-vidyalaya.git
cd canteen-meal-notifier-vidyalaya
```


  **2.	Install the dependencies:**
Install the required libraries using pip:

```bash
pip install selenium discord-webhook
```

**3.	Set up the browser driver:**
Download and install ChromeDriver or the appropriate driver for the browser you intend to use with Selenium. Ensure that the driver is accessible in your system’s PATH.
	**4.	Configure the webhook URL (optional):**
Replace the placeholder webhook URLs in the script with your actual webhook URLs.
Example:
```bash
webhookError = DiscordWebhook(url="your-discord-webhook-url")
webhookBatch = DiscordWebhook.create_batch(urls=["your-discord-webhook-url"])
```


## Database

The script uses an SQLite database to store meal data.

  -	The SQLite database file is created automatically if it doesn’t exist.
  -	The database contains a table named canteen with the following structure:
  -	date_field (DATE): The date of the meal.
  -	text_value (TEXT): The meal details.

If the database doesn’t exist when the script is run, it will be created automatically.

## Usage

Running the Script

  **1.	Initial Setup:**
Make sure that the database file (canteen.db) is in the correct directory, or it will be created when the script is executed for the first time.
	**2.	Running the Script:**
To execute the script manually:
```bash
python canteen_meal_notifier.py
```
The script will:
	•	Log in to the Vidyalaya canteen menu page.
	•	Scrape the meal data for the upcoming day.
	•	Store the meal data in the SQLite database.
	•	Check for new records and send a notification to the configured webhook if a new meal record is available.

## Cron Job Setup

To run the script periodically, you can schedule it using a cron job on Linux or Task Scheduler on Windows. Below is an example of setting up a cron job:

  **1.	Open the crontab:**
```bash
crontab -e
```

  **2.	Schedule the script:**
Add the following line to schedule the script to run daily at 2 PM:
```bash
0 14 * * * /usr/bin/python3 /path/to/canteen_meal_notifier.py
```
This will execute the script daily and send the meal data to the webhook.

## Configuration

  -	Vidyalaya Login:
Replace the username and password in the script with your Vidyalaya credentials.
Example:
```bash
driver.find_element(By.ID, 'userNameTextBox').send_keys('your-username')
driver.find_element(By.ID, 'passwordTextBox').send_keys('your-password')
```

  -	Webhook Notifications:
Customize the webhook URL to send the meal data to your desired service. You can use Discord or any other service that supports webhook integration.
	-	Browser Options:
The script is set to run in headless mode by default. You can change this by modifying the options in the script.

options.add_argument('--headless')



## Error Handling

The script sends an error notification to a designated error webhook if it encounters an issue, such as:

  -	Problems connecting to the Vidyalaya website.
  -	Issues with inserting data into the database.

Error notifications contain details of the error, helping you debug the issue.
