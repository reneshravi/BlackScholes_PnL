import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import seaborn as sns

def generate_heatmap(title, pnl_surface, x_labels, y_labels, colormap, dynamic_format_func):
    st.markdown(f"### {title}")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(
        pnl_surface,
        cmap=colormap,
        center=0,
        xticklabels=np.round(x_labels, 2),
        yticklabels=np.round(y_labels, 2),
        cbar_kws={'label': 'PnL ($)'}
    )
    annotate_heatmap(pnl_surface, ax, dynamic_format_func)
    ax.set_xlabel("Strike Price (K)")
    ax.set_ylabel("Spot Price (S)")
    st.pyplot(fig)

def dynamic_annotation_format(value):
    """Format annotation based on value magnitude."""
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"  # Millions
    elif abs(value) >= 1_000:
        return f"{value / 1_000:.1f}K"  # Thousands
    else:
        return f"{value:.1f}"  # Default with one decimal place


# Custom annotation function for heatmap
def annotate_heatmap(data, ax, fmt_func):
    """Annotate a heatmap with custom formatting."""
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            value = data[i, j]
            text = fmt_func(value)
            ax.text(j + 0.5, i + 0.5, text, ha="center", va="center", fontsize=8)