from input_loader import InputLoader
from logger import default_logger as logger


class InputController:
    def __init__(self):
        self.loader = InputLoader()
        self.csv_path = None

    def set_csv_path(self, path):
        """
        Sets the path for the CSV file.

        Args:
            path (str): The path to the CSV file.
        """
        self.csv_path = path
        logger.info(f"CSV path set to: {self.csv_path}")

    def process_input_file(self):
        """
        Processes the input CSV file to extract LinkedIn profile links.

        Returns:
            int: The number of LinkedIn profile links found, or -1 if an error occurred.
        """
        if not self.csv_path:
            logger.error("CSV path not set. Use set_csv_path() before processing.")
            return -1

        if not self.loader.load_csv(self.csv_path):
            logger.error("Failed to load CSV file.")
            return -1

        num_links = self.loader.extract_linkedin_links()
        logger.info(f"Found {num_links} LinkedIn profile links.")
        return num_links

    def get_linkedin_links(self):
        """
        Returns the extracted LinkedIn profile links.

        Returns:
            list: The list of LinkedIn profile links.
        """
        return self.loader.get_linkedin_links()

    def get_next_profile(self):
        """
        Get the next LinkedIn profile link.

        Returns:
            str: The next LinkedIn profile link, or None if there are no more links.
        """
        try:
            return next(self.loader)
        except StopIteration:
            return None

    def reset_profile_iterator(self):
        """
        Reset the profile iterator to the beginning.
        """
        self.loader.reset_iterator()
