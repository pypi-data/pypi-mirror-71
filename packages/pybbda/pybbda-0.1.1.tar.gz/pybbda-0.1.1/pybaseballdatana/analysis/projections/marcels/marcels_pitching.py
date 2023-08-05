from pybaseballdatana.data.tools.processing.aggregate import aggregate_by_season
from pybaseballdatana.data.tools.lahman.data import augment_lahman_pitching
from pybaseballdatana.data import LahmanData
from pybaseballdatana.analysis.projections.marcels.marcels_base import (
    MarcelsProjectionsBase,
)


class MarcelProjectionsPitching(MarcelsProjectionsBase):
    COMPUTED_METRICS = ["H", "HR", "ER", "BB", "SO", "HBP", "R"]
    RECIPROCAL_AGE_METRICS = ["H", "HR", "ER", "BB", "HBP", "R"]
    LEAGUE_AVG_PT = 134
    METRIC_WEIGHTS = (3, 2, 1)
    PT_WEIGHTS = (0.5, 0.1, 0)
    REQUIRED_COLUMNS = ["IPouts"]
    PLAYING_TIME_COLUMN = "IPouts"

    def __init__(self, stats_df=None, primary_pos_df=None):
        super().__init__(stats_df, primary_pos_df)

    def _load_data(self):
        return self.ld.pitching

    def preprocess_data(self, stats_df):
        return aggregate_by_season(augment_lahman_pitching(stats_df))

    def filter_non_representative_data(self, stats_df, primary_pos_df):
        return (
            stats_df.merge(primary_pos_df, on=["playerID", "yearID"], how="left")
            .query(r'primaryPos == "P"')
            .drop("primaryPos", axis=1)
        )

    def get_num_regression_pt(self, stats_df):
        fraction_games_started = stats_df.apply(
            lambda row: row["GS"] / row["G"], axis=1
        ).values
        return 75 + 105 * fraction_games_started


if __name__ == "__main__":

    ld = LahmanData()

    md = MarcelProjectionsPitching(ld.pitching)

    import time

    start = time.time()
    cnt = 0
    for season in range(2019, 2020 + 1):
        cnt += 1
        res = md.projections(season)
        # print(res)
        # print(res[res.playerID.str.contains("^bel")])
    end = time.time()
    dt = end - start
    print(res.sort_values("SO", ascending=False))
    print(dt, dt / cnt)
