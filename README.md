# Bus Trip and Station REST API Manager

This is a REST API manager for Bus Trips and Stations built using Docker and the Python Flask web framework. This application allows users to manage bus trips, stations, and related data efficiently through API endpoints.

## Prerequisites

Before running this application, you need to have the following installed on your system:

- [Docker](https://www.docker.com/get-started)
- [Python](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installing/) (Python package manager)

## Getting Started

Follow these steps to get the API manager up and running:

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/falila/stationboard.git
    ```

2. Navigate to the project directory:

    ```bash
    cd stationboard
    ```

3. Build the Docker container:

    ```bash
    docker build -t .
    ```

4. Run the Docker container:

    ```bash
    docker run -p 5000:5000
    ```

The API should now be accessible at `http://localhost:5000`.

## API Endpoints

### 1. Get All Bus Trips

- **GET /bus-trips**: Retrieves a list of all bus trips.

### 2. Get a Specific Bus Trip

- **GET /bus-trips/{trip_id}**: Retrieves a specific bus trip by its ID.

### 3. Create a New Bus Trip

- **POST /bus-trips**: Create a new bus trip.

### 4. Update a Bus Trip

- **PUT /bus-trips/{trip_id}**: Update an existing bus trip by its ID.

### 5. Delete a Bus Trip

- **DELETE /bus-trips/{trip_id}**: Delete a bus trip by its ID.

### 6. Get All Stations

- **GET /stations**: Retrieves a list of all stations.

### 7. Get a Specific Station

- **GET /stations/{station_id}**: Retrieves a specific station by its ID.

### 8. Create a New Station

- **POST /stations**: Create a new station.

### 9. Update a Station

- **PUT /stations/{station_id}**: Update an existing station by its ID.

### 10. Delete a Station

- **DELETE /stations/{station_id}**: Delete a station by its ID.

## Data Model

The data model used in this application includes two main entities: Bus Trips and Stations. The API manager provides endpoints to interact with and manage these entities effectively.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
