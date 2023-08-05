# Basic SQL

This is a small package intended to help with basic operations such as select, insert, update, and upsert as well as executing raw SQL queries for different database types.

## Additional requirements

The package is using SQLAlchemy and depending on what database you want to connect to the installation of additional packages is required. Below are the instructions for the databases that are currently supported:

### PostgreSQL
```
pip install psycopg2
```

### MySQL
```
pip install pymysql
```

### SQL Server (MSSQL)
```
pip install pyodbc
```
On Linux first follow the [Microsoft instructions](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15) to install the required drivers.

### Oracle
```
pip install cx_Oracle
```
On Linux first follow the [Oracle instructions](https://www.oracle.com/au/database/technologies/instant-client/linux-x86-64-downloads.html#ic_x64_inst) to install the required drivers.