![Python application](https://github.com/doitintl/superPy/workflows/Python%20application/badge.svg?branch=hotfix%2Feben%2FtestActions)

# Python API for superQuery

Python API library for superQuery

# Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* Python >= 3.1

### Installing

```
pip install superQuery
```

# Authentication
* Go to superquery.io and log in/sign up
* In the left side-bar, click on the "Integrations" icon
* Scroll down until you see "Python" and click "Connect"
* Note the username and password
* Set these two environment variables in your local environment:
```
export SUPERQUERY_USERNAME=xxxxxx
export SUPERQUERY_PASSWORD=xxxxxx
```

# The basic flow
* Get your autentication details (See "Authentication" above)
* Import the superQuery library: 

``` 
from superQuery import superQuery
``` 

* Create a superQuery client: 
``` 
client = superQuery.Client()
```

* Set your Google Cloud billing project: 
```
client.project("yourBillingProjectId")
```

* Decide what SQL statement you'd like to run: 
``` 
QUERY = """SELECT name FROM `bigquery-public-data.usa_names.usa_1910_current` LIMIT 10"""
```

* Get your results generator: 
```
result = client.query(QUERY)
```

* Get your results by iteration (**Option A**)
```
for row in result:
    print(row.name)
```

* Get your results by iteration and store to a Pandas dataframe (**Option B**)
```
df = result.to_df()
```

# Running queries with minimum code using Jupyter notebook
* Get your autentication details (See "Authentication" above)
* Import the superQuery library: 

``` 
from superQuery import superQuery
``` 

* Load the `%%superquery` magic  
``` 
%load_ext superQuery
```

* Run your SQL query and display the resulting Pandas dataframe (**Option A**)
``` 
%%superquery --project yourBillingProjectId
SELECT name FROM `bigquery-public-data.usa_names.usa_1910_current` LIMIT 10
```

* Run your SQL query and save the resulting Pandas dataframe to a new variable `df`, which is given as an argument to the `%%superquery` cell magic (**Option B**)
``` 
%%superquery --project yourBillingProjectId --dest df
SELECT name FROM `bigquery-public-data.usa_names.usa_1910_current` LIMIT 10
```

* Run your SQL query and save the resulting Pandas dataframe to a new variable `df` and query execution statistics to `df_stats`. Also provide query input parameters with `$params` (**Option C**)
``` 
params = superQuery.Configuration().configure_parameters({
    'fromYear': '2000', 
    'toYear': '2019'
})
```

```
%%superquery --project yourBillingProjectId --params $params --dest df --stats df_stats
SELECT name FROM `bigquery-public-data.usa_names.usa_1910_current` WHERE year >= CAST(@fromYear AS INT64) LIMIT 10
```


# Examples
## Running `examples/start.ipynb` in Google Colab
* [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/doitintl/superPy/blob/master/examples/start.ipynb)
* Update the credentials in the notebook by following the steps above under "Authentication"
* Run it!

## Running `examples/start.ipynb` in Jupyter notebook
* Launch Jupyter locally with `jupyter notebook`
* Download `examples/start.ipynb` to your local machine and open it from Jupyter
* Update the credentials in the notebook by following the steps above under "Authentication"
* Run it


## Running `examples/start.py`
* First, set these two variables in your local environment:
```
export SUPERQUERY_USERNAME=xxxxxx
export SUPERQUERY_PASSWORD=xxxxxx
```
* Enter your Google Cloud billing project into this line:

```
client.project("yourBillingProjectId")
```

* Alternatively: If you prefer to use your username/password combination directly for each query, then inside  [`start.py`](https://github.com/doitintl/superPy/blob/master/examples/start.py) enter your details obtained from the superquery.io web interface where it shows `xxxxxxx` below

```
query_job = client.query(
    "SELECT field FROM `projectId.datasetId.tableID` WHERE _PARTITIONTIME = \"20xx-xx-xx\"", 
    username="xxxxxxxxx",
    password="xxxxxxxxx")
```

* Now run
```
python3 examples/start_here.py
```
## Running `magic_example.ipynb` in Jupyter notebook
* Launch Jupyter locally with `jupyter notebook`
* Download `magic_example.ipynb` to your local machine and open it from Jupyter
* Update the credentials in the notebook by following the steps above under "Authentication"
* Run it!

## Tested With

* [Python3.7.3](https://www.python.org/downloads/release/python-373/) - Python version

## Authors

* **Eben du Toit** - [ebendutoit](https://github.com/ebendutoit), 
* **Daniël van Niekerk** - *v2.0* 
* **Magdalena Trzeciak** - [mtagda](https://github.com/mtagda) - *v2.1*, 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* The awesome people at superQuery
