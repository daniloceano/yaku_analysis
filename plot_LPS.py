# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    plot_LPS.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: daniloceano <danilo.oceano@gmail.com>      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/18 15:02:59 by daniloceano       #+#    #+#              #
#    Updated: 2024/04/18 15:41:30 by daniloceano      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import pandas as pd
import matplotlib.pyplot as plt
from lorenz_phase_space.phase_diagrams import Visualizer

# Read periods data
df_energetics = pd.read_csv("LEC_yaku_ERA5_choose/yaku_ERA5_choose_results.csv", index_col=0)
df_periods = pd.read_csv("periods_yaku.csv", index_col=0)

figures_directory = "figures"
os.makedirs(figures_directory, exist_ok=True)

for plot_periods in (False, True):
    for adjust in (0.05, 0.5):

        if plot_periods:
            # Create a new DataFrame to store the means
            df = pd.DataFrame(index=df_periods.index, columns=df_energetics.columns)
            # Compute means for each period
            for idx, period in df_periods.iterrows():
                start, end = period['start'], period['end']
                period_data = df_energetics.loc[start:end]
                df.loc[idx] = period_data.mean()  
            # Use the new DataFrame
            df.index = range(len(df))
            # Adjust figure name
            plot_filename = f"LPS_periods_yaku_adjust_{adjust}.png"
        
        else:
            df = df_energetics
            plot_filename = f"LPS_yaku_adjust_{adjust}.png"

        # Initialize the Lorenz Phase Space plotter
        lps = Visualizer(
                LPS_type='mixed',
                zoom=True,
                x_limits=[df['Ck'].min() - adjust, df['Ck'].max() + adjust],
                y_limits=[df['Ca'].min() - adjust, df['Ca'].max() + adjust],
                color_limits=[df['Ge'].min() - adjust, df['Ge'].max() + adjust],
                marker_limits=[df['Ke'].min() - adjust, df['Ke'].max() + adjust],
            )

        # Generate the phase diagram
        lps.plot_data(
            x_axis=df['Ck'].tolist(),
            y_axis=df['Ca'].tolist(),
            marker_color=df['Ge'].tolist(),
            marker_size=df['Ke'].tolist(),
        )

        # Save the final plot
        figure_path = os.path.join(figures_directory, plot_filename)
        plt.savefig(figure_path)
        print(f"Figure saved to: {figure_path}")
