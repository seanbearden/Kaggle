import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.regression.linear_model import OLS


def eda_ols(train, target_col, n_rows=4, n_cols=3):
    # Tech Debt: calculate the number of rows/columns you want in your subplot array

    # Create a figure to hold the subplots
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols * 5, n_rows * 5))

    # Flatten the array of axes for easy iterating
    axes = axes.flatten()

    # Loop through the features and create an OLS regression for each one
    for i, feature in enumerate(train.drop(target_col, axis=1).columns):
        # Create the OLS model
        X = train[feature]
        y = train[target_col]
        X_with_constant = sm.add_constant(X)
        model = OLS(y, X_with_constant).fit()

        # Plot the data and a regression line
        sns.regplot(x=feature, y=target_col, data=train, ax=axes[i], line_kws={'color': 'red'})

        # Set the title with the feature name and the R-squared value
        axes[i].set_title(f'{feature} vs {target_col}, R-squared: {model.rsquared:.2f}')

    # Adjust the layout so plots do not overlap
    plt.tight_layout()

    # Show the plot
    plt.show()
