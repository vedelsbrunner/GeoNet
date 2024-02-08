import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

df_overlap = pd.read_csv('likert_scale_node_overlap.csv')
df_usability = pd.read_csv('likert_scale_usability.csv')

df_overlap_melt = pd.melt(df_overlap, id_vars=['Participant'], var_name='Technique', value_name='Overlap Ranking')
df_usability_melt = pd.melt(df_usability, id_vars=['Participant'], var_name='Technique', value_name='Usability Ranking')

df_merged = pd.merge(df_overlap_melt, df_usability_melt, on=['Participant', 'Technique'])

avg_overlap_ranking = df_merged.groupby('Technique')['Overlap Ranking'].mean().reset_index()
avg_usability_ranking = df_merged.groupby('Technique')['Usability Ranking'].mean().reset_index()

avg_rankings = pd.merge(avg_overlap_ranking, avg_usability_ranking, on='Technique', suffixes=('_Overlap', '_Usability'))

avg_rankings_overlap_sorted = avg_rankings.sort_values(by='Overlap Ranking', ascending=False)
avg_rankings_usability_sorted = avg_rankings.sort_values(by='Usability Ranking', ascending=False)

plt.figure(figsize=(11, 10))

bar_width = 0.5

legend_patches_node_overlap = [
    Patch(facecolor='#000000', label='1 = Very Ineffective'),
    Patch(facecolor='#000000', label='2 = Somewhat Ineffective'),
    Patch(facecolor='#000000', label='3 = Neutral'),
    Patch(facecolor='#000000', label='4 = Somewhat Effective'),
    Patch(facecolor='#000000', label='5 = Very Effective')
]

legend_patches_usability = [
    Patch(facecolor='#000000', label='1 = Very Difficult'),
    Patch(facecolor='#000000', label='2 = Somewhat Difficult'),
    Patch(facecolor='#000000', label='3 = Average'),
    Patch(facecolor='#000000', label='4 = Somewhat Easy'),
    Patch(facecolor='#000000', label='5 = Very Easy')
]

plt.subplot(1, 2, 1)
overlap_plot = sns.barplot(data=avg_rankings_overlap_sorted, x='Technique', y='Overlap Ranking', color='#000000', width=bar_width)
plt.title('Average Overlap Resolution Ranking')
plt.xlabel('Layout')
plt.ylabel('Average Ranking')
plt.yticks(ticks=range(1, 6))
overlap_plot.set_xticklabels(overlap_plot.get_xticklabels(), rotation=45, horizontalalignment='right')
plt.legend(handles=legend_patches_node_overlap, title="Likert Scale", loc='upper right')

plt.subplot(1, 2, 2)
usability_plot = sns.barplot(data=avg_rankings_usability_sorted, x='Technique', y='Usability Ranking', color='#000000', width=bar_width)
plt.title('Average Usability Ranking')
plt.xlabel('Layout')
plt.ylabel('Average Ranking')
plt.yticks(ticks=range(1, 6))
usability_plot.set_xticklabels(usability_plot.get_xticklabels(), rotation=45, horizontalalignment='right')
plt.legend(handles=legend_patches_usability, title="Likert Scale", loc='upper right')

plt.tight_layout()
plt.show()
