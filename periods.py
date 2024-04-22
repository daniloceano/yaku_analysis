# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    periods.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: daniloceano <danilo.oceano@gmail.com>      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/18 15:02:44 by daniloceano       #+#    #+#              #
#    Updated: 2024/04/19 10:37:54 by daniloceano      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os 
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator

from cyclophaser import determine_periods
from cyclophaser.determine_periods import periods_to_dict, process_vorticity

def plot_all_periods(phases_dict, ax, vorticity):
    colors_phases = {'incipient': '#65a1e6',
                      'intensification': '#f7b538',
                        'mature': '#d62828',
                          'decay': '#9aa981',
                          'residual': 'gray'}

    ax.plot(vorticity.time, vorticity.zeta, linewidth=10, color='gray', alpha=0.8, label=r'ζ')

    if len(vorticity.time) < 50:
        dt = pd.Timedelta(1, unit='h')
    else:
       dt = pd.Timedelta(0, unit='h')

    legend_added = set()  # This set will track which phases have been added to the legend

    # Shade the areas between the beginning and end of each period
    for phase, (start, end) in phases_dict.items():
        # Extract the base phase name (without suffix)
        base_phase = phase.split()[0]

        # Access the color based on the base phase name
        color = colors_phases[base_phase]

        # Fill between the start and end indices with the corresponding color
        ax.fill_between(vorticity.time, vorticity.zeta.values,
                        where=(vorticity.time >= start) & (vorticity.time <= end + dt),
                        alpha=0.5, color=color, label=base_phase if base_phase not in legend_added else "")
        
        # Mark this phase as added to avoid adding it again to the legend
        legend_added.add(base_phase)

    ax.ticklabel_format(axis='y', style='sci', scilimits=(-3, 3))
    date_format = mdates.DateFormatter("%Y-%m-%d")
    ax.xaxis.set_major_formatter(date_format)
    ax.set_xlim(vorticity.time.min(), vorticity.time.max())
    ax.set_ylim(vorticity.zeta.min() - 0.25e-5, 0)

    ax2 = ax.twinx()
    ax2.plot(vorticity.time, vorticity.vorticity_smoothed, linewidth=6,
             c='#1d3557', alpha=0.8, label=r'$ζ_{fs}$')
    ax2.plot(vorticity.time, vorticity.vorticity_smoothed2, linewidth=3,
             c='#e63946', alpha=0.6, label=r'$ζ_{fs^{2}}$')
    
    ax2.legend(loc='upper right', bbox_to_anchor=(1, 0.15), fontsize=14)

    # Add this line to set x-tick locator
    ax.xaxis.set_major_locator(MaxNLocator(nbins=6))  

    plt.setp(ax.get_xticklabels(), rotation=45, ha='right', fontsize=12)
    plt.setp(ax.get_yticklabels(), fontsize=12)


track_file = "./LEC_yaku-resampled_ERA5_track/yaku-resampled_ERA5_track_trackfile"
track = pd.read_csv(track_file, sep=";")
track['time'] = pd.to_datetime(track['time'], format="%Y-%m-%d-%H%M")
track.set_index('time', inplace=True)
track.rename(columns={'min_max_zeta_850':'zeta'}, inplace=True)

process_vorticity_args = {
    "use_filter": len(track) // 4,
    "use_smoothing": len(track) // 5 | 1,
    "use_smoothing_twice": len(track) // 5 | 1,
}

periods_args = {'threshold_incipient_length': 0}

figures_directory = "figures"
os.makedirs(figures_directory, exist_ok=True)   

df_periods = determine_periods(track['zeta'].tolist(),
                               x=track.index, 
                               plot=f"{figures_directory}/periods_yaku.png",
                               plot_steps=f"{figures_directory}/periods_yaku_steps.png",
                               export_dict="periods_yaku",
                               process_vorticity_args=process_vorticity_args,
                               periods_args=periods_args)

vorticity = process_vorticity(track)
periods_dict = periods_to_dict(df_periods)

fig = plt.figure(figsize=(20, 10))
ax = fig.add_subplot(1, 1, 1)
plot_all_periods(periods_dict, ax, vorticity)