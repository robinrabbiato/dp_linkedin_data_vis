from apify_client import ApifyClient
import json
import os
import re
import logging


def process_data(url, company_name, use_company, api_token, cookie_file):
    """
    Process LinkedIn data for a given URL using Apify.

    Args:
        url (str): The LinkedIn URL to process.
        company_name (str): The name of the company or member.
        use_company (bool): Whether to use company or member filters.
        api_token (str): The Apify API token.
        cookie_file (str): Path to the file containing LinkedIn cookies.

    Returns:
        None
    """
    client = ApifyClient(api_token)

    def detox(string):
        """
        Sanitize a string for use as a filename.

        Args:
            string (str): The input string to sanitize.

        Returns:
            str: The sanitized string.
        """
        string = re.sub(r'[\\/*?:"<>|]', "", string)
        string = re.sub(r"\s", "_", string)
        string = (
            string.replace("ä", "ae")
            .replace("ö", "oe")
            .replace("ü", "ue")
            .replace("ß", "ss")
        )
        return string

    try:
        with open(cookie_file, "r") as f:
            cookies_json = json.load(f)
        logging.info(f"Cookies loaded successfully from {cookie_file}")
    except FileNotFoundError:
        logging.warning(
            f"Cookie file {cookie_file} not found. Proceeding without cookies."
        )
        cookies_json = {}

    run_input = cookies_json
    if use_company:
        run_input["filters.fromCompanies"] = [url]
    else:
        run_input["filters.fromMembers"] = [url]

    logging.info(f"Running Actor for {company_name}")
    run = client.actor("curious_coder~linkedin-post-search-scraper").call(
        run_input=run_input
    )

    items = client.dataset(run["defaultDatasetId"]).list_items().items
    logging.info(f"Retrieved {len(items)} items for {company_name}")

    detoxed_company_name = detox(company_name)
    subfolder = "company" if use_company else "member"

    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
        logging.info(f"Created subfolder: {subfolder}")

    output_file = os.path.join(subfolder, f"{detoxed_company_name}.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=4)

    logging.info(f"Results for '{company_name}' saved in '{output_file}'")
