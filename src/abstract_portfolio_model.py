import pandas as pd
from src.functional_utils import inform
from abc import ABC, abstractmethod
from typing import List


class PortfolioData:
    """Portfolio data class. Handles the storage of data."""

    def __init__(self, base_universe: pd.Dataframe, identifier_column_name: str = "ISIN"):
        self.identifier_column_name = identifier_column_name
        self.portfolio_data: pd.DataFrame = base_universe.set_index(self.identifier_column_name)

    def __setattr__(self, key, value):
        return setattr(self, key, value)

    @inform
    def add_data(self, **kwargs):
        """Adds data column into portfolio_data."""
        for key, value in kwargs.items():
            if not isinstance(value, pd.DataFrame):
                raise AssertionError(f"The value specified for {key} is not a pandas.DataFrame object.")
            elif self.identifier_column_name not in value.columns:
                raise AssertionError(f"The DataFrame {key} does not contain a '{self.identifier_column_name}' column.")
            else:
                self.portfolio_data.join(value)

    @inform
    def remove_data(self, columns: list):
        """Removes data columns from portfolio_data."""
        self.portfolio_data = self.portfolio_data.drop(columns=columns)

    def __repr__(self):
        return self.portfolio_data.describe()


class Filter:
    """Filter class. Creates Filter objects that can be input in ScreenerConfig."""

    def __init__(self, filter_name: str, column_name: str, condition: str):
        self.filter_name = filter_name
        self.column_name = column_name
        self.condition = condition

    def __repr__(self):
        return f"Filter({self.filter_name}, {self.column_name}, {self.condition})"


class PortfolioScreener:
    """
    Screener configuration. Handles the storage of screening related configuration.

    Example:
        inst = ScreenerConfig()
    """

    def __init__(self, portfolio_data: PortfolioData):
        self.portfolio_data = portfolio_data.portfolio_data
        self.screener_matrix = pd.DataFrame()
        self.screening_results = pd.DataFrame()
        self._screen_dict = dict()

    def add_filters(self, _filter: Filter):
        """Adds filters into the _screening_matrix dictionary."""
        if _filter.column_name not in self.portfolio_data.columns:
            raise AssertionError(f"'{_filter.column_name}' is not in base_universe.")
        else:
            self._screen_dict.update(
                {_filter.filter_name: eval(f"self.base_universe['{_filter.column_name}'] {_filter.condition}")}
            )

    def _get_screener_matrix(self):
        self.screener_matrix = pd.DataFrame(self._screen_dict, index=self.portfolio_data.index)

    def apply_screen(self):
        self._get_screener_matrix()
        self.screening_results = self.portfolio_data.loc[self.screening_results.all(axis=1)]


