# Application and Exam Tracker API

A backend REST API built with Python and FastAPI to track and manage job applications and competitive exam schedules. 

This project provides a programmatic alternative to manual spreadsheet tracking. It uses an SQLite database for storage and includes custom search filters.

## Features
* **CRUD Operations:** Endpoints to create, read, update, and delete application records.
* **Database Integration:** Uses SQLite and SQLAlchemy ORM for data storage.
* **Query Filtering:** Filter database entries by `status` or `category` via URL query parameters.
* **Data Validation:** Uses Pydantic schemas to validate incoming API requests and format responses.
* **API Documentation:** Includes an auto-generated Swagger UI for testing endpoints.

## Tech Stack
* **Language:** Python 3.x
* **Framework:** FastAPI
* **Database & ORM:** SQLite, SQLAlchemy
* **Validation:** Pydantic
* **Server:** Uvicorn

## Local Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/exam_tracker_api.git](https://github.com/yourusername/exam_tracker_api.git)
   cd exam_tracker_api

2. **Create and activate a virtual environment:**
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv  
   source venv/bin/activate

3. **Install dependencies:**
   pip install fastapi uvicorn sqlalchemy pydantic

4. **Run the development server:**
   uvicorn main:app --reload

5. **Access the API:**
   
* Base URL: http://127.0.0.1:8000

* Interactive Docs (Swagger UI): http://127.0.0.1:8000/docs

** API Endpoints **

| Method | Endpoint | Description
|---|---|---|
|GET| / | Returns API health status|
|POST| /items | Add a new tracked item |
|GET|/items |Retrieve items (Supports ?status= and ?category= filters)|
|PUT|/items/{id} | Update an existing item by its ID|
|DELETE|/items/{id}| Delete an item by its ID|

** AUTHOR **
Deepak
