"""
Installing libraries: pip3 install gspread google-auth
Imports entire gspread library
Imports the credentials class not the entire module
"""
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# Every google account has an IAM (Identity Access Management)
CREDS = Credentials.from_service_account_file('credidentials.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

"""
Checking our API works
Calling sales worksheet from our google spread sheet
Data variable to print sales data to the terminal using: python3 run.py
"""
sales = SHEET.worksheet('sales')
sheet_data = sales.get_all_values()
print(sheet_data)

def get_sales_data():
    """
    Get sales figures input from user
    User request loop
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, seperated by commas, CSV format.")
        print("Example: 10,20,30,40,50,60.\n")

        data_string = input("Enter your data here: ")

        #Converting string by split() method returns the broken up values as list
        sales_data = data_string.split(",")
        validate_data(sales_data)

        #Validate_data(sales_data) is condition to break while loop
        if validate_data(sales_data):
            print("Yay! The data is correct! <3")
            break

    return sales_data


def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(f"We expected to receive 6 data values, you inputted {len(values)}")
    #as keyword assigns assigns the ValueError to e (shorthand error)
    except ValueError as e:
        print(f"Invalid data {e}, please try again.\n")
        return False 

    return True

data = get_sales_data()


