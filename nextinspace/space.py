"""The classes for storing and displaying data from the LL2 API"""

from colorama import init, Fore, Back, Style
from datetime import datetime
import textwrap as t
from enum import Enum


# Values for display
MAX_LINE_LENGTH = 88
CHART_WIDTH = 59
DATE_FMAT_STR = "%a %B %d, %Y %I:%M %p %Z"


class Verbosity(Enum):
    """The verbosity of the display to terminal"""

    QUIET = 1
    NORMAL = 2
    VERBOSE = 3


class Event:
    """Generic space event"""

    def __init__(self, mission_name, location, mission_date, mission_description, mission_type):
        self.mission_name = mission_name
        self.location = location
        self.mission_date = mission_date
        self.mission_description = mission_description
        self.mission_type = mission_type

    def display(self, verbosity=Verbosity.NORMAL):
        """Display self to terminal with box sides, indents, and colors

        Args:
            verbosity (Verbosity, optional): The verbosity displayed. Defaults to Verbosity.NORMAL.
        """

        # Mission name
        mission_name_lines = t.wrap(self.mission_name, width=MAX_LINE_LENGTH)
        for line in mission_name_lines:
            print("│" + Style.BRIGHT + Fore.CYAN + line.ljust(MAX_LINE_LENGTH, " ") + Style.RESET_ALL + "│")

        # Location
        print("│" + Fore.CYAN + self.location.ljust(MAX_LINE_LENGTH, " ") + Fore.RESET + "│")

        # Filler line
        FILLER = "│" + " " * MAX_LINE_LENGTH + "│"
        print(FILLER)

        # Date
        print(
            "│"
            + Fore.GREEN
            + ("    " + self.mission_date.strftime(DATE_FMAT_STR)).ljust(MAX_LINE_LENGTH, " ")
            + Fore.RESET
            + "│"
        )

        # Mission type
        print("│" + ("    Event Type: " + self.mission_type).ljust(MAX_LINE_LENGTH, " ") + "│")

        # If verbosity is not set to quiet, print mission description
        if verbosity != verbosity.QUIET:
            print(FILLER)

            mission_description_lines = t.wrap(
                self.mission_description, width=MAX_LINE_LENGTH, initial_indent="    ", subsequent_indent="    "
            )
            for line in mission_description_lines:
                print("│" + line.ljust(MAX_LINE_LENGTH, " ") + "│")


class Launch(Event):
    """Launch event"""

    def __init__(self, mission_name, location, mission_date, mission_description, mission_type, rocket):
        super().__init__(mission_name, location, mission_date, mission_description, mission_type)
        self.rocket = rocket

    def display(self, verbosity=Verbosity.NORMAL):
        """Display self to terminal with box sides, indents, and colors

        Args:
            verbosity (Verbosity, optional): The verbosity displayed. Defaults to Verbosity.NORMAL.
        """

        # Mission name
        mission_name_lines = t.wrap(self.mission_name, width=MAX_LINE_LENGTH)
        for line in mission_name_lines:
            print("│" + Style.BRIGHT + Fore.CYAN + line.ljust(MAX_LINE_LENGTH, " ") + Style.RESET_ALL + "│")

        # Location
        print("│" + Fore.CYAN + self.location.ljust(MAX_LINE_LENGTH, " ") + Fore.RESET + "│")

        # Filler line
        FILLER = "│" + " " * MAX_LINE_LENGTH + "│"
        print(FILLER)

        # Date
        print(
            "│"
            + Fore.GREEN
            + ("    " + self.mission_date.strftime(DATE_FMAT_STR)).ljust(MAX_LINE_LENGTH, " ")
            + Fore.RESET
            + "│"
        )

        # Mission type
        print("│" + ("    Launch Type: " + self.mission_type).ljust(MAX_LINE_LENGTH, " ") + "│")

        # If verbosity is not set to quiet, print mission description
        if verbosity != Verbosity.QUIET:
            # If verbosity is set to verbose, print rocket information
            if verbosity == Verbosity.VERBOSE:
                print(FILLER)
                self.rocket.display()

            print(FILLER)
            mission_description_lines = t.wrap(
                self.mission_description, width=MAX_LINE_LENGTH, initial_indent="    ", subsequent_indent="    "
            )
            for line in mission_description_lines:
                print("│" + line.ljust(MAX_LINE_LENGTH, " ") + "│")


class Rocket:
    def __init__(
        self,
        name,
        payload_leo,
        payload_gto,
        liftoff_thrust,
        liftoff_mass,
        max_stages,
        height,
        successful_launches,
        consecutive_successful_launches,
        failed_launches,
        maiden_flight_date,
    ):

        self.name = name
        self.payload_leo = payload_leo
        self.payload_gto = payload_gto
        self.liftoff_thrust = liftoff_thrust
        self.liftoff_mass = liftoff_mass
        self.max_stages = max_stages
        self.height = height
        self.successful_launches = successful_launches
        self.consecutive_successful_launches = consecutive_successful_launches
        self.failed_launches = failed_launches
        self.maiden_flight_date = maiden_flight_date

    def display(self):
        """Display self to terminal. Only for use with the Launch display() method"""

        INTER_CELL_DIVIDER = "│" + ("├" + "─" * CHART_WIDTH + "┤").center(MAX_LINE_LENGTH, " ") + "│"

        print("│" + ("┌" + "─" * CHART_WIDTH + "┐").center(MAX_LINE_LENGTH, " ") + "│")
        print("│" + ("│" + self.name.center(CHART_WIDTH) + "│").center(MAX_LINE_LENGTH, " ") + "│")
        print(INTER_CELL_DIVIDER)
        print(self._generate_chart_line("Height: " + str(self.height) + " m", "Mass to LEO: " + str(self.payload_leo) + " kg"))
        print(INTER_CELL_DIVIDER)
        print(
            self._generate_chart_line(
                "Max Stages " + str(self.max_stages), "Liftoff Thrust: " + str(self.liftoff_thrust) + " kN"
            )
        )
        print(INTER_CELL_DIVIDER)
        print(
            self._generate_chart_line(
                "Mass to GTO: " + str(self.payload_gto) + " kg", "Liftoff Mass: " + str(self.liftoff_mass) + " Tonnes"
            )
        )
        print(INTER_CELL_DIVIDER)
        print(
            self._generate_chart_line(
                "Launch Successes: " + str(self.successful_launches),
                "Maiden Flight: " + self.maiden_flight_date.strftime("%Y-%m-%d"),
            )
        )
        print(INTER_CELL_DIVIDER)
        print(
            self._generate_chart_line(
                "Consecutive Successes: " + str(self.consecutive_successful_launches),
                "Failed Launches: " + str(self.failed_launches),
            )
        )
        print("│" + ("└" + "─" * CHART_WIDTH + "┘").center(MAX_LINE_LENGTH, " ") + "│")

    @staticmethod
    def _generate_chart_line(left, right):
        row = (left).center(CHART_WIDTH // 2, " ") + "│" + (right).center(CHART_WIDTH // 2, " ")
        return "│" + ("│" + row.center(CHART_WIDTH, " ") + "│").center(MAX_LINE_LENGTH, " ") + "│"
