NAME AND SURNAME: LETLOTLO KUAHO
STUDENT ITS No: 402604546
QUALIFICATION: BSC IT
YEAR OF STUDY: 1
ASSIGNMENT DUE DATE:23/10/26                          DATE SUBMITTED: 23/10/26

HOW TO RUN:
1. Ensure the project folder is open in your IDE (e.g., PyCharm or VS Code).

2. Locate the main.py file.

3. Right-click and select Run 'main' (or run python main.py in the terminal).

4. The Login Window will appear.

DEFAULT LOGIN CREDENTIALS

Role	Campus	Username	Password
Campus Admin	Johannesburg	admin_jhb	admin123
Campus Admin	Cape Town	admin_cpt	admin123
Campus Admin	Durban	admin_dbn	admin123
System Operator	All Campuses	operator	op123
Lecturer	Any	(Register via GUI)	(Create your own)

SYSTEM DESIGN & ARCHITECTURE 
Object-Oriented Design
The system uses encapsulation and inheritance to manage users.

   The base class User handles common attributes (username, role, campus).
 Subclasses (Lecturer, CampusAdmin, SystemOperator) inherit from User but have specific permissions and dashboard access.

Database Schema (SQLite)
The system uses a relational database with four tables to ensure data integrity:
 users: Stores login credentials and roles.
 campuses: Stores the three distinct campuses.
 resources: Stores rooms/equipment. Enforces a UNIQUE constraint on resource_code to prevent duplicates.
 bookings: Links lecturers to resources and enforces time/date rules.
Business Logic & Booking Rules
To satisfy the requirement for design flexibility, booking rules are separated into a dictionary in booking_rules.py.
 Johannesburg: Max 2 hours, 07:00 - 18:00.
 Cape Town: Max 4 hours, 08:00 - 21:00.
 Durban: Max 90 minutes, 08:00 - 16:00

TESTING AND VALIDATION
The following test cases were executed to verify the system:

Test Case	Expected Result	Actual Result
Log in with incorrect password	Error popup: "Incorrect password"	Passed
Lecturer attempts to book a JHB lab for 200 mins	Error popup: "Allows max 120 mins"	Passed
Lecturer attempts to double-book a room	Error popup: "Already booked for time slot"	Passed
Admin adds a resource with an existing code	Error popup: "UNIQUE constraint failed"	Passed
Lecturer cancels a past booking	Error popup: "Past bookings cannot be cancelled"	Passed
Close app and reopen	Database remembers users and bookings	Passed