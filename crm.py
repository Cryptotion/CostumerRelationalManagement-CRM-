from tkinter import *
from PIL import ImageTk, Image
import mysql.connector
import csv       

root = Tk()
root.title('CRM - Krishna')
root.geometry("400x600")

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "12345",
    database = "codemy",
)

# print(mydb)

# create a _Cursor and initialize it 
my_cursor = mydb.cursor()

#  Create database
# my_cursor.execute("CREATE DATABASE codemy")

#  Test to see if database was created
# my_cursor.execute("SHOW DATABASES")
# for db in my_cursor:
#     print(db)

# Drop table
# my_cursor.execute("DROP TABLE customers")

# Create a table
my_cursor.execute("CREATE TABLE IF NOT EXISTS customers (first_name VARCHAR(255), \
    last_name VARCHAR(255), \
    zipcode int(10), \
    price_paid DECIMAL(10,2), \
    user_id INT AUTO_INCREMENT PRIMARY KEY)")

# Alter Table
'''
my_cursor.execute("ALTER TABLE customers ADD (\
    email VARCHAR(255),\
    address_1 VARCHAR(255),\
    address_2 VARCHAR(255),\
    city VARCHAR(50),\
    state VARCHAR(50),\
    country VARCHAR(255),\
    phone VARCHAR(255),\
    payment_method VARCHAR(50),\
    discount_code VARCHAR(255))")

'''
#  Show table
# my_cursor.execute("SELECT * FROM customers")
# print(my_cursor.description)

# for thing in my_cursor.description:
#     print(thing)

# Clear Text Fields
def clear_fields():
    first_name_box.delete(0, END)
    last_name_box.delete(0, END)
    address1_box.delete(0, END)
    address2_box.delete(0, END)
    city_box.delete(0, END)
    state_box.delete(0, END)
    zipcode_box.delete(0, END)
    country_box.delete(0, END)
    phone_box.delete(0, END)
    email_box.delete(0, END)
    payment_method_box.delete(0, END)
    discount_code_box.delete(0, END)
    price_paid_box.delete(0, END)


#  Submit Customer To Database
def add_customer():
    sql_command = "INSERT INTO customers (first_name, last_name, zipcode, price_paid, email, address_1, address_2, city, state, country, phone, payment_method, discount_code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (first_name_box.get(), last_name_box.get(), zipcode_box.get(), price_paid_box.get(), email_box.get(), address1_box.get(), address2_box.get(), city_box.get(), state_box.get(), country_box.get(), phone_box.get(), payment_method_box.get(), discount_code_box.get())
    my_cursor.execute(sql_command, values)

    # Commit the changes to the database
    mydb.commit()
    # Clear the fields
    clear_fields()

# Write To CSV Excel Function
def write_to_csv(result):
    with open('customers.csv', 'a', newline='') as f:
        w = csv.writer(f, dialect='excel')
        for record in result:
            w.writerow(record)

# Search Customers
def search_customers():
    search_customers = Tk()
    search_customers.title("Search Customers")
    search_customers.geometry("800x600")
    def search_now():
        searched = search_box.get()
        sql = "SELECT * FROM customers WHERE last_name = %s"
        name = (searched, )
        result = my_cursor.execute(sql, name)
        result = my_cursor.fetchall()

        if not result:
            result = "Record Not Found..."
        
        searched_label = Label(search_customers, text=result)
        searched_label.grid(row=2, column=0, padx=10, columnspan=2)


    # Entry box to search for customer
    search_box = Entry(search_customers)
    search_box.grid(row=0, column=1, padx=10, pady=10)
    # Entry box label search for customer
    search_box_label = Label(search_customers, text="Search Customer By Last Name: ")
    search_box_label.grid(row=0, column=0, padx=10, pady=10)
    # Entry box search Button for customer
    search_button = Button(search_customers, text="Search Customers", command=search_now)
    search_button.grid(row=1, column=0, padx=10)

#  List Customers
def list_customers():
    list_customers_query = Tk()
    list_customers_query.title("List All Customers")
    list_customers_query.geometry("800x600")
    # Query The Database
    my_cursor.execute("SELECT * FROM customers")
    result = my_cursor.fetchall()
    for index, x in enumerate(result):
        num=0
        for y in x:
            lookup_label = Label(list_customers_query, text=y)
            lookup_label.grid(row=index , column=num)
            num +=1
    csv_button = Button(list_customers_query, text="Save to Excel", command=lambda: write_to_csv(result))
    csv_button.grid(row=index+1, column=0)




# Create a Label
title_label = Label(root, text="Codemy Customer Database", font=("Helvetica", 16))
title_label.grid(row=0, column=0, columnspan=2, pady="10")

# Create Main Form To Enter Customer Data
first_name_label = Label(root, text="First Name").grid(row=1, column=0, sticky=W, padx=10)
last_name_label = Label(root, text="Last Name").grid(row=2, column=0, sticky=W, padx=10)
address1_label = Label(root, text="Address 1").grid(row=3, column=0, sticky=W, padx=10)
address2_label = Label(root, text="Address 2").grid(row=4, column=0, sticky=W, padx=10)
city_label = Label(root, text="City").grid(row=5, column=0, sticky=W, padx=10)
state_label = Label(root, text="State").grid(row=6, column=0, sticky=W, padx=10)
zipcode_label = Label(root, text="Zipcode").grid(row=7, column=0, sticky=W, padx=10)
country_label = Label(root, text="Country").grid(row=8, column=0, sticky=W, padx=10)
phone_label = Label(root, text="Phone Number").grid(row=9, column=0, sticky=W, padx=10)
email_label = Label(root, text="Email Addresh").grid(row=10, column=0, sticky=W, padx=10)
payment_method_label = Label(root, text="Payment Method").grid(row=11, column=0, sticky=W, padx=10)
discount_code_label = Label(root, text="Discount Code").grid(row=12, column=0, sticky=W, padx=10)
price_paid_label = Label(root, text="Price Paid").grid(row=13, column=0, sticky=W, padx=10)

# Create Entry Boxes
first_name_box = Entry(root)
first_name_box.grid(row=1, column=1)

last_name_box = Entry(root)
last_name_box.grid(row=2, column=1, pady=5)

address1_box = Entry(root)
address1_box.grid(row=3, column=1, pady=5)

address2_box = Entry(root)
address2_box.grid(row=4, column=1, pady=5)

city_box = Entry(root)
city_box.grid(row=5, column=1, pady=5)

state_box = Entry(root)
state_box.grid(row=6, column=1, pady=5)

zipcode_box = Entry(root)
zipcode_box.grid(row=7, column=1, pady=5)

country_box = Entry(root)
country_box.grid(row=8, column=1, pady=5)

phone_box = Entry(root)
phone_box.grid(row=9, column=1, pady=5)

email_box = Entry(root)
email_box.grid(row=10, column=1, pady=5)

payment_method_box = Entry(root)
payment_method_box.grid(row=11, column=1, pady=5)

discount_code_box = Entry(root)
discount_code_box.grid(row=12, column=1, pady=5)

price_paid_box = Entry(root)
price_paid_box.grid(row=13, column=1, pady=5)

# Creat_Buttons
add_customer_button = Button(root, text="Add Customer To Database", command=add_customer)
add_customer_button.grid(row=14, column=0, padx=10, pady=10)
clear_field_button = Button(root, text="Clear Fields", command=clear_fields)
clear_field_button.grid(row=14, column=1)
#  List Customers button
list_customers_button = Button(root, text="List Customer", command=list_customers)
list_customers_button.grid(row=15, column=0, sticky=W, padx=10)

#  Search Customers
search_customers_button = Button(root, text="Search Customers", command=search_customers)
search_customers_button.grid(row=15, column=1, sticky=W, padx=10)


root.mainloop()