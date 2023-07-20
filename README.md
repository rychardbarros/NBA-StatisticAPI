# NBA-StatisticAPI
🏀 Here you can compare and analyze data from NBA players and teams.

![Python](https://img.shields.io/badge/-Python-181717?&logo=Python&logoColor=FFFFF)
![Flask](https://img.shields.io/badge/-Flask-181717?&logo=Flask&logoColor=FFFFFF)
![Pandas](https://img.shields.io/badge/-Pandas-181717?&logo=Pandas&logoColor=4200A2)
![Streamlit](https://img.shields.io/badge/-Streamlit-181717?&logo=Streamlit&logoColor=FF0000)
![NBA](https://img.shields.io/badge/-NBA-181717?&logo=NBA&logoColor=FFFF)

# Description

Welcome to the NBA-StatisticAPI API documentation! This API is designed to provide quick and easy access to various NBA-related statistics and information. The NBA-StatisticAPI consumes data from the public API available at https://github.com/swar/nba_api, which offers a wide range of up-to-date resources on players, teams, career statistics, draft history and more.

## Installation

To install and run the API, follow the steps below:

1. Clone the repository:
```bash
git clone https://github.com/rychardbarros/NBA-StatisticAPI.git
cd NBA-StatisticAPI
```
2. Create and activate a virtual environment (optional but recommended):
```bash
pip install virtualenv
python -m venv venv

# On Windows
venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate
```
3. Install the dependencies:
```bash
install -r requirements.txt
```
How to Use

## To run the NBA-StatisticAPI, follow the steps below:

Open a terminal or command prompt.
Navigate to the directory where the API is located:
```bash
cd path/to/the/NBA-StatisticAPI/src/api
```
Start the API server by running the routes.py file:
```bash
python routes.py
```
In another terminal or command prompt window, navigate to the root directory of the API:
```bash
cd path/to/the/NBA-StatisticAPI
```
Run the Streamlit app with the following command:
```bash
streamlit run main.py
```
Now, you can explore and interact with the NBA-StatisticAPI to get detailed information about players, teams, career statistics, and more related to the NBA. Have fun exploring the data and creating exciting applications for basketball fans!
Endpoints

The API provides the following endpoints for accessing NBA data:

    /player/{id} (GET Method): Returns the career statistics of a specific player based on the provided player ID.

    /player/name/{id} (GET Method): Returns information about a specific player based on their full name.

    /player/{id}/vs/{vs_id} (GET Method): Compares the statistics of two players based on their IDs.

    /team/all (GET Method): Returns a list of all NBA teams.

    /team/details/{id} (GET Method): Returns details about a specific team based on its ID.

    /draft/all (GET Method): Returns information about all NBA drafts.

    /franchise/all (GET Method): Returns information about all NBA franchises.

    /team/stats/{id} (GET Method): Returns the statistics of a specific team based on its ID.
# Layout
![image](https://github.com/rychardbarros/NBA-StatisticAPI/assets/106812762/b81cc450-b697-4baa-97b3-fa98823dea7c)

---
![image](https://github.com/rychardbarros/NBA-StatisticAPI/assets/106812762/e72b9490-1965-448a-99eb-7c95aa35110c)


# License 📚
[MIT license](LICENSE).

Made by [Rychard Barros](https://github.com/rychardbarros)
