import configparser
from pathlib import Path
from cookie_controller import CookieController
from scraping_controller import ScrapingController
from input_controller import InputController
from logger import default_logger as logger

CONFIG_FILE = "config.ini"
DEFAULT_CSV_PATH = "../../data/input.csv"
DEFAULT_PROFILE_OUTPUT = "../../data/linkedin_profiles.json"
DEFAULT_POST_OUTPUT = "../../data/input.csv"


def main():
    """
    Main function to orchestrate the LinkedIn scraping process.
    """
    logger.info("Starting LinkedIn scraper")

    config = load_config()
    input_controller = setup_input_controller(config)
    cookie_jar = setup_cookie_jar(config)
    scraping_controller = setup_scraping_controller(config, cookie_jar)

    scraping_controller.perform_scraping(input_controller)

    logger.info("LinkedIn scraper finished")


def load_config(config_file=CONFIG_FILE):
    """
    Loads configuration from the specified config file.

    Args:
        config_file (str): Path to the configuration file.

    Returns:
        configparser.ConfigParser: Loaded configuration.
    """
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


def get_absolute_path(relative_path):
    """
    Converts a relative path to an absolute path.

    Args:
        relative_path (str): Relative path to convert.

    Returns:
        str: Absolute path.
    """
    return str(Path(__file__).parent.joinpath(relative_path).resolve())


def setup_input_controller(config):
    csv_filename = config.get("Scraping", "csvFileName", fallback=DEFAULT_CSV_PATH)
    csv_path = get_absolute_path(csv_filename)

    input_controller = InputController()
    input_controller.set_csv_path(csv_path)

    if input_controller.process_input_file() <= 0:
        raise RuntimeError("Failed to process input file or no profiles found.")

    return input_controller


def setup_cookie_jar(config):
    iterate_accounts = config.getboolean(
        "Scraping", "iterateAccountsWhileScraping", fallback=False
    )

    cookie_controller = CookieController()
    cookie_jar = cookie_controller.handleCookies(iterate_accounts)

    if not cookie_jar:
        raise RuntimeError(
            "Failed to initialize any cookie jar. Scraping cannot proceed."
        )

    logger.info("Cookie jar successfully initialized.")
    return cookie_jar


def setup_scraping_controller(config, cookie_jar):
    profile_output = config.get(
        "Scraping", "profile_output", fallback=DEFAULT_PROFILE_OUTPUT
    )
    post_output_path = config.get(
        "Scraping", "post_output", fallback=DEFAULT_POST_OUTPUT
    )

    profile_output_path = get_absolute_path(profile_output)
    min_delay = config.getfloat("Scraping", "min_delay")
    max_delay = config.getfloat("Scraping", "max_delay")
    return ScrapingController(
        cookie_jar, profile_output_path, post_output_path, min_delay, max_delay
    )


if __name__ == "__main__":
    main()
