# SeasonalityRemoval

## This is a pure Python project that removes the Seasonality from timeseries when the Date is available.

### Install
```shell
pip install seasonality-removal
```

### Import into the project
```shell
from Seasonality.Seasonality import Seasonality
```

### Example 1 (when we have a single product or category)
##### In the data we want to deseasonalize we should have at least a date column ( in this case 'DATE') and a value column (in this case 'PRICE'). The data should be provided as a pandas dataframe.
##### data_2_deseasonalize
DATE | PRICE 
--- | --- 
2014-03-05 | 15
2014-03-06 | 16
... | ...
2020-08-08 | 19 

We can select to learn the seasonality from the base_data that are in the same format as the data_2_deseasonalize or use the same data to both learn and remove seasonality. The basis indicates what type of seasonality we want to remove (in this case the monthly seasonality). The available options for the basis are [QUARTER,MONTH,WEEK,DAY]. The value_column and the date_column indicate the column names that contain the date and the values that we want to deseasonalize (in this case 'DATE' and 'PRICE' accordingly)
```shell
ds_data = seasonality.remove_seasonality_plain(data_2_deseasonalize=data_2_deseasonalize, base_data=data_2_deseasonalize, 
                                               basis='MONTH', value_column='PRICE',date_column='DATE')
```
##### output (ds_data)
DATE | PRICE | DS_PRICE
--- | --- | ---
2014-03-05 | 15 | 15.23
2014-03-06 | 16 | 15.97
... | ... | ...
2020-08-08 | 19 | 18.88


### Example 2 (when we have a multiple products or categories)
##### In the data we want to deseasonalize we should have at least a date column ( in this case 'DATE'), a value column (in this case 'PRICE') and a category column (in this case 'CATEGOTY'). The data should be provided as a pandas dataframe.
##### data_2_deseasonalize
DATE | CATEGORY | PRICE
--- | --- | ---
2014-03-05 | Pasta | 1.27
2014-03-06 | Meat | 6.32
... | ... | ...
2020-08-08 | Milk | 1.78

We can select to learn the seasonality from the base_data that are in the same format as the data_2_deseasonalize or use the same data to both learn and remove seasonality. The basis indicates what type of seasonality we want to remove (in this case the weekly seasonality). The available options for the basis are [QUARTER,MONTH,WEEK,DAY]. The value_column, the category_column and the date_column indicate the column names that contain the date, the categories and the values that we want to deseasonalize (in this case 'DATE','CATEGORY' and 'PRICE' accordingly)
```shell
ds_data = seasonality.remove_seasonality(data_2_deseasonalize=data_2_deseasonalize, base_data=data_2_deseasonalize, 
                                         basis='WEEK', value_column='PRICE',date_column='DATE', 
                                         category_column='CATEGORY')
```
##### output (ds_data)
DATE | CATEGORY | PRICE | DS_PRICE
--- | --- | --- | ---
2014-03-05 | Pasta | 1.27 | 1.34
2014-03-06 | Meat | 6.32 | 6.12
... | ... | ...| ...
2020-08-08 | Milk | 1.78 | 1.85
