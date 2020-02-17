# Poll-Scraper

Poll RealClearPolitics for 2020 Democratic Nomination Poll alerts.



Running RPC_Scraping.py will call the RealClearPolitics API at a given interval and check if there is a new poll. If there is a new poll since the most recent check, the program sends a report of the desired number of most recent polls and the RCP Average information to a specified webhook.



Dependencies:

- pip install realclearpolitics
- pip install requests



To run: Call `python RPC_Scraping.py` in terminal or run it in your Python IDE of choice.

