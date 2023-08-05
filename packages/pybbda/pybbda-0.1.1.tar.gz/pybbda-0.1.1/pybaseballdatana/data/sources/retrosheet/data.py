import os
import psycopg2
import pandas as pd
import logging

from sqlalchemy import create_engine
from pychadwick.chadwick import Chadwick
from pybaseballdatana import PYBBDA_DATA_ROOT

logger = logging.getLogger(__name__)


class RetrosheetData:
    def __init__(self, data_root=None):
        self.data_root = data_root or PYBBDA_DATA_ROOT
        self.db_dir = os.path.join(self.data_root, "retrosheet")
        self.db_path = os.path.join(self.db_dir, "retrosheet.db")
        self._engine = None
        self.chadwick = Chadwick()

    def _connect_to_postgres(self, database="retrosheet"):
        conn = psycopg2.connect(
            database=database,
            user=os.environ["PSQL_USER"],
            password=os.environ["PSQL_PASS"],
            port=os.environ["PSQL_PORT"],
        )
        return conn

    def create_database(self):
        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir, exist_ok=True)
        self._engine = create_engine(f"sqlite:///{self.db_path}", echo=False)

    @property
    def engine(self):
        if not self._engine:
            self._engine = create_engine(f"sqlite:///{self.db_path}", echo=False)
        return self._engine

    def initialize_table(self, df, conn=None):
        conn = conn or self.engine
        df.to_sql("event", conn, index=False, if_exists="replace")

    def update_table(self, df, conn=None):
        logger.info("updating table with %s", df.GAME_ID.iloc[0])
        conn = conn or self.engine
        df.to_sql("event", conn, index=False, if_exists="append")

    def query(self, query):
        return pd.read_sql_query(query, self.engine)

    def df_from_file(self, file_path):
        games = self.chadwick.games(file_path)
        return self.chadwick.games_to_dataframe(games)
