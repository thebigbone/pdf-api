**To retrieve a list of parsed transactions:**

`GET /transactions`

- This endpoint doesn't require any parameters.

**To search for transactions within a specific date range:**

`GET /transactions/search?start_date=YYYYMMDD&end_date=YYYYMMDD`

- Replace YYYYMMDD with the start and end dates of the range you're interested in. For example, if you want to search for transactions from January 1, 2023, to January 31, 2023, the request would be:

`GET /transactions/search?start_date=20230101&end_date=20230131`

**To get the total balance as of a specific date:**

`GET /balance?date=YYYYMMDD`

- Replace YYYYMMDD with the date you're interested in. For example, if you want to get the balance as of January 31, 2023, the request would be:

`GET /balance?date=20230131`
