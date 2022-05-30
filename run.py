"""
Installing libraries: pip3 install gspread google-auth
Imports entire gspread library
Imports the credentials class not the entire module
"""
import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

#Every google account has an IAM (Identity Access Management)
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
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 6 numbers separated
    by commas. The loop will repeatedly request data, until it is valid.
    """
    try:
        #List comprehension
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(f"We expected to receive 6 data values, you inputted {len(values)}")
    #'as' keyword assigns assigns the ValueError to e (shorthand error)
    except ValueError as e:
        print(f"Invalid data {e}, please try again.\n")
        return False

    return True




def update_worksheet(data, worksheet):
    """
    Refactored function that can update both the sales and surplus worksheets.
    Receives a list of integers to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    """
    print(f"Updating {worksheet} worksheet... :D\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated succesfully!\n")



def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.
    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out
    - .get_all_values is a method from the gspread library
    - Using slicing [-1] method to slice the final item of the list.
    - Return it to the stock variable
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]
    
    #zip() method allows to lists to become a zip object
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    print(surplus_data)

    return surplus_data

def get_last_5_entries_data():
    """
    Collects columns of data from sales worksheet, collecting
    the last 5 entries for each sandwich and returns the data
    as a list of lists.
    """
    sales = SHEET.worksheet("sales")
    #col.values provided by gspread to request 3rd column
    column = sales.col_values(3)
    print(column)

def main():
    """
    Main function to run all program functions
    """
    data = get_sales_data()
    print(data)
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")

#Function calls must be below where a function is defined
print("Welcome to Love SandWiches Data Automation :)")
main()

get_last_5_entries_data()



"""
def update_sales_worksheet(data):

    Update sales worksheet, add new row with the list data provided

    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully.\n")


def calculate_surplus_data(sales_row):
    
    Compare sales with stock and calculate the surplus for each item type.
    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    print(stock_row)
"""