import pandas as pd
import os


'''Filter out empty rows and only keep rows where a user was put out of priority for a non-zero % of day'''
# years_list = os.listdir('yearly_data/')
# years_list = years_list[1:]
# # years_list = ['2018.csv']
# print(years_list)
#
# for year in years_list:
#     print(year)
#     df = pd.read_csv('yearly_data/' + year)
#     filtered_df = df.loc[df['analysisOutOfPriorityPercentOfDay'] > 0]
#     print(filtered_df)
#     filtered_df.to_csv('yearly_data/' + year)
#
######################################################################################################

'''Remove unnecessary columns'''
#
# years_list = os.listdir('yearly_data/')
# years_list = years_list[1:]
# # years_list = years_list[2:]
# # years_list = ['2002.csv']
# print(years_list)
#
# for year in years_list:
#     print(year)
#     df = pd.read_csv('yearly_data/' + year, dtype = object)
#     new_df = df.filter(['analysisDate', 'analysisWdid', 'analysisStructureName',
#                         'analysisOutOfPriorityPercentOfDay','locationWdid', 'locationStructure', 'priorityWdid', 'priorityStructure', ], axis=1)
#     new_df.to_csv('yearly_data_lite/' + year, index = False)

######################################################################################################

'''Add node and edge attributes'''