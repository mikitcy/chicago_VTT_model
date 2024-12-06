import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Function to calculate the cumulative distribution
def calculate_cumulative_distribution(data):
    sorted_data = np.sort(data)
    yvals = np.arange(1, len(sorted_data) + 1) / float(len(sorted_data))
    return sorted_data, yvals

# 04_Plotting function
def plot_single_cumulative_distribution(dfs, attribute, labels, ax):
    lines = []
    for df, label in zip(dfs, labels):
        data = df[attribute]
        x, y = calculate_cumulative_distribution(data)
        line, = ax.plot(x, y, label=f"{label}")
        lines.append(line)

    ax.set_xlabel(f'{attribute.capitalize()}')
    ax.set_ylabel('Cumulative Distribution [%]')
    ax.set_title(f'{attribute.capitalize()}')
    ax.set_xlim(left=0, right=150) #For private cost. Delete to get social cost
    ax.grid(True)
    return lines

def plot_cumulative_distribution(dfs, attributes, labels, fig, axes, filepath):
    colors = [
        "#42d4f4",  # bright sky blue
        "#f58231", # orange
        "#3cb44b",  # bright green
    ]

    for i, attribute in enumerate(attributes):
        ax = axes.flatten()[i]
        plot_single_cumulative_distribution(dfs, attribute, labels, ax)
        ax.grid(False)
        for line, color in zip(ax.get_lines(), colors):
            line.set_color(color)
            line.set_linewidth(2)

    plt.tight_layout()
    plt.savefig(filepath)
    plt.show()

def plot_cumulative_distribution_comparison(df, attributes, ax, filepath):
    lines = []
    legends = []
    for i, attribute in enumerate(attributes):
        data = df[attribute]
        x, y = calculate_cumulative_distribution(data)
        line, = ax.plot(x, y)
        lines.append(line)
        legends.append(attribute)
        ax.set_xlabel(f'{attribute.capitalize()}')
        ax.set_ylabel('Cumulative Distribution [%]')
        ax.grid(True)

    ax.legend(lines, legends, loc='lower right')

    plt.tight_layout()
    plt.savefig(filepath)
    plt.show()

def plot_cumulative_distribution_weather(dfs, attribute, labels, ax, filepath):
    lines = []
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    markers = ['o', 'v', 's', 'P', '*', '+', 'x']

    for df, label in zip(dfs, labels):
        weather_conditions = df['Weather_type'].unique()
        for j, weather in enumerate(weather_conditions):
            data = df[df['Weather_type'] == weather][attribute]
            x, y = calculate_cumulative_distribution(data)

            color = colors[j % len(colors)]
            marker = markers[j % len(markers)]
            line, = ax.plot(x, y, color=color, marker=marker, label=f"{label} ({weather})")
            lines.append(line)

    ax.set_xlabel(f'{attribute.capitalize()}')
    ax.set_ylabel('Cumulative Distribution [%]')
    ax.grid(True)
    ax.legend()
    plt.tight_layout()
    plt.savefig(filepath)
    plt.show()
