# Movie Trends Analyzer

**Authors** : Victoria Le,  Nick Nguyen

### Project Description

This project will save information from a popular movie rating sites (RottenTomatoes and IMDB) to figure out a trend in popular movies. The top 50 movies released in a given year (filtering only those that had 50000+ votes) of the year will be saved to a database, where users can graphically compare aspects of a movie to it's popularity. These aspects contain data such as the genre, score and rating of each movie. A bar chart will be used to look at a single year. If multiple years are being compared, then a line graph will be shown.

## Project Plans

### Outline

#### Main

- [x] Design a data file (what are the headers)
- [x] Properly save web data from IMDb into the file
- [x] Design a simple homepage
    - [x] Header with project title and github link
    - [x] Description of the website
    - [x] Button to move on to the analyzing page
    - [x] Button to move on to the data page
- [x] Design an analytics page
    - [x] Add a button to update/reset data
    - [x] Slot for an image
- [x] Display graphs for the data
    - [x] Allow users to change what aspect is being graphed
- [x] Design a data page
    - [x] Add a button to retrieve/save/delete data


#### Extra
- [ ] Recommendation system based on highest rating (bonuses if a movie shows up in multiple year)
- [ ] Allow users to save a graph in some format, to compare it with other graphs
- [ ] A download button to get a csv containing ONLY the data shown in the graph
- [ ] A method to estimate the popularity of a movie based on inputted aspects
- [ ] Show the two most popular movie of the latest year (if any data) on the home page
    - [ ] Save/Display the image for each movie as well
- [ ] Filter the data on more aspects
- [ ] Add more graphs (ie. budget)

### Interface

The program will have a homepage with a brief description, instructions, and a button to navigate to the analytics and data page.

The analytics page contains a simple tabbar for users to choose the type of graph they would like to generate and a side bar with a filtering system for selecting a time range. This page will also have a button to update or reset the graph if the user chooses to make any changes to their selection. On the side bar will also be a list of 100 movies that were made within the given time range, filtered according to the settings below it.

Clicking the button on the analytics page will display a graph based on the chosen tab (ie. Genre, Score, Rating). When swapping years, the movie list must be reupdated, before the correct graph is shown.

The data page contains a list of all the movie files found in the data directory (where this program would normally save data). A textbox is given for users to input years (numbers only), where it will attempt to grab the relevant data from IMDB. Files can be checked and deleted as needed.

### Data Collection/Storage

We will collect data from [IMDb](https://www.imdb.com/).

As many of the official APIs for the website are not available for public use or require subscriptions, we will make use of the Beautiful Soup Python package for web scraping and acquiring movie information.

Data will be collected and stored as a numpy saved pickle file, denoting the movie title, year, rating, and the rest of it's aspects. When saving data, it will only save based on the user inputs. None of the files are persistent, or checked for corruption. Incase they're broken, simply use the data page and redownload the files.

### Data Analysis and Visualization

We will gather a list of the top fifty movies from each given year and place them all into a list. From there, we generate a bar/line plot using matplotlib, graphing the chosen data aginst the selected time range. The current options to graph are by genres, user score and rating.
