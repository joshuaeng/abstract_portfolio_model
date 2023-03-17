import pandas as pd
from src.DataHandler import PortfolioData
from abc import ABC, abstractmethod


class Screener(ABC):
    @abstractmethod
    def add_screen(self, screen):
        raise NotImplementedError("This method is not implemented.")

    @abstractmethod
    def apply_screens(self):
        raise NotImplementedError("This method is not implemented.")


class Screen:
    """Creates Screen objects that can be input in PortfolioScreener."""
    def __init__(self, filter_name: str, column_name: str, condition: str):
        self.filter_name = filter_name
        self.column_name = column_name
        self.condition = condition

    def __repr__(self):
        return f"Screen({self.filter_name}, {self.column_name}, {self.condition})"


class PortfolioScreener(Screener):
    """
    Screener configuration. Handles the storage of screening related configuration.

    Example:
        inst = ScreenerConfig()
    """
    def __init__(self, portfolio_data: PortfolioData):
        self.portfolio_data = portfolio_data.portfolio_data
        self.screener_matrix = pd.DataFrame()
        self._screen_dict = dict()

    def add_screen(self, screen: Screen):
        """Adds filters into the _screening_matrix dictionary."""
        if screen.column_name not in self.portfolio_data.columns:
            raise AssertionError(f"'{screen.column_name}' is not in portfolio_data.")
        else:
            self._screen_dict.update(
                {screen.filter_name: eval(f"self.portfolio_data['{screen.column_name}'] {screen.condition}")}
            )

    def apply_screens(self):
        """Applies screens in portfolio data"""
        if self._screen_dict == dict():
            raise AssertionError("No Screen has been added yet.")
        else:
            self.screener_matrix = pd.DataFrame(self._screen_dict, index=self.portfolio_data.index)
            self.portfolio_data = self.portfolio_data.loc[self.screener_matrix.all(axis=1)]