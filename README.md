# Grocery Scraper

Simple Price comparison component for Serving Fresh

## Steps

Please go through the steps below and command explanation to understand the flow of the Price Comparison component.

All the Markets APIs are store in _jsondata.json file_.

**Run 'python3 main.py' with password to MySQL server for RDS as first argument**

Explanation: Subsequent requests are fired for all the Market APIs and response is stored in _groceries_ table of _pricing DB_.
Program automatically identifies duplicates entry and will only insert if the item is new in the table.

**Run './mysql_login.sh --login' to log into MySQL server for RDS**

Explanation: Use this command to login and create groceries and price_competitive table in pricing DB.

**Run 'python3 price_compare.py' with password to MySQL server for RDS as first argument**

Explanation: Program performs price comparison between the _Serving Fresh item_ and _market item_.
