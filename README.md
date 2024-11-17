Face Recognition System

Overview:**
**
This project implements a Python-based **Face Recognition System ** designed for real-time attendance tracking and management. It leverages cutting-edge libraries like face_recognition and OpenCV for facial feature detection and recognition. **MongoDB** and **MySQL** are used for efficient data storage and retrieval, supporting multiple branch setups with multi-camera configurations.

**Features:**

1.Real-Time Face Recognition: Accurate facial detection and encoding using live camera feeds.

2.Multi-Camera Support: Monitors multiple branches simultaneously.

3.Attendance Tracking: Automatically logs attendance in MySQL databases.

4.Dynamic User Management:

Add new users with facial encodings.

Remove users by ID or batch file.

5.Optimized Algorithms:

Fast encoding computation with face_recognition.

Sorting and searching using custom algorithms for efficiency.

---

**Tech Stack**

1.Programming Language: Python 3.8+

2.Libraries:

face_recognition: For face detection and encoding.

OpenCV: For camera feed handling and image processing.

pymongo: For MongoDB interactions.

mysql-connector-python: For MySQL database management.

multiprocessing: For parallel processing of camera feeds.

3.Databases:

MongoDB: For storing face encodings.

MySQL: For employee and attendance records.

---

**Installation**

Prerequisites

Ensure the following are installed:

Python 3.8+

MongoDB and MySQL

Required Python Libraries (listed in requirements.txt)

Setup

1. Clone the Repository:

git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name


2. Install Dependencies:

pip install -r requirements.txt


3. Database Setup:

MongoDB: Create a database (project) and a collection (val) to store encodings.

MySQL: Create a database (aTest) with tables for employees, branches, and attendance logs.


4. Update Configuration:

Update MongoDB and MySQL credentials in main.py.


5. Run the System:

python main.py

---

How It Works

1. User Registration:

Captures face encodings using a webcam.

Stores user data (ID, name, branch) and encodings in MongoDB.


2. Real-Time Recognition:

Uses camera feeds to detect and match faces against stored encodings.

Logs attendance in MySQL with timestamps.


3. Dynamic Updates:

Supports adding/removing users and updating encodings seamlessly.


4. Multi-Branch Support:

Monitors multiple branches and cameras simultaneously using multiprocessing.

---

File Structure

├── main.py                 # Main script for the face recognition system
├── requirements.txt        # List of dependencies
├── input/                  # Directory for input images (optional)
├── README.md               # Documentation
├── .gitignore              # Excluded files and folders
└── LICENSE                 # Project license

---

**Future Enhancements**

Cloud Integration: Use AWS or Google Cloud for database scalability.

Security Features: Implement anti-spoofing techniques.

Performance Optimization: Reduce latency for faster recognition.

User Interface: Add a graphical UI for easier system interaction.

---

Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository.

2. Create a new branch (feature-name).

3. Make changes and test thoroughly.

4. Submit a pull request for review.

---

License

This project is licensed under the MIT License.

---

Contact:

Author: Haritha Lavakumar
Email: harithalavakumar@gmail.com
Feel free to reach out with questions, feedback, or feature requests!
