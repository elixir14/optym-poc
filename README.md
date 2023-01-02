# Optym POC API

# Running Locally

## Clone API project

    $ git clone git@github.com:elixir14/optym-poc.git


## Copy environment file and fill all requirements

    $ cp .env.template .env


## Run Server
- **Create Virtual environment**

    `$ python3 -m venv /path/to/new/virtual/environment`

  `$ source /path/to/new/virtual/environment/bin/activate`


- **Install dependencies**
    
    `$ pip install -r requirements.txt`


- **Run Migrations**

    `$ alembic upgrade head`


- **Run Server**

    `$ uvicorn --reload optym_poc.main:app --host 0.0.0.0 --port 8007`


- **Test Application**

    `Open swagger URL http://localhost:8007`


- **Running Testcases**

    `$ pytest -v`


## Azure configuration link
    
    https://intility.github.io/fastapi-azure-auth/single-tenant/azure_setup/
