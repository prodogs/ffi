from sched import scheduler
import psycopg2
import winsound
import schedule
import time

def beep():
    frequency = 2500  # Set Frequency To 2500 Hertz
    duration = 1000  # Set Duration To 1000 ms == 1 second
    winsound.Beep(frequency, duration)


def query():
    print("Running Query")
    try:
        connection = psycopg2.connect(
            user="dcmaInstantAuditServiceAdmin",
            password="ZugyS1SRe!J5RDPj",
            host="ta-workplace-dcma-instant-audit-service-tst.cluster-cgimdk8ltynu.us-east-1.rds.amazonaws.com",
            port="5432",
            database="dcma_instant_audit_service"
        )

        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        print(connection.get_dsn_parameters(), "\n")

        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")

        table_name = 'ra_retirement.api_audit'  # replace with your table name

        query = "SELECT * from ra_retirement.api_audit where query_string like '%aws%' and creation_ts > (now() - interval '5 minutes');"

        cursor.execute(query)
        schema = cursor.fetchall()

        if (len(schema) > 1):
            beep()

        print(f"Schema of {table_name}:")
        for column in schema:
            print(f" ID = {column[0]}, \n Request ID = {column[1]},\n Request Type = {column[2]}, \n Key = {column[3]},\n account_no = {column[4]},\nquery_string =  {column[5]},\nrequest_payload =  {column[6]},\n  response_payload = {column[7]}, \n response_status={column[8]},\n response_status_message {column[9]}, \n source={column[10]}, \n creation_ts = {column[11]}, \n modified_ts = {column[12]}\n")


    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

schedule.every(1).minutes.do(query)



while True:
    schedule.run_pending()
    time.sleep(1)

    
def callRest():
        import requests

        # Define the API endpoint
        url = "http://example.com/api_endpoint"  # replace with your API endpoint

        # Define the headers for the API request
        headers = {
            "Content-Type": "application/json",
            # Add any other headers required by the API
        }

        # Define the data to be sent to the API
        data = {
            # Add the data required by the API
        }

        # Send a POST request to the API
        response = requests.post(url, headers=headers, json=data)

        # Print the response from the API
        print(response.json())