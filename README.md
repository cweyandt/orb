# ORB
Welcome to the Occupant Responsive Buildings (ORB) repository! Here you will find documentation to help you:
- Understand the API that connects to our Change Point Detection models
- Understand the Change Point Detection models created for predicting occupancy based on Wi-Fi data
- Understand how the ground truth for model accuracy was created

## Getting Started
ORB is designed to be run entirely in `docker`. These instruction assume that `docker` has already been installed on the host system and is updated to the most current version.  

Prerequisites:
- `git`
- `docker`

### Working with the docker containers:
1. Clone the ORB repository from github:  
`git clone https://github.com/cweyandt/orb.git`

   
2. Change directory to the repository:  
`cd orb`
     

3. Build the docker images:  
`docker compose build`  

   
4. Start the docker containers in detached mode:  
`docker compose up -d`
   

5. View container logs:  
a. `docker compose logs`  - view existing logs for all containers  
b. `docker compose logs -f`  - stream new logs for all containers (CTRL+C to exit)  
c. `docker compose logs -f orb` - stream logs for a specific container [orb, nginx, jupyter]  


6. Stop the ORB applications:  
`docker compose down`

### Using ORB:
The following URLs are used to access ORB resources:
1. http://localhost/    -  Website
2. http://localhost:8888/    -   JupyterLab
3. http://localhost/api/v1/docs    -   Swagger UI API Documentation
4. http://localhost/api/v1/redoc   - Redoc UI API Documentation
5. http://localhost/api/v1  -   API endpoint


## System specification

1. **Data collection:** is assumed to have been addressed through a data-warehousing method such as SkyFoundry's Skyspark or OSIsoft's PI applications. 

2. **Data cleansing:**

## API Reference
Following OpenAPI Specification: https://github.com/OAI/OpenAPI-Specification/tree/main/examples/v3.1

## Docker container structure
![ORB Container Architecture](./doc/orb_containers.png "ORB Container Architecture")
