# -*- coding: utf-8 -*-
"""21f3001271.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1SrrHZZGDu3sZZMzdxVcGNkTwfJTytZAI
"""

# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier
from sklearn.metrics import classification_report
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

#Import data
train = pd.read_csv('/content/train.csv')
test = pd.read_csv('/content/test.csv')

train.describe()

# Define feature engineering function
def create_features(df):
    # Create copy to avoid modifying original data
    df = df.copy()

    # Create age groups
    df['age_group'] = pd.cut(df['age'],
                            bins=[0, 20, 30, 40, 50, 60, 100],
                            labels=['0-20', '21-30', '31-40', '41-50', '51-60', '60+'])

    # Create balance groups
    df['balance_group'] = pd.qcut(df['balance'], q=5, labels=['very_low', 'low', 'medium', 'high', 'very_high'])

    # Create campaign intensity feature (handle division by zero)
    df['campaign_intensity'] = df['campaign'] / (df['pdays'].replace(-1, 999) + 1)
    df['campaign_intensity'] = df['campaign_intensity'].clip(upper=df['campaign_intensity'].quantile(0.99))

    # Create contact rate (handle division by zero)
    df['contact_rate'] = df['previous'] / (df['pdays'].replace(-1, 999) + 1)
    df['contact_rate'] = df['contact_rate'].clip(upper=df['contact_rate'].quantile(0.99))

    # Create interaction features
    df['age_balance'] = df['age'] * df['balance']
    df['age_balance'] = df['age_balance'].clip(upper=df['age_balance'].quantile(0.99))

    df['duration_campaign'] = df['duration'] * df['campaign']
    df['duration_campaign'] = df['duration_campaign'].clip(upper=df['duration_campaign'].quantile(0.99))

    # Replace any remaining infinities with NaN (will be handled by imputer)
    df = df.replace([np.inf, -np.inf], np.nan)

    return df

# prompt: can you explain the funciton that has been done here

import pandas as pd
import numpy as np
This code defines a function `create_features` for feature engineering on a Pandas DataFrame, likely for a machine learning model. Let's break down each step:


1. **Data Copying:**
   - `df = df.copy()`: Creates a copy of the input DataFrame to avoid modifying the original data.  This is a crucial step for data integrity.

2. **Age Group Creation:**
   - `df['age_group'] = pd.cut(...)`:  Creates a new categorical feature 'age_group' by binning the 'age' column into six age ranges (0-20, 21-30, ..., 60+). This transforms a numerical feature into a categorical one.

3. **Balance Group Creation:**
   - `df['balance_group'] = pd.qcut(...)`: Creates a new categorical feature 'balance_group' by dividing the 'balance' column into five quantiles (very_low, low, medium, high, very_high).  This converts a numerical feature into ordinal categories based on the distribution of the 'balance'.

4. **Campaign Intensity:**
   - `df['campaign_intensity'] = df['campaign'] / (df['pdays'].replace(-1, 999) + 1)`: Creates a new feature 'campaign_intensity'.  It represents the number of contacts performed during a campaign relative to the number of days that passed by after the client was last contacted. It replaces -1 values in `pdays` (likely indicating no previous contact) with 999 to avoid division by zero, though 999 might be too large a value. The `clip` function is then applied to set an upper bound on the values of 'campaign_intensity', restricting extremely large values.

5. **Contact Rate:**
   - `df['contact_rate'] = df['previous'] / (df['pdays'].replace(-1, 999) + 1)`:  Similar to 'campaign_intensity,' this creates a 'contact_rate' feature, but based on the number of previous contacts. Again, a large value (999) replaces -1 in `pdays` and `clip` sets an upper bound.

6. **Interaction Features:**
   - `df['age_balance'] = df['age'] * df['balance']`: Creates an interaction feature 'age_balance', which is the product of 'age' and 'balance'.  Interaction features capture relationships between two or more original features.
   - `df['duration_campaign'] = df['duration'] * df['campaign']`:  Similar interaction feature representing the product of 'duration' and 'campaign'.  Both interaction features have an upper bound.

7. **Infinity Handling:**
   - `df = df.replace([np.inf, -np.inf], np.nan)`: Replaces any infinite values (which might have arisen from divisions by zero or other numerical operations) with NaN (Not a Number).  This is important as many machine learning models cannot handle infinite values, but NaN values can typically be handled by imputation.

8. **Return:**
   - `return df`: Returns the modified DataFrame with the new engineered features.

**In summary:** This function aims to enhance the predictive power of a model by creating new features from existing ones. These engineered features capture various relationships and potentially reveal hidden patterns in the data, such as the intensity of marketing campaigns, contact rates, and combined effects of age and balance.  The use of quantiles and clipping helps prevent outliers from disproportionately affecting the model.

"""# **Exploratory Data Analysis**"""

#Distribution of class variable

plt.figure(figsize=(8,6))
Y = train["target"]
total = len(Y)*1.
ax=sns.countplot(x="target", data=train)
for p in ax.patches:
  ax.annotate('{:.1f}%'.format(100*p.get_height()/total), (p.get_x()+0.1, p.get_height()+5))

  #put 11 ticks (therefore 10 steps), from 0 to the total number of rows in the dataframe
  ax.yaxis.set_ticks(np.linspace(0, total, 11))
  #adjust the ticklabel to the desired format, without changing the position of the ticks.
  ax.set_yticklabels(map('{:.1f}%'.format, 100*ax.yaxis.get_majorticklocs()/total))
  ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
  # ax.legend(labels=["no","yes"])
  plt.show()

def countplot(label, dataset):
  plt.figure(figsize=(15,10))
  Y = train[label]
  total = len(Y)*1.
  ax=sns.countplot(x=label, data=dataset)
  for p in ax.patches:
    ax.annotate('{:.1f}%'.format(100*p.get_height()/total), (p.get_x()+0.1, p.get_height()+5))

  #put 11 ticks (therefore 10 steps), from 0 to the total number of rows in the dataframe
  ax.yaxis.set_ticks(np.linspace(0, total, 11))
  #adjust the ticklabel to the desired format, without changing the position of the ticks.
  ax.set_yticklabels(map('{:.1f}%'.format, 100*ax.yaxis.get_majorticklocs()/total))
  ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
  # ax.legend(labels=["no","yes"])
  plt.show()

# Process datetime
train['last contact date'] = pd.to_datetime(train['last contact date'])
train['year'] = train['last contact date'].dt.year
train['month'] = train['last contact date'].dt.month
train['weekday'] = train['last contact date'].dt.weekday
train.drop(columns=['last contact date'], inplace=True)

# Apply feature engineering
train = create_features(train)

# Split features and target
X = train.drop(columns=['target', 'year'])
y = (train['target'] == 'yes').astype(int)

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline

def countplot_withY(label, dataset):
  plt.figure(figsize=(20,10))
  Y = train[label]
  total = len(Y)*1.
  ax=sns.countplot(x=label, data=dataset, hue="target")
  for p in ax.patches:
    ax.annotate('{:.1f}%'.format(100*p.get_height()/total), (p.get_x()+0.1, p.get_height()+5))

  #put 11 ticks (therefore 10 steps), from 0 to the total number of rows in the dataframe
  ax.yaxis.set_ticks(np.linspace(0, total, 11))
  #adjust the ticklabel to the desired format, without changing the position of the ticks.
  ax.set_yticklabels(map('{:.1f}%'.format, 100*ax.yaxis.get_majorticklocs()/total))
  ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
  # ax.legend(labels=["no","yes"])
  plt.show()

countplot("job", train)

countplot_withY("job", train)

countplot("marital", train)

countplot_withY("marital", train)

countplot("default", train)

countplot_withY("default", train)

countplot("education",train)

countplot_withY("education", train)

countplot("housing", train)

countplot_withY("housing", train)

countplot("loan", train)

countplot_withY("loan", train)

countplot("contact", train)

countplot_withY("contact", train)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Assuming 'data_train' DataFrame is already loaded as shown in the provided code.

# Select the relevant columns for the correlation matrix
cols = ['age', 'balance', 'duration', 'campaign', 'pdays', 'previous']
correlation_matrix = train[cols].corr()

# Create the heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix')
plt.show()

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Define column groups
num = ['age', 'previous', 'pdays', 'duration', 'balance',
       'campaign_intensity', 'contact_rate', 'age_balance', 'duration_campaign']
ordinal_cat = ['education']
nominal_cat = ['marital', 'housing', 'loan', 'default', 'weekday', 'contact',
               'job', 'poutcome', 'age_group', 'balance_group']

# Create pipelines
num_pipe = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

ordinal_pipe = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('ordinal_encoder', OrdinalEncoder(categories=[['primary', 'secondary', 'tertiary']]))
])

nominal_pipe = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value='Missing')),
    ('onehot_encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

# Create preprocessor
preprocessor = ColumnTransformer(
    transformers=[
        ('numerical', num_pipe, num),
        ('ordinal', ordinal_pipe, ordinal_cat),
        ('nominal', nominal_pipe, nominal_cat)
    ],
    remainder='passthrough'
)

# Fit preprocessor and transform data
X_train_transformed = preprocessor.fit_transform(X_train)
X_test_transformed = preprocessor.transform(X_test)

"""# **Logistic Regression**"""

from sklearn.linear_model import LogisticRegression

# Initialize and train the Logistic Regression model
logreg_model = LogisticRegression(max_iter=1000, random_state=42) # Increased max_iter
logreg_model.fit(X_train_transformed, y_train)

# Make predictions on the test set
y_pred_logreg = logreg_model.predict(X_test_transformed)

# Evaluate the model
print(classification_report(y_test, y_pred_logreg))

# prompt: create auc visualization for the above graph

import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc

# Compute ROC curve and ROC area for each class
fpr, tpr, _ = roc_curve(y_test, logreg_model.predict_proba(X_test_transformed)[:, 1])
roc_auc = auc(fpr, tpr)

plt.figure()
lw = 2
plt.plot(fpr, tpr, color='darkorange',
         lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic example')
plt.legend(loc="lower right")
plt.show()

"""# **Random Forest**"""

from sklearn.ensemble import RandomForestClassifier

# Initialize and train the Random Forest Classifier
rf_classifier = RandomForestClassifier(random_state=42)
rf_classifier.fit(X_train_transformed, y_train)

# Make predictions
y_pred_rf = rf_classifier.predict(X_test_transformed)

# Evaluate the model
print(classification_report(y_test, y_pred_rf))

# Compute ROC curve and ROC area
fpr_rf, tpr_rf, _ = roc_curve(y_test, rf_classifier.predict_proba(X_test_transformed)[:, 1])
roc_auc_rf = auc(fpr_rf, tpr_rf)

plt.figure()
lw = 2
plt.plot(fpr_rf, tpr_rf, color='darkorange', lw=lw, label='ROC curve (area = %0.2f)' % roc_auc_rf)
plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Random Forest ROC Curve')
plt.legend(loc="lower right")
plt.show()

# prompt: create xgboost with randomized search cv mode;

from sklearn.model_selection import RandomizedSearchCV

# Define the parameter grid for XGBoost
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [3, 5, 7],
    'learning_rate': [0.01, 0.1, 0.2],
    'subsample': [0.8, 0.9, 1.0],
    'colsample_bytree': [0.8, 0.9, 1.0],
}

# Initialize XGBoost classifier
xgb_model = XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='logloss')

# Initialize RandomizedSearchCV
random_search = RandomizedSearchCV(
    estimator=xgb_model,
    param_distributions=param_grid,
    n_iter=10,  # Number of parameter settings that are sampled
    scoring='roc_auc',
    cv=5,
    n_jobs=-1,  # Use all available cores
    verbose=1,
    random_state=42
)

# Fit the randomized search to the data
random_search.fit(X_train_transformed, y_train)

# Get the best model
best_xgb_model = random_search.best_estimator_

# Make predictions using the best model
y_pred_xgb = best_xgb_model.predict(X_test_transformed)

# Evaluate the model
print(classification_report(y_test, y_pred_xgb))

# Compute ROC curve and ROC area
fpr_xgb, tpr_xgb, _ = roc_curve(y_test, best_xgb_model.predict_proba(X_test_transformed)[:, 1])
roc_auc_xgb = auc(fpr_xgb, tpr_xgb)

plt.figure()
lw = 2
plt.plot(fpr_xgb, tpr_xgb, color='darkorange', lw=lw, label='ROC curve (area = %0.2f)' % roc_auc_xgb)
plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('XGBoost ROC Curve')
plt.legend(loc="lower right")
plt.show()

# Print the best hyperparameters
print("Best hyperparameters:", random_search.best_params_)

# Process test data similarly to training data
test['last contact date'] = pd.to_datetime(test['last contact date'])
test['year'] = test['last contact date'].dt.year
test['month'] = test['last contact date'].dt.month
test['weekday'] = test['last contact date'].dt.weekday
test.drop(columns=['last contact date'], inplace=True)

# Apply feature engineering to test data
test = create_features(test)

# Drop year column to match training data
test = test.drop(columns=['year'])

# Transform test data using fitted preprocessor
test_transformed = preprocessor.transform(test)

# prompt: make predictions in test data

# Predict on the test data using the best XGBoost model
test_predictions = best_xgb_model.predict(test_transformed)

# Print or save the predictions
test_predictions
# Example: Save predictions to a CSV file
#submission = pd.DataFrame({'target': test_predictions})
#submission.to_csv('submission.csv', index=False)

# prompt: create submission dataframe and save predictions to csv

submission = pd.DataFrame({'target': test_predictions})
submission.to_csv('submission.csv', index=False)