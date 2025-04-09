

# Airline Booking System

Welcome to the Airline Booking System project! This web application allows users to book flights, manage their reservations, and interact with an admin interface for staff to view and manage bookings.

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation Instructions](#installation-instructions)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Description

This project is a web-based airline reservation system designed to facilitate booking, canceling, and managing flights for customers. Additionally, there is an admin interface where staff can view and manage bookings, as well as update flight availability.

The system includes:
- A login system for both customers and staff
- Flight search and booking capabilities for customers
- Admin panel for managing bookings and flights
- User-friendly interface with modern design

## Features

- **Customer Side**:
  - User registration and login
  - Search and filter flights by destination, date, and availability
  - View available flights and make bookings
  - View and cancel existing bookings

- **Admin Side**:
  - Admin login interface
  - View and manage all customer bookings
  - Add, update, or delete flight information

## Technologies Used

- **Frontend**: HTML, CSS 
- **Backend**: Python (Flask )
- **Database**: SQL (MySQL)
- **Version Control**: Git and GitHub for source code management

## Installation Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/michx02/AirlineSystem.git
   ```

2. **Install dependencies**:
   Navigate into the project directory and install the required packages using `pip` (assuming Python is installed):
   ```bash
   cd AirlineSystem
   pip install -r requirements.txt
   ```

3. **Set up the database**:
   - Ensure that your database server (MySQL/PostgreSQL) is running.
   - Use the provided `airsystem.sql` file to create the necessary tables and populate them with sample data:
     ```bash
     mysql -u root -p < airsystem.sql
     ```

4. **Run the application**:
   Start the server using:
   ```bash
   python app.py  # Or 'python manage.py' if using Django
   ```

5. **Access the application**:
   Open your browser and go to `http://127.0.0.1:5000` (or the appropriate port if configured differently).

## Usage

- Once you navigate to the application, you can log in as either a **Customer** or an **Admin**.
- Customers can book flights, view their booking history, and manage their reservations.
- Admins can log in to manage flight data and customer bookings.

## Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests with any improvements or fixes. Please follow these steps when contributing:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature-name`)
5. Create a pull request to merge your changes

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

