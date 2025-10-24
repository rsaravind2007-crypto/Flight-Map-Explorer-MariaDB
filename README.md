# Flight-Map-Explorer-MariaDB

## OVERVIEW
An interactive web application that lets users **upload airport datasets**, **insert airports manually**, and **explore nearby airports** using **MariaDB spatial features**. Built with **Python, Streamlit, and MariaDB**. The web app provides a minimap through which the airports can be visualized ( radius can be modified and results are generated accordingly) 

---

##  Features

-  **CSV Upload:** Import airport data easily.
-  **Interactive Map:** Visualize airports and flight routes dynamically.
-  **Nearby Airports Search:** Find airports within a specific radius from an origin airport.
-  **MariaDB Spatial Queries:** Utilizes `POINT`, `SPATIAL INDEX`, and `ST_Distance_Sphere()` for fast geospatial calculations.
-  **Python (Streamlit) :** Provides a clean and interactive user interface.

---
## Technology Stack Used
-Programming Language: Python
-Web Framework / Frontend: Streamlit
-Backend: MariaDB with GIS / Spatial features (POINT, SPATIAL INDEX)
-Data Handling: Pandas (CSV parsing, dataframe operations)
-Mapping & Visualization: PyDeck (Visualize airports and routes on maps)
---
## How to Run / Implement This Project

## Install Dependencies

-Requires python 3.12+ version and Then install required packages:
-pip install -r requirements.txt

### Set Up MariaDB

-Download the latest version of MariaDB
-Create a database, for example openflights : CREATE DATABASE openflights;
-create a table airports with the stucture defined in the source code ( 
-Download the openflights dataset from browser and load the data into the database (optional) 


