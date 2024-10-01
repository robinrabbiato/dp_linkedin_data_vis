import json
import os
from datetime import datetime
from logger import default_logger as logger


class ScrapingDataManager:
    """
    Manages the scraping data for LinkedIn profiles and posts.

    This class handles loading, saving, and validating scraped profile and post data.
    """

    def __init__(self, profile_output_file, post_output_file):
        """
        Initializes the ScrapingDataManager with specified output files.

        Args:
            profile_output_file (str): Path to the JSON file where scraped profiles will be stored.
            post_output_file (str): Path to the JSON file where scraped posts will be stored.
        """
        self.profile_output_file = profile_output_file
        self.post_output_file = post_output_file
        self.scraped_profiles = self.load_existing_data(self.profile_output_file)
        self.scraped_posts = self.load_existing_data(self.post_output_file)

    def load_existing_data(self, file_path):
        """
        Loads existing scraped data from a JSON file.

        Args:
            file_path (str): Path to the JSON file.

        Returns:
            dict: A dictionary containing previously scraped data or an empty dictionary if none exist.
        """
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                logger.error(
                    f"Error decoding JSON from {file_path}. Starting with empty dataset."
                )
        return {}

    def is_profile_scraped(self, profile_id):
        """
        Checks if a profile has already been scraped.

        Args:
            profile_id (str): The public ID of the LinkedIn profile.

        Returns:
            bool: True if the profile has been scraped, False otherwise.
        """
        return profile_id in self.scraped_profiles

    def save_profile_data(self, profile_id, profile_data):
        """
        Saves a newly scraped profile to the stored data.

        Args:
            profile_id (str): The public ID of the LinkedIn profile.
            profile_data (dict): The data of the scraped profile.
        """
        self.scraped_profiles[profile_id] = {
            "data": profile_data,
            "last_scraped": datetime.now().isoformat(),
        }

    def save_post_data(self, profile_id, posts_data):
        """
        Saves newly scraped posts to the stored data.

        Args:
            profile_id (str): The public ID of the LinkedIn profile.
            posts_data (list): The list of scraped posts.
        """
        self.scraped_posts[profile_id] = posts_data

    def save_data(self):
        """
        Saves all scraped data to the specified JSON files.
        """
        self._save_to_file(self.profile_output_file, self.scraped_profiles, "profiles")
        self._save_to_file(self.post_output_file, self.scraped_posts, "posts")

    def _save_to_file(self, file_path, data, data_type):
        """
        Saves data to a specified JSON file.

        Args:
            file_path (str): Path to the JSON file.
            data (dict): Data to be saved.
            data_type (str): Type of data being saved (for logging purposes).
        """
        if not data:
            logger.warning(f"No {data_type} data to save.")
            return

        logger.info(f"Saving {data_type} data to {file_path}")
        temp_file = f"{file_path}.temp"
        try:
            with open(temp_file, "w") as f:
                json.dump(data, f, indent=2)
                f.flush()
                os.fsync(f.fileno())

            os.replace(temp_file, file_path)
            logger.info(
                f"{data_type.capitalize()} data successfully saved to {file_path}"
            )
        except Exception as e:
            logger.error(f"Failed to save {data_type} data to {file_path}: {str(e)}")
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def get_profile_count(self):
        """
        Returns the number of scraped profiles.

        Returns:
            int: The number of scraped profiles.
        """
        return len(self.scraped_profiles)

    def log_current_state(self):
        """
        Logs the current state of the scraped data.
        """
        logger.info(f"Current number of scraped profiles: {self.get_profile_count()}")
        logger.info(
            f"Current number of profiles with scraped posts: {len(self.scraped_posts)}"
        )
        logger.info(
            f"Profile output file size: {os.path.getsize(self.profile_output_file) if os.path.exists(self.profile_output_file) else 0} bytes"
        )
        logger.info(
            f"Post output file size: {os.path.getsize(self.post_output_file) if os.path.exists(self.post_output_file) else 0} bytes"
        )

    def get_scraped_profile(self, profile_id):
        """
        Retrieves the data of a previously scraped profile.

        Args:
            profile_id (str): The public ID of the LinkedIn profile.

        Returns:
            dict: The scraped profile data or None if not found.
        """
        return self.scraped_profiles.get(profile_id, {}).get("data")

    def get_scraped_posts(self, profile_id):
        """
        Retrieves the posts of a previously scraped profile.

        Args:
            profile_id (str): The public ID of the LinkedIn profile.

        Returns:
            list: The scraped posts or None if not found.
        """
        return self.scraped_posts.get(profile_id)
