import pandas as pd
import json
import logging
import re
import requests
from pathlib import Path
from data_processor import process_data
import time
import random

# Setup logging configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def load_config():
    """
    Load the configuration from config.json file.

    Returns:
        dict: A dictionary containing the configuration settings.

    Raises:
        SystemExit: If the configuration file is not found.
    """
    try:
        with open("config.json", "r") as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        logging.error("Configuration file 'config.json' not found.")
        exit(1)


def is_valid_linkedin_url(url):
    """
    Check if the given string is a valid LinkedIn URL.

    Args:
        url: The URL to check. Can be a string or any other type.

    Returns:
        bool: True if the string is a valid LinkedIn URL, False otherwise.
    """
    if not isinstance(url, str):
        return False
    regex = re.compile(
        r"^(https?://)?(www\.)?linkedin\.com/(in|company)/.+$", re.IGNORECASE
    )
    return regex.match(url) is not None


def is_reachable(url):
    """
    Check if the given URL is reachable.

    Args:
        url (str): The URL to check.

    Returns:
        bool: True if the URL is reachable, False otherwise.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        return response.status_code == 200
    except requests.RequestException:
        return False


def process_csv(file_path, config):
    """
    Process the CSV file containing LinkedIn URLs and company names.

    Args:
        file_path (str): Path to the CSV file.
        config (dict): Configuration dictionary containing column names and other settings.

    Returns:
        None
    """
    try:
        df = pd.read_csv(file_path, sep=";")
        logging.info(f"Successfully loaded CSV file: {file_path}")
    except FileNotFoundError:
        logging.error(f"CSV file not found: {file_path}")
        return

    url_column = config["url_column"]
    company_name_column = config["company_name_column"]

    if url_column not in df.columns or company_name_column not in df.columns:
        logging.error(
            f"Required columns '{url_column}' or '{company_name_column}' not found in CSV."
        )
        return

    total_entries = len(df)
    processed_entries = 0
    skipped_entries = 0
    unreachable_entries = 0
    logging.info(f"Total entries to process: {total_entries}")

    for index, row in df.iterrows():
        url = row[url_column]
        company_name = row[company_name_column]

        if pd.isna(url) or pd.isna(company_name):
            logging.warning(
                f"Missing URL or company name for entry {index + 1}. Skipping this entry."
            )
            skipped_entries += 1
            continue

        if not is_valid_linkedin_url(url):
            logging.warning(
                f"Invalid LinkedIn URL for entry {index + 1}: {url}. Skipping this entry."
            )
            skipped_entries += 1
            continue

        # Uncomment the following block if you want to check URL reachability
        # if not is_reachable(url):
        #     logging.warning(f"Unreachable LinkedIn URL for entry {index + 1}: {url}. Skipping this entry.")
        #     unreachable_entries += 1
        #     continue

        use_company = "linkedin.com/company/" in url

        logging.info(f"Processing entry {index + 1} of {total_entries}: {company_name}")
        process_data(
            url,
            company_name,
            use_company,
            config["APIFY_API_TOKEN"],
            config["cookie_file"],
        )

        processed_entries += 1
        # Print progress
        print(
            f"Progress: {processed_entries}/{total_entries} entries processed, {skipped_entries} skipped, {unreachable_entries} unreachable",
            end="\r",
        )

        # Add a random delay between requests
        time.sleep(random.uniform(1, 3))

    print()  # New line after progress display
    logging.info(
        f"Processing completed. {processed_entries} entries processed, {skipped_entries} skipped, {unreachable_entries} unreachable."
    )


def main():
    """
    Main function to run the LinkedIn data processing script.

    This function loads the configuration, processes the CSV file,
    and coordinates the overall execution of the script.

    Returns:
        None
    """
    logging.info("Starting LinkedIn data processing program")

    config = load_config()
    logging.info("Configuration loaded successfully")

    # Convert relative paths to absolute paths
    script_dir = Path(__file__).parent
    config["csv_file"] = str(script_dir / config["csv_file"])
    config["cookie_file"] = str(script_dir / config["cookie_file"])

    process_csv(config["csv_file"], config)

    logging.info("Program execution completed")


if __name__ == "__main__":
    main()
