# RS-project
A user's reviews based recommender system, developed for my university degree thesis

## Checking if the virtual enviornment is installed
Firstly you need to check you've installed virtualenv in your computer. If you're using Linux, just type in the shell:

`apt search virtualenv`

If it's not installed, you can install it by typing:

`sudo install virtualenv`

## Fetching the reviews
### Activating the virtual environment
Move into the folder where you cloned the repo and activate the virtual environment, move in the scraping directory, by typing these:

`source ./venv/bin/activate`

`cd scraping`

### Running the script
If you want to simply display the reviews in the shell output, run this:

`scrapy crawl fetcher`

Otherwise, to store the reviews in a json file rather than showing them in the shell, run this command instead:

`scrapy crawl fetcher -o reviews.json`