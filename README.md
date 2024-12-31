# School Attendance Tracker

This is a simple web application for tracking school attendance. It allows users to mark attendance and view attendance history.

## Features


- Mark attendance with date, status (present/absent), and notes
- View attendance history

## Requirements

- Python 3.x
- Flask
- SQLite3

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/school-attendance-tracker.git
    cd school-attendance-tracker
    ```

2. Install the required packages:
    ```sh
    pip install flask
    ```

3. Initialize the database:
    ```sh
    python -c "from app import init_db; init_db()"
    ```


## Usage

1. Run the application:
    ```sh
    python app.py
    ```

2. Open your web browser and go to `http://127.0.0.1:5000/`.


3. Mark attendance and view attendance history.

## File Structure
school-attendance-tracker/ │ ├── app.py  ├── attendance.db ├── templates/ │ ├── index.html  └── README.md


## License

This project is licensed under the MIT License.