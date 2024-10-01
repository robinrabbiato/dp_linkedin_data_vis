import json
import os
import requests
import browser_cookie3
from requests.cookies import RequestsCookieJar
from logger import default_logger as logger


class CookieManager:
    """
    Manages the loading, saving, and validation of cookies for LinkedIn scraping.

    This class handles all cookie-related operations, including file I/O,
    browser cookie extraction, and cookie validation.
    """

    def __init__(self, cookie_file="linkedin_cookies.json"):
        """
        Initializes the CookieManager with a specified cookie file.

        Args:
            cookie_file (str): Path to the JSON file for cookie storage.
        """
        self.cookie_file = cookie_file
        self.cookies = self.load_cookies()
        logger.info(f"CookieManager initialized with file: {cookie_file}")

    def load_cookies(self):
        """
        Loads cookies from the JSON file.

        Returns:
            dict: Loaded cookie data or an empty dictionary if no file exists or an error occurs.
        """
        try:
            if os.path.exists(self.cookie_file):
                with open(self.cookie_file, "r") as f:
                    cookies = json.load(f)
                logger.info(f"Cookies loaded successfully from {self.cookie_file}")
                return cookies
        except json.JSONDecodeError:
            logger.error(
                f"Error decoding JSON from {self.cookie_file}. Using empty cookie set."
            )
        except IOError:
            logger.error(
                f"Error reading file {self.cookie_file}. Using empty cookie set."
            )
        return {}

    def save_cookies(self):
        """
        Saves the current cookies to the JSON file.
        """
        try:
            with open(self.cookie_file, "w") as f:
                json.dump(self.cookies, f, indent=2)
            logger.info(f"Cookies saved successfully to {self.cookie_file}")
        except IOError:
            logger.error(
                f"Error writing to file {self.cookie_file}. Cookies not saved."
            )

    def add_cookie(self, name, value):
        """
        Adds a new cookie or updates an existing one.

        Args:
            name (str): Name of the cookie set.
            value (dict): Cookie data.
        """
        self.cookies[name] = value
        self.save_cookies()
        logger.info(f"Cookie '{name}' added/updated")

    def get_cookie_jar(self, name):
        """
        Creates a RequestsCookieJar object from stored cookie data.

        Args:
            name (str): Name of the cookie set.

        Returns:
            RequestsCookieJar: Cookie jar object or None if not found.
        """
        if name not in self.cookies:
            logger.warning(f"Cookie set '{name}' not found")
            return None
        cookie_data = self.cookies[name]
        jar = RequestsCookieJar()
        for cookie in cookie_data:
            jar.set(
                cookie["name"],
                cookie["value"],
                domain=cookie["domain"],
                path=cookie["path"],
            )
        logger.info(f"Cookie jar created for '{name}'")
        return jar

    def load_from_firefox(self):
        """
        Loads LinkedIn cookies from the Firefox browser and saves them.

        Returns:
            bool: True if cookies were successfully loaded, False otherwise.
        """
        try:
            firefox_cookies = browser_cookie3.firefox(domain_name=".linkedin.com")
            cookie_data = []
            for cookie in firefox_cookies:
                cookie_data.append(
                    {
                        "name": cookie.name,
                        "value": cookie.value,
                        "domain": cookie.domain,
                        "path": cookie.path,
                    }
                )
            self.cookies["firefox"] = cookie_data
            self.save_cookies()
            logger.info("Cookies successfully loaded from Firefox and saved")
            return True
        except Exception as e:
            logger.error(f"Error loading cookies from Firefox: {str(e)}")
            return False

    def validate_linkedin_cookies(self, cookie_set_name):
        """
        Validates the LinkedIn cookies by making a test request.

        Args:
            cookie_set_name (str): Name of the cookie set to validate.

        Returns:
            bool: True if cookies are valid, False otherwise.
        """
        cookie_jar = self.get_cookie_jar(cookie_set_name)
        if not cookie_jar:
            logger.warning(f"No cookie jar found for '{cookie_set_name}'")
            return False

        try:
            response = requests.get(
                "https://www.linkedin.com/feed/",
                cookies=cookie_jar,
                allow_redirects=False,
            )
            logger.info(f"LinkedIn response status code: {response.status_code}")

            if response.status_code == 200:
                logger.info("LinkedIn cookies are valid")
                return True
            elif response.status_code == 302:
                redirect_url = response.headers.get("Location", "")
                if "login" in redirect_url:
                    logger.warning(
                        "LinkedIn cookies are invalid or expired (redirected to login)"
                    )
                else:
                    logger.warning(f"Unexpected redirect: {redirect_url}")
                return False
            else:
                logger.warning(
                    f"Unexpected response from LinkedIn: {response.status_code}"
                )
                return False

        except requests.RequestException as e:
            logger.error(f"Error validating LinkedIn cookies: {str(e)}")
            return False

    def get_valid_cookie_jar(self):
        """
        Returns a valid cookie jar, checking all available cookie sets.

        Returns:
            RequestsCookieJar: A valid cookie jar, or None if no valid cookies found.
        """
        for cookie_set_name in self.list_cookie_keys():
            if self.validate_linkedin_cookies(cookie_set_name):
                return self.get_cookie_jar(cookie_set_name)

        logger.warning("No valid LinkedIn cookies found")
        return None

    def list_cookie_keys(self):
        """
        Lists all keys of the stored cookie sets.

        Returns:
            list: A list of all keys representing different stored cookie sets.
        """
        keys = list(self.cookies.keys())
        logger.info(f"Listing all stored cookie keys: {keys}")
        return keys
