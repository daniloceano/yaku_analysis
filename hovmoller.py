# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    hovmoller.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: daniloceano <danilo.oceano@gmail.com>      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/18 16:02:31 by daniloceano       #+#    #+#              #
#    Updated: 2024/04/19 10:27:16 by daniloceano      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.colors as colors
import cmocean as cmo

# Load the data
results_file = "LEC_yaku-resampled_ERA5_track/Ge_level.csv"
df = pd.read_csv(results_file)

# Convert 'time' column to datetime and set as index
df['time'] = pd.to_datetime(df['time'])
df.set_index('time', inplace=True)

# Select the columns for the Hovmöller diagram (assuming all except 'time')
data = df.iloc[:, 1:].transpose()  # Transpose so that columns become levels and rows become time

# Prepare the plot
fig, ax = plt.subplots(figsize=(12, 6))

# Normalize the data limits for the colorbar
imin = data.min(numeric_only=True).min()
imax = data.max(numeric_only=True).max()
absmax = np.amax([np.abs(imin), imax])
norm = colors.TwoSlopeNorm(vcenter=0, vmin=-absmax * 0.8, vmax=absmax * 0.8)

levels = np.linspace(-absmax, absmax, 10)

# Create the Hovmöller diagram
c = ax.contourf(df.index, data.index.astype(float), data, cmap=cmo.cm.balance,
                norm=norm, levels=levels, extend='both')
# ct = ax.contour(df.index, data.index.astype(float), data, colors='k', linewidths=0.5)

# Set the format of the date on the x-axis
ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))  # adjust interval as needed
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

ax.invert_yaxis()

# Adding color bar
plt.colorbar(c, ax=ax, label='Values')

# Labels and title
ax.set_title('Hovmöller Diagram')
ax.set_xlabel('Time')
ax.set_ylabel('Pressure Level (Pa)')  # assuming units are in Pascal, adjust as necessary

plt.xticks(rotation=45)
plt.tight_layout()

figures_directory = "figures"
os.makedirs(figures_directory, exist_ok=True)
figure_path = os.path.join(figures_directory, "hovmoller_Ge.png")
plt.savefig(figure_path)
print(f"Figure saved to: {figure_path}")
