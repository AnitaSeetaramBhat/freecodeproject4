import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def draw_cat_plot():
    # Import data
    df = pd.read_csv('medical_examination.csv')

    # Add 'overweight' column
    df['overweight'] = ((df['weight'] / (df['height'] / 100) ** 2) > 25).astype(int)

    # Normalize data by making 0 always good and 1 always bad
    df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
    df['gluc'] = (df['gluc'] > 1).astype(int)

    # Create DataFrame for cat plot using pd.melt
    df_cat = pd.melt(
        df,
        id_vars=['cardio'],
        value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight']
    )

    # Group and reformat the data to split it by 'cardio'
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='total')

    # Draw the catplot
    fig = sns.catplot(
        x='variable', y='total', hue='value', col='cardio', data=df_cat,
        kind='bar', height=5, aspect=1
    ).fig

    # Save the figure
    fig.savefig('catplot.png')
    return fig

def draw_heat_map():
    # Import data
    df = pd.read_csv('medical_examination.csv')

    # Add 'overweight' column
    df['overweight'] = ((df['weight'] / (df['height'] / 100) ** 2) > 25).astype(int)

    # Normalize data by making 0 always good and 1 always bad
    df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
    df['gluc'] = (df['gluc'] > 1).astype(int)

    # Clean the data
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(12, 12))

    # Draw the heatmap
    sns.heatmap(
        corr, mask=mask, annot=True, fmt='.1f', center=0, square=True, cbar_kws={'shrink': 0.5}, ax=ax
    )

    # Save the figure
    fig.savefig('heatmap.png')
    return fig

def main():
    draw_cat_plot()
    draw_heat_map()

if __name__ == "__main__":
    main()
