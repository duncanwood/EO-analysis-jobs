import matplotlib.pyplot as plt
import pandas as pd
import lsst.eotest.image_utils as imutils

__all__ = ['plot_fe55_raft_gains']

channel = {i: f'C{_}' for i, _ in imutils.channelIds.items()}

def plot_fe55_raft_gains(raft_files, y_range=(1, 1.6), figsize=(12, 12)):
    """
    Plot Fe55 gains for all amps for each CCD in a raft.

    Parameters
    ----------
    raft_files: list
        A list of pickle files containing pandas data frames with
        the gains for each amp in a CCD as a function of MJD.
        The filenames are assumed to be of the form
        '<raft>_<sensor>_<run>_gain_sequence.pickle`, so that the
        detector name (e.g., 'R22_S11'), raft, and run number can
        be extracted.
    y_range: (float, float) [(1, 1.6)]
        Plotting limts of the y-axis for each plot.
    figsize: (float, float) [(12, 12)]
        Size of the figure for each raft.
    """
    plt.figure(figsize=figsize)
    for i, item in enumerate(raft_files, 1):
        plt.subplot(3, 3, i)
        df = pd.read_pickle(item)
        mjd0 = int(min(df['mjd']))
        det_name = os.path.basename(item)[:len('R22_S11')]
        amps = sorted(list(set(df['amp'])))
        for amp in amps:
            my_df = df.query(f'amp == {amp}')
            plt.scatter(24*(my_df['mjd'] - mjd0), my_df['gain'], s=2,
                        label=f'{channel[amp]}')
        plt.legend(fontsize='x-small', ncol=2)
        plt.ylim(*y_range)
        plt.title(det_name, fontsize='x-small')
        plt.xlabel(f'24*(MJD - {mjd0:d})')
        plt.ylabel('gain (e-/ADU)')
    plt.tight_layout(rect=(0, 0, 1, 0.95))
    tokens = os.path.basename(item).split('_')
    run = tokens[2]
    raft = tokens[0]
    plt.suptitle(f'Fe55 gain stability, {raft}, Run {run}')
    plt.savefig(f'{raft}_{run}_fe55_gain_stability.png')
