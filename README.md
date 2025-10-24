# Flight-Map-Explorer-MariaDB

## OVERVIEW
An interactive web application that lets users **upload airport datasets**, **insert airports manually**, and **explore nearby airports** using **MariaDB spatial features**. Built with **Python, Streamlit, and MariaDB**. The web app provides a minimap through which the airports can be visualized ( radius can be modified and results are generated accordingly) 

---

##  Features Of The web application 

-  **CSV Upload:** Import airport data easily.
-  **Interactive Map:** Visualize airports and flight routes dynamically.
-  **Nearby Airports Search:** Find airports within a specific radius from an origin airport.
-  **MariaDB Spatial Queries:** Utilizes `POINT`, `SPATIAL INDEX`, and `ST_Distance_Sphere()` for fast geospatial calculations.
-  **Python (Streamlit) :** Provides a clean and interactive user interface.

---
## Features Leveraging MariaDB

This project makes use of **MariaDB's spatial and GIS features** to deliver efficient geospatial functionality:

- **`POINT` Data Type:** Stores the latitude and longitude of each airport as a spatial point.  
- **`SPATIAL INDEX`:** Optimizes queries on geographic coordinates for faster search performance.  
- **`ST_Distance_Sphere()`:** Calculates the great-circle distance between two points on Earth, allowing accurate nearby airport searches.  
- **Spatial Queries:** Find all airports within a specified radius from a selected origin airport.    
- **Real-time Geospatial Analytics:** Combines MariaDB queries with Python (Streamlit + PyDeck) to dynamically visualize airports and flight routes on a map.  

These features ensure **fast, accurate, and scalable geospatial operations** directly in the database, reducing the need for heavy client-side computation.

---

## Technology Stack Used
-  Programming Language: Python
-  Web Framework / Frontend: Streamlit
-  Backend: MariaDB with GIS / Spatial features (POINT, SPATIAL INDEX)
-  Data Handling: Pandas (CSV parsing, dataframe operations)
-  Mapping & Visualization: PyDeck (Visualize airports and routes on maps)
---
## How to Run / Implement This Project

### Install Dependencies

- Requires python 3.12+ version and Then install required packages:
- pip install -r requirements.txt

### Set Up MariaDB

#### If hosting in Locally ( LocalHost) :
- Install the latest version of MariaDB.
- Create a database, for example openflights : CREATE DATABASE openflights;
- Create the airports table using the structure defined in spatial_GIS.py.
- Download the openflights dataset from browser and load the data into the database (optional) as we can upload the airports.csv directly into the web app.
- clone the repository and use the code ( spatial_GIS.py) ,update the database connection and run the file using the command "streamlit run <module_name>.py".

#### If hosting in skysql (Online) :
- Create a SkySQL account and set up a database service.
- Create the airports table with the structure as defined in source code and load the airport dataset.
- Create a Streamlit Cloud account to host the web app online.
- Use the spatial_GIS_network.py code and update the connection credentials to your SkySQL database.
- Deploy the Streamlit app via Streamlit Cloud for online access. 
---

##Author : ARAVIND R S 
