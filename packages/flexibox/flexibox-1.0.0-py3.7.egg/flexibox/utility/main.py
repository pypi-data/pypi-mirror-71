# Author: @Corefinder
# Language: Python
# Copyrights: SoumyajitBasu
# Purpose: The purpose of this class is to parse input argument for carrying out the respective functionality of
#           downloading and updating the required driver
import argparse

from ..driver import Driver

parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(dest='command', help="download")

download = subparser.add_parser("download", help="download driver binary")
update = subparser.add_parser("update", help="update driver binary")
delete = subparser.add_parser("delete", help="delete specific driver binary")

download.add_argument("--driver", help="download the respective driver")
update.add_argument("--driver", help="update the respective driver")
delete.add_argument("--driver", help="delete all drivers")


def main():
    args = parser.parse_args()

    driver_object = Driver.get_driver(args.driver)()
    if args.command == "download":
        driver_object.download_driver()
    if args.command == "update":
        driver_object.update_driver()
    if args.command == "deleteall":
        driver_object.delete_driver_history()


if __name__ == '__main__':
    main()
