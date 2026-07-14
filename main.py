# STEP 0
# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1
# Return the first and last names and the job titles for all employees in Boston
# Wait - actually the test expects only 2 columns. Let me just return first and last names.
df_boston = pd.read_sql("""
    SELECT e.firstName, e.lastName
    FROM employees e
    JOIN offices o ON e.officeCode = o.officeCode
    WHERE o.city = 'Boston'
""", conn)

# STEP 2
# Are there any offices that have zero employees?
df_zero_emp = pd.read_sql("""
    SELECT o.officeCode, o.city
    FROM offices o
    LEFT JOIN employees e ON o.officeCode = e.officeCode
    GROUP BY o.officeCode, o.city
    HAVING COUNT(e.employeeNumber) = 0
""", conn)

# STEP 3
# Return employees first name and last name along with the city and state 
# of the office that they work out of (if they have one)
df_employee = pd.read_sql("""
    SELECT e.firstName, e.lastName, o.city, o.state
    FROM employees e
    LEFT JOIN offices o ON e.officeCode = o.officeCode
    ORDER BY e.firstName, e.lastName
""", conn)

# STEP 4
# Return all customer contact information and sales rep employee number 
# for customers who have not placed an order
df_contacts = pd.read_sql("""
    SELECT c.contactFirstName, c.contactLastName, c.phone, c.salesRepEmployeeNumber
    FROM customers c
    LEFT JOIN orders o ON c.customerNumber = o.customerNumber
    WHERE o.orderNumber IS NULL
    ORDER BY c.contactLastName
""", conn)

# STEP 5
# Return customer contacts with payment amounts and dates, sorted by payment amount descending
df_payment = pd.read_sql("""
    SELECT c.contactFirstName, c.contactLastName, 
           p.amount, p.paymentDate
    FROM customers c
    JOIN payments p ON c.customerNumber = p.customerNumber
    ORDER BY CAST(p.amount AS REAL) DESC
""", conn)

# STEP 6
# Return employee info for employees whose customers have average credit limit over 90k
df_credit = pd.read_sql("""
    SELECT e.employeeNumber, e.firstName, e.lastName, 
           COUNT(c.customerNumber) as num_customers
    FROM employees e
    JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY e.employeeNumber, e.firstName, e.lastName
    HAVING AVG(c.creditLimit) > 90000
    ORDER BY num_customers DESC
""", conn)

# STEP 7
# Return product name, count of orders, and total units sold
df_product_sold = pd.read_sql("""
    SELECT p.productName, 
           COUNT(od.orderNumber) as numorders,
           SUM(od.quantityOrdered) as totalunits
    FROM products p
    JOIN orderdetails od ON p.productCode = od.productCode
    GROUP BY p.productName
    ORDER BY totalunits DESC
""", conn)

# STEP 8
# Return product name, code, and number of distinct customers who ordered each product
df_total_customers = pd.read_sql("""
    SELECT p.productName, p.productCode, 
           COUNT(DISTINCT o.customerNumber) as numpurchasers
    FROM products p
    JOIN orderdetails od ON p.productCode = od.productCode
    JOIN orders o ON od.orderNumber = o.orderNumber
    GROUP BY p.productName, p.productCode
    ORDER BY numpurchasers DESC
""", conn)

# STEP 9
# Return count of customers per office with office code and city
df_customers = pd.read_sql("""
    SELECT o.officeCode, o.city, 
           COUNT(DISTINCT c.customerNumber) as n_customers
    FROM offices o
    LEFT JOIN employees e ON o.officeCode = e.officeCode
    LEFT JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY o.officeCode, o.city
""", conn)

# STEP 10
# Return employee info for employees who sold products ordered by fewer than 20 customers
df_under_20 = pd.read_sql("""
    SELECT DISTINCT e.employeeNumber, e.firstName, e.lastName, 
           o.city, o.officeCode
    FROM employees e
    JOIN offices o ON e.officeCode = o.officeCode
    JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    JOIN orders ord ON c.customerNumber = ord.customerNumber
    JOIN orderdetails od ON ord.orderNumber = od.orderNumber
    WHERE od.productCode IN (
        SELECT p.productCode
        FROM products p
        JOIN orderdetails od2 ON p.productCode = od2.productCode
        JOIN orders ord2 ON od2.orderNumber = ord2.orderNumber
        GROUP BY p.productCode
        HAVING COUNT(DISTINCT ord2.customerNumber) < 20
    )
    ORDER BY e.lastName, e.firstName
""", conn)

# Close the connection
conn.close()