# STEP 1A
# Import SQL Library and Pandas
import sqlite3
import pandas as pd

# STEP 1B
# Connect to the database
conn = sqlite3.connect('data.sqlite')


# STEP 2
# Replace None with your code
df_first_five = pd.read_sql("""SELECT employeeNumber, lastName FROM employees""", conn)

# STEP 3
# Replace None with your code
df_five_reverse = pd.read_sql("""SELECT lastName, employeeNumber FROM employees""", conn)

# STEP 4
# Replace None with your code
df_alias = pd.read_sql("""SELECT lastName, employeeNumber AS ID FROM employees""", conn)

# STEP 5
# Replace None with your code
df_executive = pd.read_sql("""SELECT *, CASE WHEN jobTitle = "President" OR jobTitle = "VP Sales" OR jobTitle = "VP Marketing" THEN "Executive" ELSE "Not Executive" END AS role FROM employees""", conn)

# STEP 6
# Replace None with your code
df_name_length = pd.read_sql("""SELECT LENGTH(lastName) AS name_length FROM employees""", conn)

# STEP 7
# Replace None with your code
df_short_title = pd.read_sql("""SELECT SUBSTR(jobTitle, 1, 2) AS short_title FROM employees""", conn)

# STEP 8
# Replace None with your code
sum_total_price = pd.read_sql("""SELECT SUM(ROUND(priceEach * quantityOrdered)) AS total_price FROM orderDetails""", conn).iloc[:, 0]

# STEP 9
# Replace None with your code
df_day_month_year = pd.read_sql("""SELECT orderDate, STRFTIME('%d', orderDate) AS day, STRFTIME('%m', orderDate) AS month, STRFTIME('%Y', orderDate) AS year FROM orders""", conn)

conn.close()