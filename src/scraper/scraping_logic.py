# scraping_logic.py

from linkedin_api import Linkedin
from logger import default_logger as logger


class ScrapingLogic:
    """
    Handles scraping operations using the unofficial LinkedIn API.

    This class interacts with the LinkedIn API to scrape user and company profiles.
    """

    def __init__(self, cookies, data_manager):
        """
        Initializes the ScrapingLogic with cookies and a data manager for storing results.

        Args:
            cookies (RequestsCookieJar): Validated LinkedIn authentication cookies.
            data_manager (ScrapingDataManager): Instance of ScrapingDataManager for managing scraped data.
        """
        try:
            self.api = Linkedin("", "", cookies=cookies)
            self.data_manager = data_manager
            logger.info("Successfully initialized LinkedIn API with provided cookies")
        except Exception as e:
            logger.error(f"Failed to initialize LinkedIn API: {str(e)}")
            raise

    def scrape_data(self, public_id, profile_type="user", data_type="profile"):
        """
        Scrapes data from a LinkedIn profile (user or company).

        Args:
            public_id (str): The public ID of the LinkedIn profile.
            profile_type (str): The type of profile to scrape ("user" or "company").
            data_type (str): The type of data to scrape ("profile" or "posts").

        Returns:
            dict or list: The scraped data.
        """
        try:
            if profile_type not in ["user", "company"]:
                raise ValueError(f"Invalid profile type: {profile_type}")

            if data_type == "profile":
                if profile_type == "user":
                    data = self.api.get_profile(public_id)
                else:  # profile_type == "company"
                    data = self.api.get_company(public_id)
            elif data_type == "posts":
                if profile_type == "user":
                    data = self.api.get_profile_posts(public_id)
                else:  # profile_type == "company"
                    data = self.api.get_company_updates(public_id)
            else:
                raise ValueError(f"Invalid data type: {data_type}")

            logger.info(
                f"Successfully scraped {data_type} for {profile_type} profile: {public_id}"
            )
            return data
        except Exception as e:
            logger.error(
                f"Error scraping {data_type} for {profile_type} profile {public_id}: {str(e)}"
            )
            return None
