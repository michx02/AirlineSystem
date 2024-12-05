
#Author: Michael Mvano
#Website


import pymysql
from hashlib import md5
from datetime import *

import matplotlib.pyplot as plt
import io
import base64
from flask import Flask, render_template, request, session, flash, redirect, url_for
from datetime import datetime, timedelta


app = Flask(__name__)

app.secret_key = 'my_secret_key'
# app.config['SECRET_KEY'] = 'my_secret_key'

# Establish connection to MySQL database
db = pymysql.connect(host="localhost", 
                   port = 3306,
                   user="root", 
                   password="", 
                   database="airsystem", 
                   charset="utf8mb4", 
                   cursorclass=pymysql.cursors.DictCursor
)

# cursor = db.cursor()
# @app.before_first_request
# def init_db():
#     db.ping(reconnect=True)



@app.route('/search_flights', methods=['GET'])
def search_flights():
    source = request.args.get('source')
    destination = request.args.get('destination')
    departure_date = request.args.get('departure_date')
    return_date = request.args.get('return_date')

    print(f"Searching flights from {source} to {destination}, departure: {departure_date}, return: {return_date}")

    try:
        cursor = db.cursor()

        # Base query to include airport names
        query = """
        SELECT f.airline_name, f.flight_number, f.depart_date, f.depart_time, f.arrival_date, f.arrival_time, 
               f.base_price, f.flight_status, 
               da.airport_name AS depart_airport_name, aa.airport_name AS arrival_airport_name
        FROM flight f
        JOIN airport da ON f.depart_airport_code = da.airport_code
        JOIN airport aa ON f.arrival_airport_code = aa.airport_code
        WHERE f.depart_date = %s 
          AND da.airport_name = %s
          AND aa.airport_name = %s
        """
        query_params = [departure_date, source, destination]

        # Include return date if provided
        if return_date:
            query += """
            UNION
            SELECT f.airline_name, f.flight_number, f.depart_date, f.depart_time, f.arrival_date, f.arrival_time, 
                   f.base_price, f.flight_status, 
                   da.airport_name AS depart_airport_name, aa.airport_name AS arrival_airport_name
            FROM flight f
            JOIN airport da ON f.depart_airport_code = da.airport_code
            JOIN airport aa ON f.arrival_airport_code = aa.airport_code
            WHERE f.depart_date = %s 
              AND da.airport_name = %s
              AND aa.airport_name = %s
            """
            query_params.extend([return_date, destination, source])

        cursor.execute(query, query_params)
        flights = cursor.fetchall()
        print(f"Found flights: {flights}")

        return render_template('view_future_flights.html', flights=flights)

    except Exception as e:
        print(f"Error searching flights: {e}")
        flash("An error occurred while searching for flights.")
        return redirect(url_for('index_page'))


@app.route('/check_flight_status', methods=['GET', 'POST'])
def check_flight_status():
    if request.method == 'POST':
        airline_name = request.form.get('airline_name')
        flight_number = request.form.get('flight_number')
        flight_date = request.form.get('flight_date')

        print(f"Checking status for {airline_name}, Flight: {flight_number}, Date: {flight_date}")

        try:
            cursor = db.cursor()

            # Query to fetch flight status using airline name, flight number, and flight date
            query = """
            SELECT airline_name, flight_number, depart_date, arrival_date, flight_status
            FROM flight 
            WHERE airline_name = %s AND flight_number = %s AND (depart_date = %s OR arrival_date = %s)
            """
            cursor.execute(query, (airline_name, flight_number, flight_date, flight_date))
            flight_status = cursor.fetchone()

            return render_template('view_flight_status.html', flight_status=flight_status)

        except Exception as e:
            print(f"Error fetching flight status: {e}")  # Debugging
            flash("An error occurred while checking the flight status.")
            return redirect(url_for('index_page'))
    return redirect(url_for('index_page'))




def authenticate_customer(email_address_in, password_in):
    cursor = db.cursor()
    query = "SELECT * FROM customer WHERE email_address = %s"
    try:
        cursor.execute(query, (email_address_in,))
        output = cursor.fetchone()
        cursor.close()

        print(f"Query result: {output}")  # Debugging

        if not output:
            flash("Email not found.")
            print("Email not found in database.")  # Debugging
            return False

        stored_password = output.get("customer_password")
        print(f"Stored password: {stored_password} | Entered password hash: {password_in}")  # Debugging

        if stored_password == password_in:
            print("Password match.")  # Debugging
            return True
        else:
            flash("Incorrect password.")
            print("Password mismatch.")  # Debugging
            return False
    except Exception as e:
        print(f"Error in authentication: {e}")  # Debugging
        flash("An error occurred during login.")
        return False




def authenticate_airline_staff(username_in, password_in):
    cursor = db.cursor()
    query = "SELECT * FROM airline_staff WHERE username = %s"

    try:
        print(f"Authenticating username: {username_in}")
        print(f"Password hash to match: {password_in}")

        cursor.execute(query, (username_in,))
        output = cursor.fetchone()
        print(f"Query result: {output}")
        cursor.close()

        if not output:
            print("Username not found.")
            flash("Incorrect Username or Password")
            return False

        stored_password = output.get("user_password")
        print(f"Stored password hash: {stored_password}")

        if stored_password == password_in[:20]:
            print("Password match.")
            return True
        else:
            print("Incorrect password.")
            flash("Incorrect Username or Password")
            return False
    except Exception as e:
        print(f"Error in authentication: {e}")
        flash("An error occurred during login.")
        return False




# function to check whether the airline staff already exists in the databse, used when registering
def airline_staff_exists(username_in):
    cursor = db.cursor()
    query = "SELECT * FROM Airline_Staff WHERE username = %s"
    
    try:
        cursor.execute(query, username_in)
        output = cursor.fetchall() # this query should only be returning one row becuase usernames are unique
        if output[0]["username"] == username_in: # if the retrieved output matches the username passed in 
            return True # return true becuase the username exists
        return False # if the usernames do not match, aka if it returns an empty set, the username doesn't exist
    
    except Exception:
        return False # erorr occured, couldn't check staff exists


# function to check whether the customer already exists in the databse, used when registering
def customer_exists(email_addess):
    cursor = db.cursor()
    query = "SELECT * FROM customer WHERE email_address = %s"
    
    try:
        cursor.execute(query, (email_addess,)) # ust be email_address, because you have to pass in a tuple, not a single variable
        output = cursor.fetchall() # this query should only be returning one row becuase email_address are unique
        if output[0]["email_address"] == email_addess: # if the retrieved output matches the username passed in 
            return True # return true becuase the username exists
        return False # if the usernames do not match, aka if it returns an empty set, the username doesn't exist
    
    except Exception:
        return False# erorr occured, couldn't check customer exists

@app.route('/')
def index_page():
    # fetch()
    return render_template('index.html')

@app.route("/customer_login_page", methods=["GET", "POST"])
def customer_login_page():
    if request.method == "POST":
        email_address = request.form.get("email_address")
        password = md5(request.form.get("password").encode()).hexdigest()

        print(f"Attempting login for: {email_address} | Hashed password: {password}")  # Debugging

        if authenticate_customer(email_address, password):
            session["email_address"] = email_address
            print(f"Login successful! Session set for {email_address}")  # Debugging
            return redirect(url_for("customer"))
        else:
            print("Login failed. Incorrect credentials.")  # Debugging
            flash("Login failed. Check your credentials.")

    return render_template("customer_login_page.html")






@app.route('/customer_dashboard', methods=['GET'])
def customer():
    try:
        # Check if the user is logged in
        if "email_address" not in session:
            flash("Please log in to access the dashboard.", "error")
            return redirect(url_for('customer_login_page'))

        email_address = session["email_address"]
        print(f"Customer Dashboard for: {email_address}")  # Debugging

        cursor = db.cursor()

        # Fetch customer details
        cursor.execute("""
            SELECT first_name, last_name, email_address
            FROM customer
            WHERE email_address = %s
        """, (email_address,))
        customer_data = cursor.fetchone()

        if not customer_data:
            flash("Customer not found. Please log in again.", "error")
            return redirect(url_for('customer_login_page'))

        print(f"Customer data: {customer_data}")  # Debugging

        # Fetch all flights purchased by the customer
        cursor.execute("""
            SELECT 
                flight.airline_name, flight.flight_number, flight.depart_date, flight.depart_time, 
                flight.arrival_date, flight.arrival_time, flight.depart_airport_code, 
                flight.arrival_airport_code, ticket.calculated_price
            FROM 
                purchase
            JOIN 
                ticket ON purchase.ticket_id = ticket.ticket_id
            JOIN 
                flight ON ticket.airline_name = flight.airline_name 
                AND ticket.flight_number = flight.flight_number 
                AND ticket.depart_date = flight.depart_date
            WHERE 
                purchase.email_address = %s
        """, (email_address,))
        purchased_flights = cursor.fetchall()

        print(f"Purchased flights: {purchased_flights}")  # Debugging

        return render_template(
            'customer_dashboard.html',
            customer=customer_data,
            future_flights=purchased_flights
        )

    except Exception as e:
        print(f"Error in customer dashboard: {e}")  # Debugging
        flash("An error occurred while loading the dashboard. Please try again.", "error")
        return redirect(url_for('customer_login_page'))





@app.route('/spending_range', methods=['GET'])
def spending_range():
    # try:
        email_address = session['email_address']
        cursor = db.cursor()
        
        # fetch user data:
        query = "SELECT * FROM customer where customer.email_address = %s"
        cursor.execute(query, email_address)
        user_data = cursor.fetchall() # extracts user data
        
        query = """
        SELECT sum(ticket.calculated_price) 
        FROM customer, purchase, ticket 
        WHERE customer.email_address = %s and customer.email_address = purchase.email_address and purchase.ticket_id = ticket.ticket_id 
        and purchase.purchase_date >= YEAR(DATE_SUB(CURDATE(), INTERVAL 1 YEAR))
        """
        # DATE_SUB(CURRENT_DATE(), INTERVAL 1 YEAR)
        cursor.execute(query, email_address)
        user_spending = cursor.fetchall()[0]['sum(ticket.calculated_price)']
        
        # fetch spending within a range
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        query = """
        SELECT sum(ticket.calculated_price)
        FROM customer, purchase, ticket 
        WHERE customer.email_address = %s and customer.email_address = purchase.email_address and purchase.ticket_id = ticket.ticket_id 
        and purchase.purchase_date >= %s and purchase.purchase_date <= %s
        """
        cursor.execute(query, (email_address, start_date, end_date))
        range_spending = cursor.fetchall()[0]['sum(ticket.calculated_price)']
  
        query = """
        SELECT ticket.ticket_id, ticket.airline_name, ticket.flight_number, ticket.depart_date, ticket.depart_time 
        FROM purchase, ticket 
        WHERE purchase.email_address = %s and purchase.ticket_id = ticket.ticket_id;
        """
        cursor.execute(query, email_address)
        future_flights = cursor.fetchall()
        cursor.close()
        
        return render_template('customer_dashboard.html', customer = user_data[0], start_date=start_date, end_date=end_date, spending_past_year = user_spending, range_spending = range_spending, future_flights=future_flights)
    
    # except Exception as e:
    #     # Handle exceptions
    #     return "Error: Unable to fetch spending data within the specified range"
    
    
    
@app.route('/purchase_ticket', methods=["POST"])
def pay_for_ticket():
    if request.method == "POST":
        try:
            # Check if the user is logged in
            email_address = session.get('email_address')
            if not email_address:
                flash("You need to log in to purchase a ticket.", "error")
                return redirect(url_for('customer_login_page'))

            print(f"User logged in with email: {email_address}")  # Debugging

            # Collect form data
            form_data = {
                "first_name": request.form.get('first_name'),
                "last_name": request.form.get('last_name'),
                "date_of_birth": request.form.get('date_of_birth'),
                "airline_name": request.form.get('airline_name'),
                "flight_number": request.form.get('flight_number'),
                "depart_date": request.form.get('depart_date'),
                "depart_time": request.form.get('depart_time'),
                "card_type": request.form.get('card_type'),
                "card_number": md5(request.form.get('card_number').encode()).hexdigest(),
                "name_on_card": request.form.get('name_on_card'),
                "exp_date": request.form.get('expiration_date')  # Corrected field name
            }

            print(f"Form data collected: {form_data}")  # Debugging

            # Verify flight existence
            if not check_if_flight_exists(
                form_data["airline_name"],
                form_data["flight_number"],
                form_data["depart_date"],
                form_data["depart_time"]
            ):
                flash("The flight does not exist. Please check your input.", "error")
                print("Flight does not exist.")  # Debugging
                return redirect(url_for('customer'))

            cursor = db.cursor()

            # Retrieve flight base price
            cursor.execute("""
                SELECT base_price 
                FROM flight 
                WHERE airline_name = %s AND flight_number = %s AND depart_date = %s AND depart_time = %s
            """, (form_data["airline_name"], form_data["flight_number"], form_data["depart_date"], form_data["depart_time"]))
            price_data = cursor.fetchone()

            if not price_data:
                flash("Error fetching flight price.", "error")
                print("Flight price not found.")  # Debugging
                return redirect(url_for('customer'))

            base_price = price_data['base_price']
            print(f"Base price fetched: {base_price}")  # Debugging

            # Retrieve airplane details
            cursor.execute("""
                SELECT flight.airplane_id_number, airplane.seats AS total_seats
                FROM flight 
                JOIN airplane ON flight.airplane_id_number = airplane.airplane_id_number
                WHERE flight.airline_name = %s AND flight.flight_number = %s AND flight.depart_date = %s AND flight.depart_time = %s
            """, (form_data["airline_name"], form_data["flight_number"], form_data["depart_date"], form_data["depart_time"]))
            airplane_data = cursor.fetchone()

            if not airplane_data:
                flash("No airplane associated with this flight.", "error")
                print("No airplane found for the given flight details.")  # Debugging
                return redirect(url_for('customer'))

            airplane_id = airplane_data['airplane_id_number']
            total_seats = airplane_data['total_seats']
            print(f"Airplane ID: {airplane_id}, Total Seats: {total_seats}")  # Debugging

            # Check number of booked seats
            cursor.execute("""
                SELECT COUNT(ticket_id) AS booked_seats
                FROM ticket
                WHERE airline_name = %s AND flight_number = %s AND depart_date = %s AND depart_time = %s
            """, (form_data["airline_name"], form_data["flight_number"], form_data["depart_date"], form_data["depart_time"]))
            seat_data = cursor.fetchone()

            booked_seats = seat_data.get('booked_seats', 0)
            print(f"Booked seats: {booked_seats}")  # Debugging

            # Check seat availability and adjust price
            calculated_price = base_price
            if booked_seats >= total_seats:
                flash("The flight is fully booked.", "error")
                print("Flight is fully booked.")  # Debugging
                return redirect(url_for('customer'))
            elif (booked_seats / total_seats) >= 0.8:
                calculated_price *= 1.25  # Increase price by 25%

            print(f"Calculated price: {calculated_price}")  # Debugging

            # Generate ticket ID
            cursor.execute("SELECT COUNT(ticket_id) AS total_tickets FROM ticket")
            ticket_count_data = cursor.fetchone()
            ticket_id = (ticket_count_data['total_tickets'] or 0) + 1
            print(f"Generated ticket ID: {ticket_id}")  # Debugging

            # Insert ticket and purchase information
            cursor.execute("""
                INSERT INTO ticket (ticket_id, airline_name, flight_number, depart_date, depart_time, calculated_price, first_name, last_name, date_of_birth)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (ticket_id, form_data["airline_name"], form_data["flight_number"], form_data["depart_date"], form_data["depart_time"], calculated_price, form_data["first_name"], form_data["last_name"], form_data["date_of_birth"]))

            cursor.execute("""
                INSERT INTO purchase (ticket_id, email_address, purchase_time, purchase_date, card_type, card_number, name_on_card, exp_date)
                VALUES (%s, %s, CURTIME(), CURDATE(), %s, %s, %s, %s)
            """, (ticket_id, email_address, form_data["card_type"], form_data["card_number"], form_data["name_on_card"], form_data["exp_date"]))

            # Commit transaction
            db.commit()
            flash("Ticket purchased successfully!", "success")
            print("Ticket purchase successful.")  # Debugging
            return redirect(url_for('customer'))

        except Exception as e:
            print(f"Error during ticket purchase: {e}")  # Debugging
            flash("An error occurred during ticket purchase. Please try again.", "error")
            return redirect(url_for('customer'))

    return redirect(url_for('customer'))


            
@app.route('/cancel_ticket', methods=["GET", "POST"])
def cancel_trip():
    if request.method == "POST":
        try:
            # Retrieve the ticket ID from the form
            ticket_id = request.form.get('ticket_id')

            if not ticket_id:
                flash("Ticket ID is required to cancel a trip.", "error")
                return redirect(url_for('customer'))

            cursor = db.cursor()

            # Check if the ticket exists and fetch its details
            query_check_ticket = "SELECT * FROM ticket WHERE ticket_id = %s"
            cursor.execute(query_check_ticket, ticket_id)
            ticket = cursor.fetchone()

            if not ticket:
                flash("Ticket does not exist!", "error")
                return redirect(url_for('customer'))

            # Check if the ticket's departure date is in the future
            depart_date = ticket['depart_date']
            if date.today() >= depart_date:
                flash("Cannot cancel tickets for past or current flights.", "error")
                return redirect(url_for('customer'))

            
            query_delete_ticket = "DELETE FROM ticket WHERE ticket_id = %s"
            query_delete_purchase = "DELETE FROM purchase WHERE ticket_id = %s"


            cursor.execute(query_delete_ticket, (ticket_id,))
            cursor.execute(query_delete_purchase, (ticket_id,))

            db.commit()
            cursor.close()

            flash("Ticket successfully canceled.", "success")
            return redirect(url_for('customer'))

        except Exception as e:
            print(f"Error while canceling ticket: {e}")  # Debugging
            flash("An error occurred while canceling the ticket. Please try again.", "error")
            return redirect(url_for('customer'))
    else:
        return redirect(url_for('customer'))


@app.route('/airline_staff_login_page.html', methods=['GET', 'POST'])
def airline_staff_login_page():
    if request.method == "POST":
        username = request.form['username']
        password = md5(request.form['password'].encode()).hexdigest()

        print(f"Attempting login for airline staff: {username}")  # Debugging
        print(f"Password hash: {password}")  # Debugging

        if authenticate_airline_staff(username, password):
            session["username"] = username
            print(f"Login successful! Session set for {session['username']}")  # Debugging
            return redirect(url_for('airline_staff'))
        else:
            print("Login failed. Incorrect credentials.")  # Debugging
            flash("Login failed. Check your credentials.")

    return render_template('airline_staff_login_page.html')


@app.route('/airline_staff_dashboard.html', methods=['GET', 'POST'])
def airline_staff():
    try:
        if "username" not in session:
            print("Session missing username.")  # Debugging
            raise Exception("Session error")

        username = session["username"]
        print(f"Logged in as: {username}")  # Debugging

        cursor = db.cursor()
        query = "SELECT * FROM airline_staff WHERE username = %s"
        cursor.execute(query, (username,))
        user_data = cursor.fetchone()
        print(f"User data: {user_data}")  # Debugging

        query = "SELECT * FROM employed_by WHERE username = %s"
        cursor.execute(query, (username,))
        employment_data = cursor.fetchone()
        print(f"Employment data: {employment_data}")  # Debugging

        airline_name = employment_data["airline_name"]
        print(f"Airline name: {airline_name}")  # Debugging

        return render_template(
            'airline_staff_dashboard.html',
            staff=user_data,
            airline_name=airline_name,
        )
    except Exception as e:
        print(f"Error: {e}")  # Debugging
        flash("Please login or create an account.")
        return redirect(url_for('airline_staff_login_page'))
    

@app.route('/view_flights', methods=['GET', 'POST'])
def view_flights():
    try:
        # Ensure the staff is logged in
        if "username" not in session:
            flash("Please log in to access this feature.", "error")
            return redirect(url_for('airline_staff_login_page'))

        username = session["username"]
        cursor = db.cursor()

        # Get the airline the staff works for
        cursor.execute("SELECT airline_name FROM employed_by WHERE username = %s", (username,))
        airline = cursor.fetchone()

        if not airline:
            flash("No airline associated with the staff account.", "error")
            return redirect(url_for('airline_staff'))

        airline_name = airline["airline_name"]
        print(f"Airline Staff works for: {airline_name}")  # Debugging

        # Default: Show future flights in the next 30 days
        if request.method == "GET":
            query = """
                SELECT *
                FROM flight
                WHERE airline_name = %s AND depart_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)
            """
            cursor.execute(query, (airline_name,))
            flights = cursor.fetchall()
            print(f"Default flights: {flights}")  # Debugging

        # Apply filters if provided (POST request)
        elif request.method == "POST":
            filters = []
            conditions = ["airline_name = %s"]
            filters.append(airline_name)

            # Filter by date range
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')
            if start_date and end_date:
                conditions.append("depart_date BETWEEN %s AND %s")
                filters.extend([start_date, end_date])

            # Filter by source airport/city
            source = request.form.get('source')
            if source:
                conditions.append("depart_airport_code = (SELECT airport_code FROM airport WHERE airport_name = %s OR city = %s)")
                filters.extend([source, source])

            # Filter by destination airport/city
            destination = request.form.get('destination')
            if destination:
                conditions.append("arrival_airport_code = (SELECT airport_code FROM airport WHERE airport_name = %s OR city = %s)")
                filters.extend([destination, destination])

            # Combine conditions into the SQL query
            query = f"SELECT * FROM flight WHERE {' AND '.join(conditions)}"
            print(f"Generated Query: {query}")  # Debugging
            print(f"Query Parameters: {filters}")  # Debugging

            cursor.execute(query, filters)
            flights = cursor.fetchall()

        return render_template('view_flights.html', flights=flights, airline_name=airline_name)

    except Exception as e:
        print(f"Error in view_flights: {e}")
        flash("An error occurred while fetching flights. Please try again.", "error")
        return redirect(url_for('airline_staff'))

@app.route('/view_flight_customers', methods=['GET'])
def view_flight_customers():
    try:
        flight_number = request.args.get('flight_number')
        depart_date = request.args.get('depart_date')
        depart_time = request.args.get('depart_time')

        if not flight_number or not depart_date or not depart_time:
            flash("Invalid flight details provided.", "error")
            return redirect(url_for('view_flights'))

        cursor = db.cursor()
        query = """
            SELECT customer.first_name, customer.last_name, customer.email_address
            FROM ticket
            JOIN purchase ON ticket.ticket_id = purchase.ticket_id
            JOIN customer ON purchase.email_address = customer.email_address
            WHERE ticket.flight_number = %s AND ticket.depart_date = %s AND ticket.depart_time = %s
        """
        cursor.execute(query, (flight_number, depart_date, depart_time))
        customers = cursor.fetchall()

        print(f"Customers for flight {flight_number} on {depart_date} at {depart_time}: {customers}")  # Debugging

        return render_template('view_flight_customers.html', customers=customers, flight_number=flight_number)

    except Exception as e:
        print(f"Error in view_flight_customers: {e}")
        flash("An error occurred while fetching customers. Please try again.", "error")
        return redirect(url_for('view_flights'))
    

@app.route('/view_frequent_customers', methods=['GET'])
def view_frequent_customers():
    try:
        # Get airline name for the logged-in staff
        username = session.get('username')
        cursor = db.cursor()
        query = "SELECT airline_name FROM employed_by WHERE username = %s"
        cursor.execute(query, (username,))
        airline_name = cursor.fetchone()['airline_name']

        # Fetch the most frequent customer
        query = """
        SELECT customer.email_address, customer.first_name, customer.last_name, COUNT(purchase.ticket_id) AS ticket_count
        FROM customer
        JOIN purchase ON customer.email_address = purchase.email_address
        JOIN ticket ON purchase.ticket_id = ticket.ticket_id
        WHERE ticket.airline_name = %s AND ticket.depart_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
        GROUP BY customer.email_address
        ORDER BY ticket_count DESC
        LIMIT 1
        """
        cursor.execute(query, (airline_name,))
        frequent_customer = cursor.fetchone()

        return render_template('view_frequent_customers.html', customer=frequent_customer)

    except Exception as e:
        print(f"Error fetching frequent customers: {e}")
        flash("An error occurred while fetching frequent customers.")
        return redirect(url_for('airline_staff'))
    


@app.route('/view_customer_flights', methods=['GET'])
def view_customer_flights():
    customer_email = request.args.get('email')  # Passed from a link or form

    try:
        username = session.get('username')
        cursor = db.cursor()

        # Fetch airline name
        query = "SELECT airline_name FROM employed_by WHERE username = %s"
        cursor.execute(query, (username,))
        airline_name = cursor.fetchone()['airline_name']

        # Fetch flights for the given customer
        query = """
        SELECT ticket.flight_number, ticket.depart_date, ticket.depart_time, 
               flight.depart_airport_code, flight.arrival_airport_code
        FROM ticket
        JOIN purchase ON ticket.ticket_id = purchase.ticket_id
        JOIN flight ON flight.flight_number = ticket.flight_number
        WHERE purchase.email_address = %s AND flight.airline_name = %s
        """
        cursor.execute(query, (customer_email, airline_name))
        flights = cursor.fetchall()

        return render_template('view_customer_flights.html', flights=flights, customer_email=customer_email)

    except Exception as e:
        print(f"Error fetching customer flights: {e}")
        flash("An error occurred while fetching the customer's flights.")
        return redirect(url_for('airline_staff'))



@app.route('/view_revenue', methods=['GET'])
def view_revenue():
    try:
        username = session['username']  # Get logged-in staff username
        cursor = db.cursor()

        # Get the airline name the staff is associated with
        query_airline = """
        SELECT airline_name FROM Employed_By WHERE username = %s
        """
        cursor.execute(query_airline, (username,))
        airline_name = cursor.fetchone()['airline_name']

        # Calculate revenue for the last month
        query_last_month = """
        SELECT SUM(ticket.calculated_price) AS revenue_last_month
        FROM ticket
        INNER JOIN purchase ON ticket.ticket_id = purchase.ticket_id
        WHERE ticket.airline_name = %s
        AND purchase.purchase_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
        """
        cursor.execute(query_last_month, (airline_name,))
        revenue_last_month = cursor.fetchone()['revenue_last_month'] or 0

        # Calculate revenue for the last year
        query_last_year = """
        SELECT SUM(ticket.calculated_price) AS revenue_last_year
        FROM ticket
        INNER JOIN purchase ON ticket.ticket_id = purchase.ticket_id
        WHERE ticket.airline_name = %s
        AND purchase.purchase_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
        """
        cursor.execute(query_last_year, (airline_name,))
        revenue_last_year = cursor.fetchone()['revenue_last_year'] or 0

        cursor.close()

        # Render the revenue information on a new HTML page
        return render_template('view_revenue.html', revenue_last_month=revenue_last_month, revenue_last_year=revenue_last_year)

    except Exception as e:
        print(f"Error retrieving revenue data: {e}")  # Debugging
        flash("An error occurred while retrieving revenue data.")
        return redirect(url_for('airline_staff'))



def check_if_flight_exists(airline, flight_num, depart_date, depart_time):
    curs = db.cursor()
    query = "SELECT * FROM flight WHERE airline_name = %s AND flight_number = %s AND depart_date = %s AND depart_time = %s"
    
    try:
        output = curs.execute(query, (airline, flight_num, depart_date, depart_time))
        output = curs.fetchall()
        if output:
            return True
        else:
            return False
    except:
        return False

@app.route('/add_flight', methods = ["GET", "POST"])
def create_flight():
    if (request.method == "POST"):
        flight_number = request.form.get('flight_number')
        departing_airport_code = request.form.get('depart_airport_code')
        depart_date = request.form.get('depart_date')
        depart_time = request.form.get('depart_time')
        destination_airport_code = request.form.get('arrival_airport_code')
        arrival_date = request.form.get('arrival_date')
        arrival_time = request.form.get('arrival_time')
        base_price = request.form.get('base_price')
        status = request.form.get('status')
        airplane_id_number = request.form.get('airplane_id')
        
        dobj = datetime.strptime(depart_date, "%Y-%m-%d").date()
        current_date = date.today()
        in_future = current_date < dobj
        
        curs = db.cursor()
        query1 = "INSERT INTO flight VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        
        query2 = " SELECT * FROM Employed_By where username = %s"
        curs.execute(query2, session.get('username'))
        output = curs.fetchall()
        airline_name = output[0]["airline_name"]
                
        if (not (check_if_flight_exists(airline_name, flight_number, depart_date, depart_time))) & in_future:
            curs.execute(query1, (airline_name, flight_number, depart_date, depart_time, departing_airport_code, arrival_date, arrival_time, destination_airport_code, base_price, status, airplane_id_number))
            db.commit()
            curs.close()
            return redirect(url_for('airline_staff'))
        else:
            curs.close()
            error = "flight already exists"
            return redirect(url_for('airline_staff'))
    else:
        return redirect(url_for('airline_staff'))

@app.route('/change_flight_status', methods=["GET", "POST"])
def change_flight_status():
    if request.method == "POST":
        try:
            # Retrieve form data
            flight_number = request.form.get('flight_number')
            depart_date = request.form.get('depart_date')
            depart_time = request.form.get('depart_time')
            flight_status = request.form.get('status')

            if not (flight_number and depart_date and depart_time and flight_status):
                flash("All fields are required to change the flight status.", "error")
                return redirect(url_for('airline_staff'))

            # Get the airline name for the logged-in staff
            cursor = db.cursor()
            query_airline = "SELECT airline_name FROM Employed_By WHERE username = %s"
            cursor.execute(query_airline, (session.get('username'),))
            airline_data = cursor.fetchone()

            if not airline_data:
                flash("Could not verify airline for the logged-in user.", "error")
                return redirect(url_for('airline_staff'))

            airline_name = airline_data["airline_name"]

            # Check if the flight exists
            if check_if_flight_exists(airline_name, flight_number, depart_date, depart_time):
                # Update the flight status
                query_update_status = """
                    UPDATE flight 
                    SET flight_status = %s 
                    WHERE airline_name = %s AND flight_number = %s AND depart_date = %s AND depart_time = %s
                """
                cursor.execute(query_update_status, (flight_status, airline_name, flight_number, depart_date, depart_time))
                db.commit()
                flash("Flight status updated successfully.", "success")
            else:
                flash("Error: Flight does not exist. Please check the flight details.", "error")

            cursor.close()
            return redirect(url_for('airline_staff'))

        except Exception as e:
            print(f"Error while changing flight status: {e}")  # Debugging
            flash("An error occurred while changing the flight status. Please try again.", "error")
            return redirect(url_for('airline_staff'))

    # Redirect for non-POST requests
    return redirect(url_for('airline_staff'))


def check_airport_exists(code):
    curs = db.cursor()
    query = "SELECT * FROM Airport WHERE code = %s"
    
    try:
        curs.execute(query, (code))
        output = curs.fetchall()
        if (output):
            return True
        else:
            return False
    except:
        return False

@app.route('/add_airport', methods = ["POST"])
def add_airport():
    if (request.method == "POST"):
        code = request.form.get('code')
        name = request.form.get('name')
        city = request.form.get('city')
        country = request.form.get('country')
        number_of_terminals = request.form.get('number_of_terminals')
        type = request.form.get('type')
        
        
        curs = db.cursor()
        query1 = "INSERT INTO airport VALUES (%s, %s, %s, %s, %s, %s)"
        
        if not (check_airport_exists(code)):
            curs.execute(query1, (code, name, city, country, number_of_terminals, type))
            db.commit()
            curs.close()
            return redirect(url_for('airline_staff'))
        else:
            curs.close()
            error = "Airport already exists!"
            return redirect(url_for('airline_staff'))
    else:
        return redirect(url_for('airline_staff'))

def check_airplane_exists(airline_name, id):
    curs = db.cursor()
    query = "SELECT * FROM Airplane WHERE airline_name = %s AND id = %s"
    
    try:
        curs.execute(query, (airline_name, id))
        output = curs.fetchall()
        if output:
            return True
        else:
            return False
    except:
        return False

#missing maintenance id in airplane sql
#missing airline name in airline staff dashboard html
@app.route('/add_airplane', methods = ['POST'])
def add_airplane():
    if (request.method == "POST"):
        id_number = request.form.get('id_number')
        number_of_seats = request.form.get('num_of_seats')
        manufacturing_company = request.form.get('manufacturing_company')
        model_number = request.form.get('model_number')
        manufacturing_date = request.form.get('manufacturing_date')
        age = request.form.get('age')
        
        curs = db.cursor()
        query1 = "INSERT INTO Airplane VALUES (%s, %s,NULL , %s, %s, %s, %s, %s)"
        
        query2 = " SELECT * FROM Employed_By where username = %s"
        curs.execute(query2, session.get('username'))
        output = curs.fetchall()
        airline_name = output[0]["airline_name"]
        
        if not check_airplane_exists(airline_name, id_number):
            curs.execute(query1, (airline_name, id_number, number_of_seats, manufacturing_company, model_number, manufacturing_date, age))
            db.commit()
            curs.close()
            return redirect(url_for('airline_staff'))
        else:
            curs.close()
            error = "Airplane already exists!"
            return redirect(url_for('airline_staff'))
    else:
        return redirect(url_for('airline_staff'))

def maintenance_exists(id):
    curs = db.cursor()
    query = "SELECT * FROM Maintenance WHERE id = %s"
    
    try:
        output = curs.execute(query, (id))
        if (output[0] == id):
            return True
        else:
            return False
    except:
        return False

@app.route('/schedule_maintenance', methods = ['POST'])
def schedule_maintenance():
    if (request.method == "POST"):
        airplane_id = request.form.get('airplane_id')
        id = request.form.get('maintenance_id')
        start_date = request.form.get('start_date')
        start_time = request.form.get('start_time')
        end_date = request.form.get('end_date')
        end_time = request.form.get('end_time')
        
        curs = db.cursor()
        query1 = "INSERT INTO Maintenance VALUES (%s, %s, %s, %s, %s)"
        query2 = "UPDATE Airplane SET maintenance_id = %s WHERE airline_name = %s AND airplane_id_number = %s"
        
        query3 = " SELECT * FROM Employed_By where username = %s"
        curs.execute(query3, session.get('username'))
        output = curs.fetchall()
        airline_name = output[0]["airline_name"]
        
        if not (maintenance_exists(id)):
            curs.execute(query1, (id, start_date, start_time, end_date, end_time))
            curs.execute(query2, (id, airline_name, airplane_id))
            db.commit()
            curs.close()
            return redirect(url_for('airline_staff'))
        else:
            curs.close()
            error = "ERROR: Maintenance already exists!"
            return redirect(url_for('airline_staff'))
    else:
        return redirect(url_for('airline_staff'))

@app.route('/rating.html', methods = ['GET'])
def ratings():
    if request.method == "GET":
        try:
            if (session['email_address']):
                return render_template('rating.html')
        except:
            return render_template('customer_dashboard.html')

    return render_template('customer_dashboard.html')

@app.route('/view_flight_ratings', methods=['GET', 'POST'])
def view_flight_ratings():
    if 'username' not in session:
        flash("Please log in as an airline staff to view flight ratings.", "error")
        return redirect(url_for('airline_staff_login_page'))

    try:
        cursor = db.cursor()
        
        # Fetch airline name of the logged-in staff
        query_airline = """
        SELECT airline_name FROM Employed_By WHERE username = %s
        """
        cursor.execute(query_airline, (session['username'],))
        airline_data = cursor.fetchone()

        if not airline_data:
            flash("Airline information could not be retrieved.", "error")
            return redirect(url_for('airline_staff_dashboard'))

        airline_name = airline_data['airline_name']

        # Fetch flights operated by the airline with average rating and comments
        query_ratings = """
        SELECT 
            f.flight_number,
            f.depart_date,
            f.depart_time,
            f.arrival_airport_code,
            f.depart_airport_code,
            COALESCE(AVG(r.rating), 0) AS average_rating,
            GROUP_CONCAT(CONCAT(r.rating, ' - ', r.comment) SEPARATOR '; ') AS comments
        FROM 
            flight f
        LEFT JOIN 
            reviews r ON f.flight_number = r.flight_number 
            AND f.depart_date = r.depart_date
            AND f.depart_time = r.depart_time
        WHERE 
            f.airline_name = %s
        GROUP BY 
            f.flight_number, f.depart_date, f.depart_time, f.arrival_airport_code, f.depart_airport_code
        """
        cursor.execute(query_ratings, (airline_name,))
        ratings_data = cursor.fetchall()

        return render_template('view_flight_ratings.html', ratings=ratings_data)

    except Exception as e:
        print(f"Error fetching flight ratings: {e}")
        flash("An error occurred while retrieving flight ratings. Please try again.", "error")
        return redirect(url_for('airline_staff_dashboard'))



@app.route('/submit_rating', methods=['POST'])
def submit_ratings():
    if request.method == 'POST':
        try:
            # Check if the customer is logged in
            if 'email_address' not in session:
                flash("Please log in to submit a rating.", "error")
                return redirect(url_for('customer_login_page'))

            # Retrieve form data
            email_address = session['email_address']
            airline_name = request.form.get('airline_name')
            flight_number = request.form.get('flight_number')
            depart_date = request.form.get('depart_date')
            depart_time = request.form.get('depart_time')
            rating = request.form.get('rating')
            comment = request.form.get('comments')

            if not (airline_name and flight_number and depart_date and depart_time and rating):
                flash("All fields are required to submit a rating.", "error")
                return redirect(url_for('ratings'))

            cursor = db.cursor()

            # Check if the flight exists
            query_check_flight = """
            SELECT * 
            FROM flight 
            WHERE airline_name = %s AND flight_number = %s AND depart_date = %s AND depart_time = %s and depart_time = %s and depart_date < CURRENT_DATE() and  depart_date < CURRENT_TIME()
            """
            cursor.execute(query_check_flight, (airline_name, flight_number, depart_date, depart_time))
            flight = cursor.fetchone()

            if not flight:
                flash("The flight does not exist. Please check the details.", "error")
                return redirect(url_for('ratings'))

            # Insert the rating into the reviews table
            query_insert_rating = """
            INSERT INTO reviews (email_address, airline_name, flight_number, depart_date, depart_time, rating, comment)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query_insert_rating, (email_address, airline_name, flight_number, depart_date, depart_time, rating, comment))
            db.commit()
            flash("Rating submitted successfully!", "success")

            return redirect(url_for('customer'))

        except Exception as e:
            print(f"Error submitting rating: {e}")  # Debugging
            flash("An error occurred while submitting your rating. Please try again.", "error")
            return redirect(url_for('ratings'))
    return redirect(url_for('ratings'))

            
@app.route("/registration_for_airline_staff_page.html", methods = ["GET", "POST"])
def register_airline_staff():
    if (request.method == "POST"):
        username = request.form.get('username')
        password = md5(request.form.get('password').encode()).hexdigest()
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        dob = request.form.get('date_of_birth')
        phone_number = request.form.get('phone_number')
        email_address = request.form.get('email_address')
        airline_name = request.form.get('airline_name')
        
        curs = db.cursor()
        query1 = "INSERT INTO airline_staff VALUES (%s, %s, %s, %s, %s)"
        query2 = "INSERT INTO airline_staff_email_address VALUES (%s, %s)"
        query3 = "INSERT INTO airline_staff_phone_number VALUES (%s, %s)"
        query4 = "INSERT INTO employed_by VALUES (%s, %s)"
           
        if not (airline_staff_exists(username)):
            curs.execute(query1, (username, password, first_name, last_name, dob))
            curs.execute(query2, (username, email_address))
            curs.execute(query3, (username, phone_number))
            curs.execute(query4, (airline_name, username))
            
            db.commit()
            curs.close()
            return render_template('airline_staff_login_page.html')
        else:
            curs.close()
            error = "ERROR: Airline Staff Member Already Exists!"
            return render_template('registration_for_airline_staff_page.html', error=error)
    else:
        return render_template('registration_for_airline_staff_page.html')
    
@app.route("/registration_for_customer_page.html", methods = ["GET", "POST"])
def register_customer():
    if (request.method == "POST"):
        email_address = request.form.get('email_address')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = md5(request.form.get('password').encode()).hexdigest()
        building_number = request.form.get('building_number')
        street = request.form.get('street')
        apt_number = request.form.get('apt_number')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')
        phone_number = request.form.get('phone_number')
        passport_number = request.form.get('passport_number')
        passport_expiration = request.form.get('passport_expiration')
        passport_country = request.form.get('passport_country')
        dob = request.form.get('date_of_birth')
        
        curs = db.cursor()
        query1 = "INSERT INTO customer VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        query2 = "INSERT INTO customerphone VALUES (%s, %s)"
           
        if not (customer_exists(email_address)):
            curs.execute(query1, (email_address, first_name, last_name, password, building_number,street, apt_number, city, state, zipcode, passport_number, passport_expiration, passport_country, dob))            
            curs.execute(query2, (email_address, phone_number))
            
            db.commit()
            curs.close()
            return render_template('customer_login_page.html')
        else:
            curs.close()
            error = "ERROR: customer Already Exists!"
            return render_template('registration_for_customer_page.html', error=error)
    else:
        return render_template('registration_for_customer_page.html')
            
@app.route('/customer_logout', methods=['GET'])
def customer_logout():
    # Clear the session data
    session.pop('email', None)
    # Redirect to the customer login page
    return render_template('index.html')

@app.route('/airline_staff_logout', methods=['GET'])
def airline_staff_logout():
    # Clear the session data
    session.pop('username', None)
    # Redirect to the airline staff login page
    return render_template('index.html')


@app.route('/generate_report', methods=['GET', 'POST'])
def generate_report():
    try:
        username = session['username']  # Get logged-in staff username
        cursor = db.cursor()

        # Get the airline name the staff is associated with
        query_airline = """
        SELECT airline_name FROM Employed_By WHERE username = %s
        """
        cursor.execute(query_airline, (username,))
        airline_name = cursor.fetchone()['airline_name']

        # Default report parameters
        start_date = request.form.get('start_date', '2023-01-01')
        end_date = request.form.get('end_date', '2024-12-31')
        flight_status = request.form.get('flight_status', None)

        # Build the SQL query dynamically
        query = """
        SELECT flight.flight_number, flight.depart_date, flight.depart_time, 
               flight.arrival_date, flight.arrival_time, flight.flight_status, 
               SUM(ticket.calculated_price) AS revenue
        FROM flight
        LEFT JOIN ticket ON flight.airline_name = ticket.airline_name AND flight.flight_number = ticket.flight_number
        LEFT JOIN purchase ON ticket.ticket_id = purchase.ticket_id
        WHERE flight.airline_name = %s AND flight.depart_date BETWEEN %s AND %s
        """
        params = [airline_name, start_date, end_date]

        if flight_status:
            query += " AND flight.flight_status = %s"
            params.append(flight_status)

        query += " GROUP BY flight.flight_number, flight.depart_date, flight.depart_time, flight.arrival_date, flight.arrival_time, flight.flight_status"

        cursor.execute(query, params)
        report_data = cursor.fetchall()

        cursor.close()

        # Render the report on a new HTML page
        return render_template('generate_report.html', report_data=report_data, start_date=start_date, end_date=end_date, flight_status=flight_status)

    except Exception as e:
        print(f"Error generating report: {e}")  # Debugging
        flash("An error occurred while generating the report.")
        return redirect(url_for('airline_staff'))
    
@app.route('/track_spending', methods=['GET', 'POST'])
def track_spending():
    try:
        # Ensure the customer is logged in
        if "email_address" not in session:
            flash("Please log in to track your spending.")
            return redirect(url_for('customer_login_page'))

        email_address = session["email_address"]
        cursor = db.cursor()

        # Handle default or custom date range
        if request.method == 'POST':
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')
        else:
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=365)

        # Query total spending for the date range
        query = """
        SELECT SUM(ticket.calculated_price) AS total_spent
        FROM purchase
        JOIN ticket ON purchase.ticket_id = ticket.ticket_id
        WHERE purchase.email_address = %s
        AND purchase.purchase_date BETWEEN %s AND %s
        """
        cursor.execute(query, (email_address, start_date, end_date))
        result = cursor.fetchone()
        total_spent = result['total_spent'] if result['total_spent'] else 0

        # Query monthly spending for the date range
        query_monthly = """
        SELECT DATE_FORMAT(purchase.purchase_date, '%%Y-%%m') AS month,
               SUM(ticket.calculated_price) AS monthly_spent
        FROM purchase
        JOIN ticket ON purchase.ticket_id = ticket.ticket_id
        WHERE purchase.email_address = %s
        AND purchase.purchase_date BETWEEN %s AND %s
        GROUP BY month
        ORDER BY month ASC
        """
        cursor.execute(query_monthly, (email_address, start_date, end_date))
        monthly_spending = cursor.fetchall()

        # Generate bar chart for monthly spending
        months = [row['month'] for row in monthly_spending]
        amounts = [row['monthly_spent'] for row in monthly_spending]

        plt.figure(figsize=(10, 6))
        plt.bar(months, amounts, color='blue')
        plt.title("Monthly Spending")
        plt.xlabel("Month")
        plt.ylabel("Amount Spent")
        plt.xticks(rotation=45)

        # Convert plot to base64 string
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        chart_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        plt.close()

        # Query detailed spending for the table
        query_details = """
        SELECT flight.airline_name, flight.flight_number, ticket.calculated_price, 
               purchase.purchase_date, flight.depart_date, flight.arrival_date
        FROM purchase
        JOIN ticket ON purchase.ticket_id = ticket.ticket_id
        JOIN flight ON ticket.flight_number = flight.flight_number
        WHERE purchase.email_address = %s
        AND purchase.purchase_date BETWEEN %s AND %s
        """
        cursor.execute(query_details, (email_address, start_date, end_date))
        spending_details = cursor.fetchall()

        cursor.close()

        # Render the spending tracking page
        return render_template(
            'track_spending.html',
            total_spent=total_spent,
            spending_details=spending_details,
            chart_base64=chart_base64,
            start_date=start_date,
            end_date=end_date,
            monthly_spending=monthly_spending
        )

    except Exception as e:
        print(f"Error tracking spending: {e}")
        flash("An error occurred while tracking your spending.")
        return redirect(url_for('customer'))

        
if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug = True)
    
