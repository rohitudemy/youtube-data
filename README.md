# Collecting YouTube Video Stats

## Description

Identify the top YouTube video results given a list of search queries.
Output the search results with each video's descriptions and statistics

## System Requirements
Python 2.7

## Libraries
- [Google API Python Library](https://developers.google.com/api-client-library/python/)

## Other Requirements
- YouTube API Key

## Usage Instructions

### API Access (One-time Setup)

Follow these steps to set up your one time token for the YouTube Data API

#### Set up Google Cloud Project

1. Go to [Google Developers API Console](https://code.google.com/apis/console)
2. Create a project
3. In the list of APIs, Select the YouTube Data API
4. Click "Enable"
5. Click "Create credentials"
6. From the drop down menus, select the following:
 - YouTube Data API v3
 - Other non-UI
 - Public data
7. Click "What credentials do I need?"
8. Copy the API key
9. Click Done
10. Open the search.py file in a text editor
11. At the very bottom, replace "YOUR_KEY_HERE" with your key in the default section of this line:
 ```
 argparser.add_argument("--key", help="Developer Key", default="YOUR_KEY_HERE")
 ```
12. Save the search.py file

#### Running the program

1. Create or edit the queries.csv file with a list of keywords
2. Navigate to Terminal, go to the directory where the files are saved and run the following:
```
$ python search.py
```
A file will be created in the directory with the results

#### Additional options

By default, the system is looking for "queries.csv" and caps the maximum results to 25 videos. 
These can be changed with argument flags.  For example, say your filename was "keywords.csv" and you wanted
100 results:

```
$ python search.py --file=keywords.csv --max=100
```