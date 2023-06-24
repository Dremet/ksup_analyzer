import numpy as np
import pandas as pd


class Result:
    def __init__(self, results_dict: dict) -> None:
        self.assign_individual_properties(results_dict)
        self.series = None

    def assign_individual_properties(self, res: dict) -> None:
        """
        When it comes to results, there are some that describe the drivers individual performance like lap times
        and some that need more context, namely times of other drivers in order to infer positions for example.

        This method uses the (mostly) individual results given in the replay files. Only exception is the "num_laps_led"
        property which includes knowledge of other drivers times of course.
        """
        self.driver_id = res["racingTeamId"]

        # this is the total time from session begin until the driver finsished the last lap
        # this is None if the driver did not finish
        # it does include the time a driver needs in "lap 0" until the beginning of lap 1 (crossing the start/finish line)
        self.total_time = res["finishTime"]
        # list of lap times
        self.lap_times = res["lapTimes"]
        # number of laps driven, relevant for lappings
        self.num_laps_driven = len(self.lap_times) if self.lap_times else np.nan
        # minimum lap time
        self.fastest_lap_time = min(self.lap_times) if self.lap_times else np.nan
        # list of time penalties per lap, it does not include hitting CCDs during the race cause that
        # only slows you down (it does not give a time penalty)
        self.lap_time_penalties = res["lapTimePenalties"]
        # how many laps the driver led; interesting in a multi-lap quali
        self.num_laps_led = res["numLapsLed"]
        # metres driven, not sure if relevant
        self.metres_driven = res["metresDriven"]

        # as the total time includes the time from the starting position to the start/finish line
        # and the lap times do not, we can extract the time the driver needed to get there
        # This is relevant to calculate positions per lap because we need to add this time to the lap times
        # in order to calculate positions
        self.time_until_starting_line = (
            self.total_time - sum(self.lap_times) if self.total_time else None
        )

    def as_series(self) -> pd.Series:
        if self.series is None:
            property_attributes = [
                attr
                for attr in dir(self)
                if not attr.startswith("__")
                and not callable(getattr(self, attr))
                and attr not in ["series", "driver_id"]
            ]

            indices = property_attributes

            data = [getattr(self, attr) for attr in property_attributes]

            self.series = pd.Series(data=data, index=indices, name=self.driver_id)

        return self.series


class RaceResult(Result):
    def __init__(self, results_dict: dict) -> None:
        super().__init__(results_dict)


class QualiResult(Result):
    def __init__(self, results_dict: dict) -> None:
        super().__init__(results_dict)


class RaceResultsDataFrame(pd.DataFrame):
    @property
    def _constructor(self):
        return RaceResultsDataFrame

    def _run_result_calculations(self) -> None:
        pass
