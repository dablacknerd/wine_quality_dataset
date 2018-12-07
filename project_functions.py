from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import pandas as pd

def transform_corr_matrix(matrix):
    result =[]
    for col1 in matrix.columns.tolist():
        for col2 in matrix.columns.tolist():
            p_cor = round(matrix.loc[col1][col2],1)
            result.append([col1,col2,p_cor])
    return result

def variance_inflation_factor(r2):
    return round(1.0/(1.0-r2),2)

def calculate_vif_per_factor(df,features):
    results =[]
    columns_tokeep =[]
    for y_feature in features:
        x_features = list(set(features) - set([y_feature]))
        #print(x_features)
        #print(y_feature)
        X = df[x_features].values
        y = df[y_feature].values
        lm = LinearRegression().fit(X,y)
        y_hat = lm.predict(X)
        r_2 = r2_score(y,y_hat)
        #print(r_2)
        vif = variance_inflation_factor(r_2)
        results.append([y_feature,vif])
        if vif < 5.0:
            columns_tokeep.append(y_feature)
    return pd.DataFrame(results,columns=['Features','VIF']),columns_tokeep
    

def features_iqr(df):
    results = []
    for col in df.columns:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        lower_bound = round(q1 - (1.5*(q3-q1)),2)
        upper_bound = round(q3 + (1.5*(q3-q1)),2)
        results.append([col,lower_bound,upper_bound])
    return results

def is_outlier(value,lower_bound,upper_bound):
    if float(value) < lower_bound or float(value) > upper_bound:
        return 1
    else:
        return 0

def outlier_checker(df,features_iqr):
    results =[]
    for idx in df.index:
        row = df.loc[idx]
        temp =[]
        for tupe in features_iqr:
            value = row[tupe[0]]
            lb = tupe[1] # lower bound
            ub = tupe[2] # upper bound
            temp.append(is_outlier(value,lb,ub))
        #if np.array(temp).sum != 0:
            #results.append('Y')
        #else:
        results.append(sum(temp))
    return results