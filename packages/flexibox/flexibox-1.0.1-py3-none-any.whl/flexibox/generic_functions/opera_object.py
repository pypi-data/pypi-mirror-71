# Author: @Corefinder
# Language: Python
# Copyrights: SoumyajitBasu
# Purpose: The purpose of the class ChromeDriverObject is to set the create an instance for the OperaDriverObject class
#          to configure the geckodriver accordingly based on the environment.
# Can be used to set the operadriver object
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from flexibox.core.logger import Logger
from flexibox.core.utility import Utility
from flexibox.utility.os_type import OS_type


class OperaDriverObject(object):
    def __init__(self):
        self.ut = Utility()
        self.ot = OS_type()
        self.log = Logger()

    # Set opera odriver path
    # Pass the option 'headless' if it is needed to run gecko in headless
    # configuration
    def set_operadriver_object(self):
        try:
            os_type = self.ot.os_name()
            driver = None
            if os_type == "macos":
                driver_path = self.ut.get_driver_path('/dependencies/dir_operadriver/operadriver_mac64/operadriver')
                self.ut.set_executable_permission(driver_path)
                self.log.log_info("Setting path of operadriver")
                driver = webdriver.Opera(executable_path=driver_path)
                self.log.log_info("Path for opera binary is set")
            if os_type == "linux":
                driver_path = self.ut.get_driver_path('/dependencies/dir_operadriver/operadriver_linux64/operadriver')
                self.ut.set_executable_permission(driver_path)
                self.log.log_info("Setting path of operadriver")
                driver = webdriver.Opera(executable_path=driver_path)
                self.log.log_info("Path for opera binary is set")
            return driver
        except WebDriverException as e:
            self.log.log_error("There is an exception in the Web Driver configuration")
            self.log.log_error(e)
