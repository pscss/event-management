# Event Management

## Overview

The Event Management API is a backend service designed to manage events, handle bookings, and process payments. Users can browse available events, book tickets, and make payments seamlessly through integrated third-party APIs.

### Business Logic

- **Event Listings**: Users can view detailed information about events, including name, date, location, and available tickets.
- **Event Booking**: Users can book tickets for events, and the system manages inventory to ensure availability.
- **Payment Processing**: a payment gateway to be integrated, allowing users to pay for tickets easily. Currently the payment API is a dummy API.
- **User Management**: Basic user details, such as name, email, and phone number, are stored for personalized service.

## Integrated Third-Party APIs

- **Google Maps API**: Used to display event locations on a map, providing users with visual location data.

## Docker Setup

### Prerequisites

- Docker

### Build and Run Containers

1. **Build the Docker Images**:

   ```bash
   docker-compose build
   ```

2. **Start the Containers**:

   ```bash
   docker-compose up
   ```

3. **Apply Database Migrations**:

   The migrations are automatically applied when the application starts. Ensure that the database service is healthy before accessing the application.

### Access the Application

- Open your browser and navigate to `http://localhost:8001/docs` to access the Swagger UI.

## Local Setup and Execution

### Prerequisites

- Python 3.10+
- PostgreSQL16
- Poetry (for dependency management)

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Aryank47/event-management
   cd event-management
   ```

2. **Install Dependencies**:

   ```bash
   poetry install
   ```

3. **Environment Setup**:

   override the `.env` file, if necessary in the project root with the following content:

   ```env
   DATABASE_URL=postgresql+asyncpg://<user>:<password>@localhost:<5432>/<db>
   GOOGLE_MAPS_API_KEY=<your_google_maps_api_key>
   ```

4. **Run Database Migrations**:

   ```bash
   poetry run alembic upgrade head
   ```

5. **Start the Application**:

   ```bash
   uvicorn event_manager.main:app --port 8080 --reload
   ```

6. **Access the API**:

   Open your browser and navigate to `http://localhost:8080/docs` for the Swagger UI.

## Running Tests(WORK IN PROGRESS...will not work till then)

To run tests, use the following command:

```bash
poetry run pytest
```

This command will execute all unit and integration tests defined in the project.

## Conclusion

The Event Management API is a comprehensive solution for managing events, bookings, and payments. By following the setup instructions, you can run the application locally or in a Docker container.
