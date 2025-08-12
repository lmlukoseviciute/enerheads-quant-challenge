def get_season(month):
    if month in [12, 1, 2]:
        return "winter"
    elif month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    else:
        return "autumn"

def get_time_of_day(hour):
    if 6 <= hour < 12:
        return "morning"
    elif 12 <= hour < 18:
        return "afternoon"
    elif 18 <= hour < 24:
        return "evening"
    else:
        return "night"

def label_spike(x):
    if x > mean_val + std_val:
        return 1
    elif x < mean_val - std_val:
        return 1
    else:
        return 0 


def weighted_mae(y_true, y_pred, spike_weight=1000):
    mean_val = np.mean(y_true)
    std_val = np.std(y_true)

    # Identify spike indices
    spike_mask = (y_true > mean_val + std_val) | (y_true < mean_val - std_val)

    errors = np.abs(y_true - y_pred)

    # Increase weight on spike errors
    errors[spike_mask] *= spike_weight

    return np.mean(errors)


def spike_accuracy_scorer(estimator, X, y_true, tol=0.1):
    y_pred = estimator.predict(X)
    
    mean_val = np.mean(y_true)
    std_val = np.std(y_true)

    true_spikes_idx = np.where((y_true > mean_val + std_val) | (y_true < mean_val - std_val))[0]
    pred_spikes_idx = np.where((y_pred > mean_val + std_val) | (y_pred < mean_val - std_val))[0]

    common_spikes_idx = np.intersect1d(true_spikes_idx, pred_spikes_idx)
    
    if len(true_spikes_idx) == 0:
        return 1.0  
    
    correct_spikes = 0
    for idx in common_spikes_idx:
        true_val = y_true[idx]
        pred_val = y_pred[idx]
        if abs(pred_val - true_val) <= tol * abs(true_val):
            correct_spikes += 1
    
    spike_accuracy = correct_spikes / len(true_spikes_idx)
    return spike_accuracy