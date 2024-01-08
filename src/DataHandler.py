import pandas as pd
from src.functional_utils import inform


class NotInPortfolio(Exception):
    """Exception handling for elements that are not part of the portfolio data."""
    def __init__(self, message: str):
        self._message = message

    def __str__(self):
        return "NotInPortfolio: " + self._message


class NotADataFrame(Exception):
    """Exception handling for elements that are not of type pandas.DataFrame."""
    def __init__(self, message: str):
        self._message = message

    def __str__(self):
        return "NotADataFrame: " + self._message


class PortfolioData:
    """Handles the storage of data."""
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
                raise NotADataFrame(f"The value specified for {key} is not of type pandas.DataFrame.")
            elif self.identifier_column_name not in value.columns:
                raise NotInPortfolio(f"The DataFrame {key} does not contain a '{self.identifier_column_name}' column.")
            else:
                self.portfolio_data.join(value)

    @inform
    def remove_data(self, columns: list):
        """Removes data columns from portfolio_data."""
        for column in columns:
            if column not in self.portfolio_data.columns:
                raise NotInPortfolio(f"{column} is not a column if the Portfolio.")
            else:
                self.portfolio_data = self.portfolio_data.drop(columns=columns)

    def __repr__(self):
        return self.portfolio_data.describe()


