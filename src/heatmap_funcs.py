"""
File: heatmap_funcs.py
Description: Helper functions for managing heatmaps on streamlit interface
Created by: Renesh Ravi
"""

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import seaborn as sns

def generate_heatmap(title, surface_matrix, x_labels, y_labels, colormap,
                     dynamic_format_func):
    """
    generate_heatmap creates a heatmap in streamlit framework
    :param title : string containing the title for the heatmap
    :param surface_matrix: np.ndarray containing surface matrix for heatmap
    :param x_labels: np.ndarray X-axis labels
    :param y_labels: np.ndarray Y-axis labels
    :param colormap: sns.cmap color map for the heatmap
    :param dynamic_format_func: function to formation the heatmap annotations
    """
    st.markdown(f"### {title}")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(
        surface_matrix,
        cmap=colormap,
        center=0,
        xticklabels=np.round(x_labels, 2),
        yticklabels=np.round(y_labels, 2),
        cbar_kws={'label': 'PnL ($)'}
    )
    annotate_heatmap(surface_matrix, ax, dynamic_format_func)
    ax.set_xlabel("Strike Price (K)")
    ax.set_ylabel("Spot Price (S)")
    st.pyplot(fig)

def dynamic_annotation_format(value):
    """
    dynamic_annotation_format scales the values within the
    heatmap based on its size
    :param value: float value that it used to scale the heatmap values
    """
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"  # Millions
    elif abs(value) >= 1_000:
        return f"{value / 1_000:.1f}K"  # Thousands
    else:
        return f"{value:.1f}"  # Default with one decimal place


# Custom annotation function for heatmap
def annotate_heatmap(data, ax, fmt_func):
    """
    annotate_heatmap integrates custom formatting for a heatmap
    :param data: numpy.ndarray containing the data to be annotated
    :param ax: matplotlib.axes.Axes object on which the heatmap is drawn
    :param fmt_func: function that returns a formatted string
    """
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            value = data[i, j]
            text = fmt_func(value)
            ax.text(j + 0.5, i + 0.5, text, ha="center", va="center", fontsize=8)