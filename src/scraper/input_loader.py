import csv
import re
from logger import default_logger as logger


class InputLoader:
    def __init__(self):
        self.data = []
        self.linkedin_links = []
        self.current_index = 0

    def load_csv(self, file_path):
        """
        Loads data from a CSV file.

        Args:
            file_path (str): The path to the CSV file.

        Returns:
            bool: True if the file was successfully loaded, False otherwise.
        """
        try:
            with open(file_path, mode="r", encoding="utf-8") as csv_file:
                csv_reader = csv.reader(csv_file)
                self.data = list(csv_reader)

            logger.info(f"Successfully loaded {len(self.data)} rows from {file_path}")
            return True
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            return False
        except csv.Error as e:
            logger.error(f"Error reading CSV file {file_path}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error loading {file_path}: {e}")
            return False

    def extract_linkedin_links(self):
        """
        Extracts LinkedIn profile links from the loaded data.

        Returns:
            int: The number of LinkedIn profile links found.
        """
        linkedin_pattern = re.compile(
            r"https?://(?:www\.)?linkedin\.com/(?:in|company)/[\w\-]+/?(?:[\w\-=&?]+)?"
        )
        for row in self.data:
            for cell in row:
                matches = linkedin_pattern.findall(cell)
                self.linkedin_links.extend(matches)

        return len(self.linkedin_links)

    def get_linkedin_links(self):
        """
        Returns the extracted LinkedIn profile links.

        Returns:
            list: The list of LinkedIn profile links.
        """
        return self.linkedin_links

    def __iter__(self):
        """
        Make the class iterable.

        Returns:
            self: The iterator object.
        """
        self.current_index = 0
        return self

    def __next__(self):
        """
        Get the next LinkedIn profile link.

        Returns:
            str: The next LinkedIn profile link.

        Raises:
            StopIteration: When there are no more links to iterate over.
        """
        if self.current_index < len(self.linkedin_links):
            link = self.linkedin_links[self.current_index]
            self.current_index += 1
            return link
        raise StopIteration

    def reset_iterator(self):
        """
        Reset the iterator to the beginning of the list.
        """
        self.current_index = 0
