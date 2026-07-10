import pandas


class BrandUtils:

    def __init__(self) -> None:
        self.mapped_column_names = {
            'name': 'name',
            'brand_code': 'brandCode'
        }

    def mapper(self, data: list) -> list | None | str:
        if len(data) == 0:
            return '[]'
        dataframe = pandas.DataFrame.from_records(data)
        dataframe.rename(columns=self.mapped_column_names, inplace=True)
        return dataframe.to_json(orient='records')
