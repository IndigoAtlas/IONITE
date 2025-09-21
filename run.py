

import requests
# Importing required library
import pygsheets

template_str = ""

# Create the Client
# Enter the name of the downloaded KEYS 
# file in service_account_file
client = pygsheets.authorize(service_account_file="ionite-472813-3f097b8874d0.json")

# Sample command to verify successful
# authorization of pygsheets
# Prints the names of the spreadsheet
# shared with or owned by the service 
# account
print(client.spreadsheet_titles())

def mod(row: int):
   # opens a spreadsheet by its name/title
    spreadsht = client.open("IONITE")

    # opens a worksheet by its name/title
    worksht = spreadsht.worksheet("title", "Sheet1")
    # should be in a matrix format
    worksht.update_value(f'D{row}', '0')



    

def gsheet_to_csv(sheet_url_or_id: str, output_filename: str = "output.csv"):
    """
    Downloads a Google Sheet as CSV and saves it to Google Colab's local file system.

    Args:
        sheet_url_or_id (str): Either the full Google Sheets URL or just the Sheet ID.
        output_filename (str): The name of the output CSV file in Colab (default: 'output.csv').
    """
    import re
    import pandas as pd

    # If full URL provided, extract the sheet ID
    match = re.search(r"/d/([a-zA-Z0-9-_]+)", sheet_url_or_id)
    if match:
        sheet_id = match.group(1)
    else:
        sheet_id = sheet_url_or_id  # assume it's already just the ID

    # By default, export the first sheet as CSV
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

    # Read directly into pandas
    df = pd.read_csv(csv_url)

    # Save to CSV in Colab's local files
    df.to_csv(output_filename, index=False)

    print(f"✅ Saved Google Sheet as {output_filename} in Colab files.")


# Example usage:
# gsheet_to_csv("https://docs.google.com/spreadsheets/d/1abc123XYZ456/edit#gid=0", "my_data.csv")

from datetime import datetime

def is_not_in_past(date_string):
    """
    Checks if a date string in "YYYYMMDD" format is not in the past.

    Args:
        date_string (str): The date string in "YYYYMMDD" format.

    Returns:
        bool: True if the date is not in the past (today or future), False otherwise.
              Returns False if the date string is not in the correct format.
    """
    try:
        # Parse the input date string into a datetime object
        input_date = datetime.strptime(date_string, "%Y%m%d")

        # Get the current date (without time component for comparison)
        current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # Compare the input date with the current date
        return input_date >= current_date
    except ValueError:
        # Handle cases where the date_string is not in the expected format
        return False

def send(sender_email, sender_password, recipient_email, subject, body):
    """
    Send an email using SMTP (Gmail server).
    
    Args:
        sender_email (str): The sender's email address.
        sender_password (str): The sender's email password or app password.
        recipient_email (str): The recipient's email address.
        subject (str): The subject of the email.
        body (str): The plain text body of the email.
    """
    import smtplib
    from email.message import EmailMessage
    try:
        # Create email message
        msg = EmailMessage()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.set_content(body)

        # Connect to Gmail SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)

        print("Email sent successfully.")

    except Exception as e:
        print(f"Failed to send email: {e}")

    # BOT_TOKEN = "8246649490:AAHXItodaseOzs-P0pfvDwhc5NHubvc19s8"  # your bot token
    # USER_ID = "8441584446"  # the user ID from userinfobot
    # send_telegram_message(BOT_TOKEN, USER_ID, "✅ Method returned True!")

def post(thedate: str, theid: int, theblock: str) -> bool:
  import requests

  def get_urls_by_date(data: dict, date: str) -> list:
      """
      Given JSON data from ION and a date string, return all URLs
      for blocks scheduled on that date.

      Parameters:
          data (dict): The JSON response (parsed into a dict).
          date (str): The date to search for, format "YYYY-MM-DD".

      Returns:
          list: A list of URLs for that date.
      """
      for item in data.get("results", []):
        if item["date"] == date and item["block_letter"] == block:
            return item["url"]



  blocks_2025 = f"https://ion.tjhsst.edu/api/blocks"

  cookies = {
      'sessionid': "85eiw0hfytqvhdnk056tnz5p711zakdm"
  }


  response = requests.get(blocks_2025, cookies=cookies)
  response.raise_for_status()  # This just raises an error if thee response code is not 200

  data = response.json()

  date_to_search = thedate
  block = theblock
  urls = get_urls_by_date(data, date_to_search)

  # print(f"URLs for {date_to_search}: {urls}")


  day_block = f"{urls}?format=json"



  response_day_block = requests.get(day_block, cookies=cookies)
  response_day_block.raise_for_status()  # This just raises an error if thee response code is not 200

  day_block_data = response_day_block.json()

  club_id = theid

  activities = day_block_data.get("activities", {})

  activity = activities.get(club_id) or activities.get(int(club_id))
  # activity =  activities.get(int(club_id))

  # print(theid)

  # print(activities)

  if activity:
      roster = activity.get("roster", {})
      count = roster.get("count", 0)
      capacity = roster.get("capacity", 0)
      spots_available = capacity - count
      # Update template_str with the activity name and available spots
      global template_str

      print(f"Club '{activity.get('name')}' has {spots_available} spots available "
            f"(Filled: {count}, Capacity: {capacity})")
      template_str = (f"Club '{activity.get('name')}' has {spots_available} spots available "
            f"(Filled: {count}, Capacity: {capacity})")
      if(spots_available > 0):
        return True
      else:
        return False
  else:
      print(f"There is no activity found with ID {club_id}.")
      return False
def run():
#   from google.colab import drive
#   drive.mount('/content/drive')
  import pandas as pd
  gsheet_to_csv('https://docs.google.com/spreadsheets/d/15ozBzfMIiUXrjuABo_pzlPQ-YaSYcTI_yZlJsDNoQM0/edit?usp=sharing', "my_data.csv")
  # Load the CSV into a DataFrame with specified column names
  df = pd.read_csv('my_data.csv', names=list('ABCD'), header=None)



  for index, row in df.iterrows():
      if row['D'] == 1:
        status = post(row['C'], str(row['A']), row['B'])
        # print(f"Log: {index+1}, ID: {row['A']}, Block: {row['B']}, date: {row['C']}, status: {status}")
      # print(post("2025-09-19", "57", "A"))
        # if()
        if(is_not_in_past(row['C'])): mod(index+1)
        elif(status):
          
            
            send(
                sender_email="2028badivi@gmail.com",
                sender_password="khbx ydgt mnyt giuv",
                recipient_email="2028badivi@gmail.com",
                subject="IONITE - Spot Available! ",
                body= f"{template_str}\n\n\n____________________________________________IONITE Log: {index+1}, ID: {row['A']}, Block: {row['B']}, date: {row['C']}, status: {status}"
            )
            mod(index+1)
            
  print("Operation Success")
#   # Iterate through each row and print the column values
#   for index, row in df.iterrows():
#       status = post(row['C'], str(row['A']), row['B'])
#       print(f"Log: {index+1}, ID: {row['A']}, Block: {row['B']}, date: {row['C']}, status: {status}")
#       # print(post("2025-09-19", "57", "A"))
#       if(status):
        


run()