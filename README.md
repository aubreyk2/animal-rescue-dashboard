# Animal Rescue Interactive Dashboard - Python

A full-stack interactive dashboard for Grazioso Salvare, an animal rescue organization, built to manage and visualize animal rescue data.

## Technologies Used 
- Python
- MongoDB
- Pandas

## Features
- Full CRUD (Create, Read, Update, Delete) operations
- Dynamic filtering and searching
  Data visualization to support decision-making
- Reusable CRUD module separating database logic from dashboard
- CSV fallback if MongoDB connection is unavailable

## Development Approach
-Development started by breaking the project into smaller, managable components rather than tackling it all at once.
- Followed SDLC practices such as planning, development, testing, and documentation.
- Separated database logic from dashboard functionality using a reusable CRUD module.
- Designed with scalability in mind.
- Implemented MVC design pattern to keep code modular and organized as well as included input validation and error handling.

## Security
- Database credentials are not hardcoded and are passed as parameters.
- Input validation and error handling implemented throughout.
- MongoDB connection uses authentication.
- CSV fallback implemented if database connection fails.
- Sensitive data files are excluded from repository.


## Dataset This project uses the Austin Animal Center (AAC) Shelter Outcomes dataset. Download it from Kaggle: https://www.kaggle.com/datasets/aaronschlegel/austin-animal-center-shelter-outcomes-and This project also uses MongoDB sample datasets: - companies.json - city-inspections.json These can be downloaded from MongoDB's sample dataset collection. 

## Files
- datasets/aac_shelter_outcomes.csv
- CRUD_Python_Module.py
- dashboard.py
- Grazioso Salvare Logo.png

## How to Run 
1. Clone the repository
2. 2. Install dependencies: pip install -r requirements.txt
3. Connect to MongoDB database
4. Run the dashboard: python dashboard.
