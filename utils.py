try:
    import argparse
    import mne
    import matplotlib.pyplot as plt
except:
    print('try pip install -r requirements.txt')
    exit(0)

experiments = [
    {"desc": "Motor execution: left vs right hand", "tasks": [3, 7, 11]},
    {"desc": "Motor imagery: left vs right hand", "tasks": [4, 8, 12]},
    {"desc": "Motor execution: hands vs feet", "tasks": [5, 9, 13]},
    {"desc": "Motor imagery: hands vs feet", "tasks": [6, 10, 14]},
    {"desc": "Motor execution/imagery: left vs right hand", "tasks": [3, 7, 11, 4, 8, 12]},
    {"desc": "Motor execution/imagery: hands vs feet", "tasks": [5, 9, 13, 6, 10, 14]},
]

def parse_inputs(args):
    if (args.runs is None and args.tasks is None) or args.tasks == []:
        args.tasks = list(range(1, 7))
    if args.runs == []:
        args.runs = list(range(3, 15))
    if not args.subjects:
        args.subjects = list(range(1, 110))
    if args.verbose == []:
        args.verbose = ['montage', 'filter', 'graph']
    if 'mne' not in args.verbose:
        mne.set_log_level(verbose='ERROR')
    if args.tasks:
        args.tasks = [x - 1 for x in args.tasks]
    if not all((x > 0 and x < 110) for x in args.subjects):
        print('Bad subject number (1-109)')
        exit(0)
    if args.tasks and not all((x >= 0 and x < 6) for x in args.tasks):
        print('Bad task index (1-6)')
        exit(0)
    if args.runs and not all((x > 2 and x < 15) for x in args.runs):
        print('Bad run number (3-14)')
        exit(0)

def parse_arguments(ex):
    help_tasks = "List of tasks to train where:\n"
    for x, _ in enumerate(experiments):
        help_tasks += str(x + 1) + ' : ' + experiments[x]['desc'] + ' - ' + str(experiments[x]['tasks']) + '\n'
    parser = argparse.ArgumentParser(description="Total Perspective Vortex", formatter_class=argparse.RawTextHelpFormatter, prog='PROG')
    group = parser.add_mutually_exclusive_group()
    parser.add_argument('-p', '--predict', action='store_true', default=False, help="Perform prediction mode")
    parser.add_argument('-s', '--subjects', action='store', type=int, nargs='*', default=None, help="List of subjects to train")
    group.add_argument('-r', '--runs', action='store', type=int, nargs='*', default=None, help="List of runs to train")
    group.add_argument('-t', '--tasks', action='store', type=int, nargs='*', default=None, help=help_tasks)
    parser.add_argument('-v', '--verbose', nargs='*', default=['None'],
                        help="Display graphs where:\n"
                        "montage : electrodes montage\n"
                        "filter : filter graph before/after\n"
                        "graph : data, before and after filering\n"
                        "mne : display all mne function log")
    args = parser.parse_args()
    parse_inputs(args)
    return (args)

def display_build(state, raw, raw_filt, montage):
    if 'montage' in state:
        montage.plot()
        montage.plot(kind='3d')
        plt.show()
    if 'filter' in state:
        raw.compute_psd(fmax=80).plot()
        raw_filt.compute_psd(fmax=80).plot()
        plt.show()
    if 'graph' in state:
        mne.viz.plot_raw(raw, scalings={"eeg": 75e-6})
        mne.viz.plot_raw(raw_filt, scalings={"eeg": 75e-6})
        plt.show()