import sys

MIN_VALUE = 0
MAX_VALUE = sys.float_info.max

feasibility_metric_ranges = {
    "leadChange": (5, MAX_VALUE),
    "characterWon": (0.3, 0.7),
    "stageCoverage": (0.2, 1),
    # "nearDeathFrames": (100, 1000),
    "gameLength": (3600, 7200),
    "leastInteractionType": (0.07, 1)
}