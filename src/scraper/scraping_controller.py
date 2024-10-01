import random
import time
import re
from typing import Optional, Tuple
from scraping_logic import ScrapingLogic
from scraping_data_manager import ScrapingDataManager
from logger import default_logger as logger

LINKEDIN_URL_PATTERN = (
    r"(?:https?:)?(?:\/\/)?(?:[\w]+\.)?linkedin\.com\/(?:in|company)\/([^\/\?\s]+)"
)


class ScrapingController:
    """
    Controller class for managing the scraping process.
    """

    def __init__(
        self, cookies, profile_output_file, post_output_file, min_delay, max_delay
    ):
        """
        Initialize the scraping controller with necessary parameters.

        :param cookies: Cookies to be used for scraping.
        :param profile_output_file: File path to save scraped profile data.
        :param post_output_file: File path to save scraped post data.
        :param min_delay: Minimum delay between profile scrapes.
        :param max_delay: Maximum delay between profile scrapes.
        """
        self.data_manager = ScrapingDataManager(profile_output_file, post_output_file)
        self.scraping_logic = ScrapingLogic(cookies, self.data_manager)
        self.min_delay = min_delay
        self.max_delay = max_delay

    def scrape_profile(
        self, link: str
    ) -> Tuple[Optional[dict], Optional[dict], Optional[str]]:
        """
        Scrape a LinkedIn profile and its posts.

        :param link: LinkedIn profile URL.
        :return: Tuple containing profile data, posts data, and public_id.
        """
        public_id = self._extract_public_id(link)
        if not public_id:
            logger.error(f"Invalid LinkedIn URL: {link}")
            return None, None, None

        if self.data_manager.is_profile_scraped(public_id):
            logger.info(f"Profile {public_id} has already been scraped. Skipping.")
            return None, None, public_id

        profile_type = "company" if "/company/" in link else "user"

        profile_data = self.scraping_logic.scrape_data(
            public_id, profile_type, "profile"
        )

        if profile_data:
            posts = self.scraping_logic.scrape_data(public_id, profile_type, "posts")
            logger.info(f"Profile {public_id} and its posts scraped.")
            return profile_data, posts, public_id
        else:
            logger.error(f"Failed to scrape profile {public_id}")
            return None, None, public_id

    def _extract_public_id(self, link: str) -> Optional[str]:
        """
        Extract the public ID from a LinkedIn URL.

        :param link: LinkedIn URL.
        :return: Public ID if found, None otherwise.
        """
        match = re.search(LINKEDIN_URL_PATTERN, link)
        if match:
            return match.group(1)
        else:
            logger.error(f"Could not extract public ID from URL: {link}")
            return None

    def save_scraped_data(self):
        """
        Save the scraped data to the output files.
        """
        print("CALLING SAVE DATA from scraping controller")
        self.data_manager.save_data()

    def get_scraped_profile_count(self) -> int:
        """
        Get the count of scraped profiles.

        :return: Count of scraped profiles.
        """
        return self.data_manager.get_profile_count()

    def log_scraping_stats(self):
        """
        Log the statistics of the scraping process.
        """
        logger.info(f"Total scraped profiles: {self.get_scraped_profile_count()}")
        self.data_manager.log_current_state()

    def perform_scraping(self, input_controller):
        """
        Perform the scraping process.

        :param input_controller: Input controller providing the profile links.
        """
        total_profiles = 0
        skipped_profiles = 0
        scraped_profiles = 0
        total_number_of_profiles = len(input_controller.get_linkedin_links())

        for profile_link in iter(input_controller.get_next_profile, None):
            delay = random.uniform(self.min_delay, self.max_delay)
            total_profiles += 1
            logger.info(f"Processing profile {total_profiles}: {profile_link}")

            profile_data, posts, public_id = self.scrape_profile(profile_link)

            if profile_data is None:
                if public_id and self.data_manager.is_profile_scraped(public_id):
                    skipped_profiles += 1
                    logger.info(f"Skipped already scraped profile: {profile_link}")
                    delay = 0  # no delay for skipped profiles
                else:
                    logger.error(f"Failed to scrape profile: {profile_link}")
                    logger.info("To prevent blocking, the scraping process will stop.")
                    break
            else:
                scraped_profiles += 1
                logger.info(f"Successfully scraped profile: {profile_link}")

                # Save the scraped data
                self.data_manager.save_profile_data(public_id, profile_data)
                self.data_manager.save_post_data(public_id, posts)
                self.data_manager.save_data()

            percentage_processed = round(
                (total_profiles / total_number_of_profiles) * 100, 2
            )
            logger.info(
                f"Profile {public_id} and its posts processed. \n\t{percentage_processed}% of total profiles processed.\n"
            )

            time.sleep(delay)  # delay between scrapes

        logger.info("Scraping process completed.")
        logger.info(f"Total profiles processed: {total_profiles}")
        logger.info(f"Profiles scraped: {scraped_profiles}")
        logger.info(f"Profiles skipped: {skipped_profiles}")

        # Save all scraped data at the end of the process
        self.save_scraped_data()
