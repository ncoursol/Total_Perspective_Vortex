try:
    import numpy as np
    import pandas as pd
    import joblib
    import timeit
    import mne
    import os
    from mne.channels import make_standard_montage
    from mne.datasets import eegbci
    from mne.io import concatenate_raws, read_raw_edf
    from sklearn.model_selection import ShuffleSplit, cross_val_score, train_test_split
    from sklearn.pipeline import Pipeline
    from ft_csp import ft_CSP
    from ft_knn import ft_KNN
    from utils import parse_arguments, display_build, experiments
except:
    print('try pip install -r requirements.txt')
    exit(0)

def set_epochs_filter(raw_filt):
    picks = mne.pick_types(raw_filt.info, eeg=True, exclude='bads')
    events, event_id = mne.events_from_annotations(raw_filt, dict(T1=0, T2=1))
    epochs = mne.Epochs(raw_filt, events, event_id, tmin=-1, tmax=4, proj=True, picks=picks, preload=True)
    labels = epochs.events[:, -1]
    return epochs, labels

def pipeline(X_train, y_train):
    ft_csp = ft_CSP(n_components=5, log=True)
    clf = ft_KNN()
    model = Pipeline([('CSP', ft_csp), ('KNN', clf)]).fit(X_train, y_train)
    return model

def train():
    model = pipeline(X_train, y_train)
    scores = cross_val_score(model, X_train, y_train, cv=cv)
    print(f'{txt} {task + (0 if args.runs is not None else 1)}: subject {subject}: accuracy = {np.mean(scores):.2%}')
    train_scores[i][j] = np.mean(scores)
    if os.path.isfile(file):
        os.remove(file)
    joblib.dump(model, file)

def predict():
    model = joblib.load(file)
    accuracy = model.score(X_test, y_test)
    if len(tasks) == 1 and len(args.subjects) == 1:
        d = np.stack((y_test, model.predict(X_test), y_test == model.predict(X_test)), axis=1)
        res = pd.DataFrame(data=d, columns=['[prediction]', '[truth]', 'equal?'])
        print(res)
    elapsed = timeit.default_timer() - start_time
    print(f'{txt} {task + (0 if args.runs is not None else 1)}: subject {subject}: accuracy = {np.mean(accuracy):.2%} - elapsed = {elapsed:.2}s')
    predict_scores[i][j] = np.mean(accuracy)

if __name__ == "__main__":
    args = parse_arguments(0)
    tasks = args.runs if args.runs is not None else args.tasks
    txt = 'run' if args.runs is not None else 'task'
    train_scores = np.zeros((len(tasks), len(args.subjects)))
    predict_scores = np.zeros((len(tasks), len(args.subjects)))

    montage = make_standard_montage('biosemi64')
    cv = ShuffleSplit(10, test_size=0.2, random_state=42)
    for i, task in enumerate(tasks):
        exp = task if args.runs is not None else experiments[task]['tasks']
        for j, subject in enumerate(args.subjects):
            raw_subject = eegbci.load_data(subject, exp, os.getenv('HOME') + '/sgoinfre')
            start_time = timeit.default_timer()
            raw = concatenate_raws([read_raw_edf(r, preload=True) for r in raw_subject])
            raw.load_data()
            eegbci.standardize(raw)

            raw.drop_channels(['T9', 'T10'])
            raw.set_montage(montage)

            raw_filt = raw.copy().filter(l_freq=7.0, h_freq=30.0)
            epochs, labels = set_epochs_filter(raw_filt)
            display_build(args.verbose, raw, raw_filt, montage)

            X = epochs.crop(tmin=1.0, tmax=2.0).get_data()
            y = labels
            result_history = np.zeros((int(X.shape[0]), 2))
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)

            file = f"weights/S{subject}{'T' if args.runs is None else 'R'}{task}.pk1"
            if args.predict:
                if not os.path.isfile(file):
                    print(f"Skipped S{subject}R{task}: weights missing")
                    continue
                predict()
            else:
                train()

    print(end='\n')
        
    if len(tasks) > 1:
        for i, task in enumerate(tasks):
            print(f'{txt} {task}: mean accuracy = {np.mean(predict_scores[i] if args.predict else train_scores[i]):.2%}')
    print(f'Mean accuracy of all {txt}s: {np.mean(predict_scores if args.predict else train_scores):.2%}')