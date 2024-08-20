# Scrapy Hotel Data Extraction Project

This project uses Scrapy to extract hotel data from Trip.com and store it in a PostgreSQL database. It includes image downloading functionality and handles duplicate entries.

## Repository

The project is hosted on GitHub:

[https://github.com/Oyshik-ICT/Assignment_Scrapy_Modified.git](https://github.com/Oyshik-ICT/Assignment_Scrapy_Modified.git)

## Prerequisites

- Python 3.7+
- PostgreSQL

## Setup

1. Clone the repository:

   ```
   git clone https://github.com/Oyshik-ICT/Assignment_Scrapy_Modified.git
   cd Assignment_Scrapy_Modified
   ```

2. Create a virtual environment and activate it:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

4. Set up the PostgreSQL database:
   - Create a new database for the project
   - Create a `.env` file in the project root directory and add your database credentials:
     ```
     DATABASE_URL=postgresql+psycopg2://<username>:<password>@<host>:<port>/<database>
     ```
   - Example:
     ```
     DATABASE_URL=postgresql+psycopg2://postgres:p%40stgress@localhost:5433/postgres
     ```

## Running the Spider

To run the spider, use the following command:

```
scrapy crawl website_source
```

This will start the spider, which will:

1. Scrape hotel data from Trip.com
2. Download hotel images to the `hotel_images` directory
3. Store the data in the PostgreSQL database

## Project Structure

- `myspider.py`: Contains the main spider logic for scraping Trip.com
- `items.py`: Defines the structure of the scraped data
- `pipelines.py`: Handles data processing and storage in the database
- `.env`: Contains environment variables (this file is in .gitignore)
- `requirements.txt`: Lists all Python dependencies

## Customization

- To modify the number of categories scraped, adjust the `random.sample()` call in the `parse` method of `WebsiteSourceSpider`.
- To change the fields being extracted, update the `HotelItem` in `items.py` and adjust the `extract_data` method in `myspider.py`.

## Notes

- The spider is designed to handle duplicate entries based on the `hotelId`.
- Images are saved locally, and the database stores the file path instead of the URL.
- Make sure you have the necessary permissions to write to the `hotel_images` directory.

## Troubleshooting

- If you encounter database connection issues, double-check your `.env` file and ensure your PostgreSQL server is running.
- For image download problems, verify that you have write permissions in the project directory.
