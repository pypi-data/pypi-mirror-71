# Author: @Corefinder
# Language: Python
# Copyrights: SoumyajitBasu
# Purpose: PhantomJS driver initialization
# can be used across all the functionalities that would be developed in this project
import os

from flexibox.core.logger import Logger
from flexibox.core.utility import Utility
from flexibox.utility.os_type import OS_type


class Phantomjs_driver():
    def __init__(self):
        self.ut = Utility()
        self.ot = OS_type()
        self.log = Logger()

    # Get the required phsntomjs driver informations from the downloader_config.ini
    # Use the config_reader function from the Utility class to read the required configuration

    def phantomjsdriver_object(self):
        config_parser = self.ut.config_reader()
        api_url = config_parser.get('PhantomJSDriver', 'latest_browser_driver')
        return api_url

    # Get the required API data from the function phantomjsdriver_object

    def parse_phantomjsdriver_api(self):
        api_url = self.phantomjsdriver_object()
        api_data = self.ut.api_parser(api_url)
        return api_data

    # Get the required download url based on the information gathered using the
    # geckodriver_objects function

    def parse_apidata(self):
        api_url = {}
        raw_json = self.parse_phantomjsdriver_api()
        api_url = {"zip_ball": raw_json['zipball_url'], "tar_ball": raw_json['tarball_url']}
        return api_url

    # Download the required phantomjsdriver binary based on the operating system type

    def evaluate_on_environment(self, os_name):
        download_url = self.parse_apidata()
        dir_path = self.ut.get_driver_path('/dependencies/dir_phantomjsdriver')
        if os_name == 'macos':
            self.log.log_info("Environment: " + os_name)
            self.log.log_info("Downloading the required binary for phantomjsdriver")
            self.ut.driver_downloader(download_url['zip_ball'], dir_path)
            self.log.log_info("Download completed")
            self.ut.unzip_file('dir_phantomjsdriver/')
            self.log.log_info("Unarchiving contents completed")
            self.ut.rename_dir('dir_phantomjsdriver/')
        if os_name == 'linux':
            self.log_message("INFO", "Environment: " + os_name)
            self.log_message("INFO", "Downloading the required binary for phantomjsdriver")
            self.ut.driver_downloader(download_url['tar_ball'], dir_path)
            self.log_message("INFO", "Download completed")
            self.ut.untar_file('dir_phantomjsdriver/')
            self.log_message("INFO", "Unarchiving contents completed")
            self.ut.rename_dir('dir_phantomjsdriver/')

    # Create a required directory separately for phantomjs and called the evaluate_on_environment
    # function to download the required binary

    def download_driver(self):
        dir_path = self.ut.get_driver_path('/dependencies/dir_phantomjsdriver')
        if os.path.exists(dir_path):
            self.log.log_info(
                "phantomjs driver is already present. To update phantomjsdriver please run `flexibox update --driver=phantomjsdriver`"
            )
        else:
            os.makedirs(dir_path)
            os_name = self.ot.os_name()
            self.evaluate_on_environment(os_name)

    # Update the required phantomjsdriver based on the operating system type

    def update_driver(self):
        self.log.log_info("Deleting directory contents")
        self.ut.check_directory_content('/dependencies/dir_phantomjsdriver')
        self.ut.delete_dir_contents('dir_phantomjsdriver/')
        os_name = self.ot.os_name()
        self.evaluate_on_environment(os_name)
        self.log.log_info("phantomjs driver updated")
