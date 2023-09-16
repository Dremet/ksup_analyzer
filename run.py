from ksup_analyzer.replay.FileHandler import FileHandler
from ksup_analyzer.event.Event import Race, Quali, Event
from ksup_analyzer.event.LineUp import LineUp
from ksup_analyzer.plots.Plots import (
    GapToWinnerTablePlot,
    LapPositionTablePlot,
    GapToLeaderTablePlot,
)

fh = FileHandler(
    [
        "example_replay_files/20230915T22-07-51Z.header",
        "example_replay_files/20230915T22-19-14Z.header",
    ]
)


quali = Quali(fh.get_quali_file_content())
race = Race(fh.get_race_file_content())
lineup = LineUp(fh.get_race_file_content())

event = Event(lineup=lineup, race=race, quali=quali)
event.create_result_dataframe()
event.run_result_calculations()

print(event.result_df)
print(event.result_df.lap_position_table)

print(
    event.result_df[
        ["name", "fastest_lap_time_quali", "starting_position_race"]
    ].sort_values(by="starting_position_race")
)

gapToWinnerPlot = GapToWinnerTablePlot(event.result_df, race)
gapToWinnerPlot.plot(ymin=-5, ymax=15)
lapPositionPlot = LapPositionTablePlot(event.result_df, race)
lapPositionPlot.plot("Example_Replay")
gapToLeaderPlot = GapToLeaderTablePlot(event.result_df, race)
gapToLeaderPlot.plot(ymax=15)
