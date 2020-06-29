import os, sys

class Seasonality:
    __name__ = "translation_augmentation"

    def determine_path(self):
        try:
            root = __file__
            if os.path.islink(root):
                root = os.path.realpath(root)
            return os.path.dirname(os.path.abspath(root))

        except:
            print("I'm sorry, but something is wrong.")
            print("There is no __file__ variable. Please contact the author.")
            sys.exit()

    def start(self):
        print("module is running")
        print(self.determine_path())
        print("My various data files and so on are:")
        files = [f for f in os.listdir(self.determine_path() + "/things")]
        print(files)

    def validate_date_format(self, data, date_column='DATE'):
        # transform to appropriate date format
        data[date_column] = data[date_column].astype('datetime64')
        return data

    def create_extra_columns(self, data, basis, date_column='DATE'):
        data['YEAR'] = data[date_column].dt.year

        if basis == 'QUARTER':
            data[basis] = data[date_column].dt.quarter
        elif basis == 'MONTH':
            data[basis] = data[date_column].dt.month
        elif basis == 'WEEK':
            data[basis] = data[date_column].dt.week
        elif basis == 'DAY':
            data[basis] = data[date_column].dt.day
        else:
            print('Cannot find the requested basis: ' + basis + ' in the provided DATE column'+'\n The available'+
            ' options for the basis are one of the following: [QUARTER,MONTH,WEEK,DAY]')
        return data

    def remove_seasonality_plain(self, data_2_deseasonalize, base_data, value_column='PRICE', date_column='DATE', basis='MONTH'):
        '''
        We learn the seasonality from the the 'base_data' and we remove it from the 'data_2_deseasonalize'.
        We can use this method in case we have a single class in the dataset
        NOTE: We can have the same 'base_data' and 'data_2_deseasonalize'.
        NOTE: The more years available in the 'base_data' the better
        NOTE: The column 'DATE' should be available in both 'base_data' and 'data_2_deseasonalize'.

        :param data_2_deseasonalize: the data that we want to remove the seasonality from

        :param base_data: the data that should be used to create the seasonality indexes

        :param value_column: the column that contains the value that needs to be deseasonalized

        :param date_column: the column that contains the dates

        :param basis: in which basis should the seasonality be removed
                     available options --> ['QUARTER','MONTH','WEEK','DAY']
        '''
        # create the proper date format
        base_data = self.validate_date_format(data=base_data, date_column=date_column)

        # create the needed columns for year, basis(quarter/month/week/day),extra columns
        base_data = self.create_extra_columns(data=base_data, basis=basis, date_column=date_column)

        # find price per required time preriod
        original_price = base_data.groupby(['YEAR', basis]).agg({value_column: 'mean'})
        original_price.reset_index(inplace=True)

        # find the yearly price
        yearly_price = base_data.groupby(['YEAR']).agg({value_column: 'mean'})
        yearly_price.reset_index(inplace=True)

        # merge both prices in a single dataframe
        merged_prices = original_price.merge(yearly_price, on=['YEAR'])
        merged_prices.rename(columns={value_column + '_x': basis + '_AVERAGE', value_column + '_y': 'YEARLY_AVERAGE'},
                             inplace=True)
        merged_prices['SEASONAL_INDEX'] = merged_prices[basis + '_AVERAGE'] / merged_prices['YEARLY_AVERAGE']

        # find the average seasonal index
        averaged_SI = merged_prices.groupby([basis]).agg({'SEASONAL_INDEX': 'mean'})
        averaged_SI.reset_index(inplace=True)
        averaged_SI.rename(columns={'SEASONAL_INDEX': 'AVG_SEASONAL_INDEX'}, inplace=True)

        # remove seasonality
        data_2_deseasonalize = self.validate_date_format(data=data_2_deseasonalize, date_column=date_column)
        data_2_deseasonalize = self.create_extra_columns(data=data_2_deseasonalize, basis=basis, date_column=date_column)
        final_df = data_2_deseasonalize.merge(averaged_SI[['AVG_SEASONAL_INDEX', basis]], on=basis)
        final_df['DS_' + value_column] = final_df[value_column] / final_df['AVG_SEASONAL_INDEX']
        final_df.drop(['YEAR', 'AVG_SEASONAL_INDEX', basis], axis=1, inplace=True)

        return final_df

    def remove_seasonality(self, data_2_deseasonalize, base_data, value_column='PRICE', category_column='CATEGORY',
                           date_column='DATE', basis='MONTH'):
        '''
        We learn the seasonality from the the 'base_data' and we remove it from the 'data_2_deseasonalize'.
        We can use this method in case we have multiple classes in the dataset
        NOTE: We can have the same 'base_data' and 'data_2_deseasonalize'.
        NOTE: The more years available in the 'base_data' the better
        NOTE: The column 'DATE' should be available in both 'base_data' and 'data_2_deseasonalize'.

        :param data_2_deseasonalize: the data that we want to remove the seasonality from

        :param base_data: the data that should be used to create the seasonality indexes

        :param value_column: the column that contains the value that needs to be deseasonalized

        :param category_column: the column that contains the different categories

        :param date_column: the column that contains the dates

        :param basis: in which basis should the seasonality be removed
                     available options --> ['QUARTER','MONTH','WEEK','DAY']

        '''


        # create the proper date format
        base_data = self.validate_date_format(data=base_data, date_column=date_column)

        # create the needed columns for year, basis(quarter/month/week/day),extra columns
        base_data = self.create_extra_columns(data=base_data, basis=basis, date_column=date_column)

        # find price per required time preriod
        original_price = base_data.groupby(['YEAR', basis, category_column]).agg({value_column: 'mean'})
        original_price.reset_index(inplace=True)

        # find the yearly price
        yearly_price = base_data.groupby(['YEAR', category_column]).agg({value_column: 'mean'})
        yearly_price.reset_index(inplace=True)

        # merge both prices in a single dataframe
        merged_prices = original_price.merge(yearly_price, on=['YEAR', category_column])
        merged_prices.rename(columns={value_column + '_x': basis + '_AVERAGE', value_column + '_y': 'YEARLY_AVERAGE'},
                             inplace=True)
        merged_prices['SEASONAL_INDEX'] = merged_prices[basis + '_AVERAGE'] / merged_prices['YEARLY_AVERAGE']

        # find the average seasonal index
        averaged_SI = merged_prices.groupby([category_column, basis]).agg({'SEASONAL_INDEX': 'mean'})
        averaged_SI.reset_index(inplace=True)
        averaged_SI.rename(columns={'SEASONAL_INDEX': 'AVG_SEASONAL_INDEX'}, inplace=True)

        # remove seasonality
        data_2_deseasonalize = self.validate_date_format(data=data_2_deseasonalize, date_column=date_column)
        data_2_deseasonalize = self.create_extra_columns(data=data_2_deseasonalize, date_column=date_column, basis=basis)

        final_df = data_2_deseasonalize.merge(averaged_SI[['AVG_SEASONAL_INDEX', category_column, basis]],
                                              on=[category_column, basis])
        final_df['DS_' + value_column] = final_df[value_column] / final_df['AVG_SEASONAL_INDEX']
        final_df.drop(['YEAR', 'AVG_SEASONAL_INDEX', basis, ], axis=1, inplace=True)
        return final_df
