# Documentation for HBnB Website

This documentation presents the architecture of an HBnB website using various UML diagrams. Each diagram highlights a specific aspect of the system, from the overall structure to detailed business logic.

## Package Diagram
### Description of the Package Diagram

The package diagram illustrates the modular structure of the system by defining the main layers and components. The system is divided into several packages representing the website's functionalities and responsibilities.

#### Main Packages

1. User

    * Manages user sign-up, login, and profile management.
    * Features: Authentication, personal information management.

2. Reservation

    * Handles search, booking, and reservation history for users.
    * Features: Search for listings, manage bookings, and payments.

3. Host

    * Allows hosts to publish and manage their listings.
    * Features: Create new listings, manage prices, and availability.

3. Property

    * Describes information related to the available properties for rent.
    * Features: Property details, photos, amenities.

4. Payment

    * Manages payments, transactions, and refunds.
    * Features: Secure payment, invoice, and refund management.

## Class Diagram

### Description of the Class Diagram

The class diagram details the main entities of the system, along with their attributes and relationships. It provides a visualization of the data structure and the interactions between the objects within the system.

#### Main Classes

1. ##### User

* ##### Attributes:
    * userID
    * name
    * email
    * password
    * address

* ##### Methods:
    * register()
    * login()
    * updateProfile()
    
2. ##### Property

* ##### Attributes:
    * propertyID
    * name
    * description
    * price
    * location
    * availability
* Methods:
    * addProperty()
    * updateAvailability()
    * showDetails()
    
3. ##### Reservation

* Attributes:
    * reservationID
    * userID
    * propertyID
    * startDate
    * endDate
    * totalAmount
* Methods:
    * makeReservation()
    * cancelReservation()
    * calculateTotalAmount()

4. ##### Payment

* Attributes:
    * paymentID
    * reservationID
    * amount
    * paymentMethod
    * status
* Methods:
    * processPayment()
    * refund()

## Sequence Diagram
## Description of the Sequence Diagram

The sequence diagram illustrates the order of interactions between objects during certain actions on the website. This diagram focuses on a key process: making a reservation.

## Reservation Process Sequence

1. #### User logs in:

    * The user enters their login credentials.
    * The system verifies the information, and the user is logged in.

2. #### User searches for properties:

    * The user enters search criteria (dates, location, etc.).
    * The system returns a list of available properties that match the criteria.

3. #### User selects a property:

    * The user selects a property from the list.
    * The system displays the details of the selected property.

4. #### User books the property:

    * The user selects their stay dates and confirms the booking.
    * The system creates a reservation and calculates the total amount.

5. #### User processes the payment:

    * The system redirects the user to the payment module.
    * The user enters payment details.
    * The system processes the transaction and confirms the payment.

6. #### Reservation is confirmed:

     * The system sends a confirmation email to the user.
    * The reservation is saved in the database.

## Conclusion
This documentation provides an overview of the architecture of an HBnB website, using different UML diagrams to describe the main components, relationships, and processes. These diagrams can be used as a basis for developing the website, offering a clear vision of the system's organization and the interaction between its various parts.