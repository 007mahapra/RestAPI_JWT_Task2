# A Web App to demonstrate JWT , login , token timeout and handling user api permission based on user's role 

This project helps to get the demonstrate JWT , login , token timeout and handling user api permission based on user's role. 
It uses the SQLite  as database to keep things simple as the focus is to demonstrate the JWT.

This README provides an overview of the available API endpoints for managing ransomware data. The API allows you to load, create, retrieve, update, and delete ransomware records stored in a MongoDB database. The endpoints are accessible through standard HTTP methods.

## Features
1. Create user and login
2. generate JWT token in the backend with the help of JWT_SECRET_KEY.
3. JWT token will be valid for specified period of time only.
4. Get appropriate response based on the user role.
5. User can only access the api which is allowed to the user based on the user role.


## Tech Stack

- **Python**: Python is the primary programming language used for building the API. I have used Flask from Python to create the API.
- **SQlite**:SQLite is a lightweight, serverless, and zero-configuration database management system. It is used in this project to store the table data.
 Product and user table are created.
- **HTML and JavaScript** : The frontend of the API is built using HTML and JavaScript.


## Prerequisites
This project can be executed on any machine with the following prerequisites:

- Python 3.x
   - Libraries: Flask, pymongo  [Python Required Libraries](requirements.txt)
- SQLite installed and running

But for the ease of use I have used docker to run the project. Here are the steps to run the project using Docker:

Note : Docker should be installed on your machine and docker-compose should be installed.

## Installation steps

1. Clone the repository:

```bash 
git clone https://github.com/007mahapra/RestAPI_JWT_Task2.git
```
2. Navigate to the project directory: Ransomware-API-Docker
3. Run the Docker image: 
   ```bash
   cd docker
   docker-compose up --build
   ```
4. Access the API at http://localhost:5000
5. This project also has frontend which can be accessed at http://localhost:5000 and the frontend is built using HTML and JavaScript.
6. The frontend is already configured to use the API endpoints, so you can interact with the API directly from the frontend and perform various operations.



## Front End documentation
The frontend is built using HTML and JavaScript. It has basic HTML, CSS, and JavaScript code to display the records and test user role feature. 

I have used JavaScript to make the API calls to the backend API . The Front end allows to demonstrate login, user role based api access.

Front end can be accessed at http://localhost:5000 

Guide is uploaded here for the frontend. [Front End Guide & Perofmed steps](guide_steps)

Note: The UI is bit basic as the focus is to demonstrate the JWT. Please expect visual issues.  Logout and login again if anything funny happens.


## API Endpoints to interact with the API | Documentation

Note : You will need to get the JWT token from the backend to access the api as the api is protected.

Here are minimal `curl` API requests for each route of your Flask application:

### 1. **Login (POST /login)**
```bash
curl -X POST http://localhost:5000/login \
-H "Content-Type: application/json" \
-d '{"username": "admin", "password": "password"}'
```

### 2. **Create User (POST /user)**  
- Requires `x-access-token` (JWT from the login route).
```bash
curl -X POST http://localhost:5000/user \
-H "Content-Type: application/json" \
-H "x-access-token: <YOUR_JWT_TOKEN>" \
-d '{"username": "newuser", "password": "newpassword", "role": "privileged"}'
```

### 3. **Get Products (GET /products)**  
- Requires `x-access-token`.
```bash
curl -X GET http://localhost:5000/products \
-H "x-access-token: <YOUR_JWT_TOKEN>"
```

### 4. **Add Product (POST /product)**  
- Requires `x-access-token`.
```bash
curl -X POST http://localhost:5000/product \
-H "Content-Type: application/json" \
-H "x-access-token: <YOUR_JWT_TOKEN>" \
-d '{"name": "Product1", "description": "Sample product description"}'
```

### 5. **Get Product by ID (GET /product/<product_id>)**  
- Requires `x-access-token`.
```bash
curl -X GET http://localhost:5000/product/1 \
-H "x-access-token: <YOUR_JWT_TOKEN>"
```

### 6. **Get All Users (GET /users)**  
- Requires `x-access-token` (Admin access).
```bash
curl -X GET http://localhost:5000/users \
-H "x-access-token: <YOUR_JWT_TOKEN>"
```

### Notes:
- Replace `<YOUR_JWT_TOKEN>` with the token returned from the `/login` request.
- Modify the `localhost:5000` URL if your Flask app is hosted elsewhere or running on a different port.


## Want to run the project locally ?

# To run manually
- 1. Install packages
```bash
pip install --no-cache-dir -r requirements.txt
```

- 2. Set default app to server.py
```bash 
# if powershell 
$env:FLASK_AP = "server.py"
# if Linux Shell
export FLASK_AP="server.py"
```

- 3. Run it manually 
```bash 
flask run --host=0.0.0.0  
```

The application will be accessible at `http://localhost:5000`.

## References
Datatables : https://datatables.net/
Mongodb : https://www.mongodb.com/
https://blog.logrocket.com/build-deploy-flask-app-using-docker/




