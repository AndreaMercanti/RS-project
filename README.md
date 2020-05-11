# RS-project
A user's reviews based recommender system, developed for my university degree thesis

## Checking if the virtual enviornment is installed
Firstly you need to check you've installed virtualenv in your computer. If you're using Linux, just type in the shell:

`apt search virtualenv`

If it's not installed, you can install it by typing:

`sudo apt install virtualenv`

## Fetching the reviews
### Activating the virtual environment
Move into the folder where you cloned the repo and activate the virtual environment, move in the scraping directory, by typing these:

`source ./venv/bin/activate`

`cd scraping`

### Running the script
Execute this command to run the entire project:

`scrapy crawl fetcher`