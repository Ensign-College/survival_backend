import psycopg2

connection =""


try:
    connection = psycopg2.connect(
        host="your_host",
        port="your_port",
        database="your_database_name",
        user="your_username",
        password="your_password"
    )
    # Use the connection object for database operations
    # ...
except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL:", error)
finally:
    # Close the connection
    if connection:
        connection.close()
