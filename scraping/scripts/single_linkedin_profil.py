from apify_client import ApifyClient
from dotenv import load_dotenv
import os
import json
import argparse
import re

# Load the environment variables from the .env file
load_dotenv()

# Initialize the ApifyClient with your API token
client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

# Create the parser and add arguments
parser = argparse.ArgumentParser()
parser.add_argument("url", help="The URL to fetch data from")
parser.add_argument(
    "company_name",
    help="The name of the company, which will be used as the output file name",
)
parser.add_argument(
    "--company",
    action="store_true",
    help="Use 'filters.fromCompanies' if set, otherwise use 'filters.fromMembers'",
)
args = parser.parse_args()


# Function to detox a string
def detox(string):
    string = re.sub(r'[\\/*?:"<>|]', "", string)  # Remove invalid characters
    string = re.sub(r"\s", "_", string)  # Replace spaces with underscores
    string = (
        string.replace("ä", "ae")
        .replace("ö", "oe")
        .replace("ü", "ue")
        .replace("ß", "ss")
    )  # Replace umlauts
    return string


# Try to load the cookies from the cookies.json file
try:
    with open("cookies.json", "r") as f:
        cookies_json = json.load(f)
except FileNotFoundError:
    print(
        "Warning: The cookies.json file was not found. Please make sure it exists in the same directory as your script."
    )
    cookies_json = {}

# Combine cookies_json, "filters.fromCompanies" or "filters.fromMembers", and the company name into run_input
run_input = cookies_json
if args.company:
    run_input["filters.fromCompanies"] = [args.url]
else:
    run_input["filters.fromMembers"] = [args.url]

# Run the Actor and wait for it to finish
run = client.actor("curious_coder~linkedin-post-search-scraper").call(
    run_input=run_input
)

# Fetch Actor results from the run's dataset as JSON
items = client.dataset(run["defaultDatasetId"]).list_items().items

# Detox the company name
detoxed_company_name = detox(args.company_name)

# Determine the subfolder based on the --company flag
subfolder = "company" if args.company else "member"

# Create the subfolder if it doesn't exist
if not os.path.exists(subfolder):
    os.makedirs(subfolder)

# Save the results to a JSON file named after the company, in the subfolder
output_file = os.path.join(subfolder, f"{detoxed_company_name}.json")
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=4)

print(f"The results for '{args.company_name}' have been saved in '{output_file}'.")
