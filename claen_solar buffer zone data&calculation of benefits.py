
import pandas as pd
df = pd.read_excel("Solar buffer zone data and calculation of benefits_1.xlsx",sheetname=1)
df['Dol_pAc']=df['wprice*yield']
df.loc[df['Dol_pAc'] == 0, 'Dol_pAc'] = df['f_value/acre']
df['Dol_NPpAc'] = df['Dol_pAc']*df['DN']
df['Dol_HBpAc'] = df['Dol_pAc']*df['DH']

#create unique list of state
UniqueState = df.state.unique()
#create a data frame dictionary to store your data frames
dfDict = {elem : pd.DataFrame for elem in UniqueState}
for key in dfDict.keys():
    dfDict[key] = df[:][df.state== key]

def wavg(group, avg_name, weight_name):
    """
    http://stackoverflow.com/questions/10951341/pandas-dataframe-aggregate-function-using-multiple-columns
    In rare instance, we may not have weights, so just return the mean.
    """
    d = group[avg_name]
    w = group[weight_name]
    try:
        return (d * w).sum() / w.sum()
    except ZeroDivisionError:
        return d.mean()

'''
Use ACRES_C as weight for calcualting Weighted Average pollinator dependency of crops for the following reason:
1. the crop land area data shows the cultivation zone or each crop, thus reflect the imporatnce of each crop in that area
2. ACRES_C have no missing value
'''
# wavg(il,"DH", "f_Dol_HBpAc")
# wavg(il,"DH", "total_yield")
wavg(il,"DH", "ACRES_C")

w_DH = df.groupby("state").apply(wavg, "DH", "ACRES_C").reset_index(name='w_ DH')
w_DN = df.groupby("state").apply(wavg, "DN", "ACRES_C").reset_index(name='w_ DN')
w_Dol_NPpAc = df.groupby("state").apply(wavg, "Dol_NPpAc", "ACRES_C").reset_index(name='w_Dol_NPpAc')
w_Dol_HBpAc = df.groupby("state").apply(wavg, "Dol_HBpAc", "ACRES_C").reset_index(name='w_Dol_HBpAc')

f_df = pd.read_excel("Solar buffer zone data and calculation of benefits_1.xlsx",sheetname=0)

f_df = f_df.merge(w_DH,left_on='STATE ABBREVIATION', right_on='state', how='outer')
f_df = f_df.merge(w_DN,left_on='STATE ABBREVIATION', right_on='state', how='outer')
f_df = f_df.merge(w_Dol_NPpAc,left_on='STATE ABBREVIATION', right_on='state', how='outer')
f_df = f_df.merge(w_Dol_HBpAc,left_on='STATE ABBREVIATION', right_on='state', how='outer')
f_df.to_excel('Solar buffer zone data and calculation of benefits_toJoin.xlsx')
