from cookie_manager import CookieManager
from logger import default_logger as logger
import itertools


class CookieController:
    """
    Controls the management of cookies for LinkedIn scraping.

    This class handles the loading, validation, and iteration of cookies,
    interfacing with the CookieManager for actual cookie operations.
    """

    def __init__(self):
        """
        Initializes the CookieController with a CookieManager instance.
        """
        self.cookie_manager = CookieManager()
        self.cookie_iterator = None

    def handleCookies(self, iterate_accounts):
        """
        Handles the entire cookie management process and returns the next valid cookie jar.

        Args:
            iterate_accounts (bool): Whether to iterate through multiple account cookies.

        Returns:
            RequestsCookieJar: A valid cookie jar, or None if no valid cookies are available.
        """
        self.load_cookies()

        if self.get_cookie_count() == 0:
            if self.prompt_load_cookies() and self.get_cookie_count() > 0:
                logger.info("Cookies successfully imported from Firefox.")
            else:
                logger.warning("No cookies available. Scraping may not work correctly.")
                return None

        valid_cookie_jar = self.cookie_manager.get_valid_cookie_jar()
        if not valid_cookie_jar:
            logger.warning("No valid cookies found. Scraping may not work correctly.")
            return None

        if iterate_accounts and self.get_cookie_count() > 1:
            self.setup_cookie_iterator()
            return self.get_next_valid_cookie_jar()
        else:
            return valid_cookie_jar

    def load_cookies(self):
        """
        Loads cookies from the cookie file using the CookieManager.

        Returns:
            dict: The loaded cookies.
        """
        return self.cookie_manager.load_cookies()

    def get_cookie_count(self):
        """
        Returns the number of cookie sets available.

        Returns:
            int: The number of cookie sets.
        """
        return len(self.cookie_manager.list_cookie_keys())

    def prompt_load_cookies(self):
        """
        Prompts the user to load cookies from Firefox and imports them if agreed.

        Returns:
            bool: True if cookies were successfully imported, False otherwise.
        """
        load_from_firefox = (
            input("Do you want to load cookies from Firefox? (y/n): ").lower() == "y"
        )
        if load_from_firefox:
            return self.cookie_manager.load_from_firefox()
        return False

    def setup_cookie_iterator(self):
        """
        Sets up an iterator to cycle through available cookie sets.
        """
        available_cookies = self.cookie_manager.list_cookie_keys()
        self.cookie_iterator = itertools.cycle(available_cookies)

    def get_next_valid_cookie_jar(self):
        """
        Returns the next valid cookie jar from the iterator.

        Returns:
            RequestsCookieJar: The next valid cookie jar, or None if no valid cookies are found.
        """
        if self.cookie_iterator is None:
            logger.warning(
                "Cookie iterator not set up. Call setup_cookie_iterator() first."
            )
            return None

        for _ in range(
            self.get_cookie_count()
        ):  # Limit iterations to avoid infinite loop
            next_cookie_set = next(self.cookie_iterator)
            if self.cookie_manager.validate_linkedin_cookies(next_cookie_set):
                return self.cookie_manager.get_cookie_jar(next_cookie_set)

        logger.warning("No valid cookies found in the rotation.")
        return None
