import numpy as np
from scipy.interpolate import interp1d

def load_lip_sync_data(file_path):
    """
    Load lip sync data from a file.
    The file should contain timestamps and corresponding mouth shape indices.
    Expected format: timestamp<TAB>shape_index (one per line)
    """
    data = {}
    with open(file_path, 'r') as file:
        for line in file:
            timestamp, shape_index = line.strip().split('\t')
            data[float(timestamp)] = int(shape_index)
    return data

def interpolate_data(reference_timestamps, data):
    """
    Interpolates test data to match reference timestamps using previous interpolation.
    """
    sorted_timestamps = sorted(data.keys())
    sorted_values = [data[t] for t in sorted_timestamps]
    
    interpolation_func = interp1d(sorted_timestamps, sorted_values, kind='previous', fill_value='extrapolate')
    interpolated_values = interpolation_func(reference_timestamps)
    
    return np.round(interpolated_values).astype(int)

def compute_adjusted_accuracy(base_labels, test_labels):
    """
    Compute adjusted accuracy where slight differences are partially credited.
    """
    differences = np.abs(base_labels - test_labels)
    
    scores = np.where(differences == 0, 1.0,  # Exact match
              np.where(differences == 1, 0.9,  # Slight mismatch
              np.where(differences == 2, 0.7,  # Moderate mismatch
              np.where(differences == 3, 0.5,  # Larger mismatch
              0.0))))  # Significant mismatch
    
    accuracy = np.mean(scores) * 100  # Convert to percentage
    return accuracy

def main():
    # Load lip sync results
    cherry_data = load_lip_sync_data("/Users/seherova/Documents/fonemlerveses/changed_dropout_parameter/V0_ch_dropout_catched_pattern_txt")  # AI-based model
    tapir_data = load_lip_sync_data("/Users/seherova/Documents/projectss/speech-lip sync-sync/cherry-lip-sync/v04_cherry_ve_LipSync/tapir_LipSync_V04.txt")    # Signal processing model
    
    # Reference timestamps from Cherry (AI-based model)
    reference_timestamps = sorted(cherry_data.keys())
    
    # Interpolate Tapir data to match Cherry's timestamps
    tapir_interpolated = interpolate_data(reference_timestamps, tapir_data)
    cherry_values = np.array([cherry_data[t] for t in reference_timestamps])
    
    # Compute correctness using adjusted accuracy
    correctness = compute_adjusted_accuracy(cherry_values, tapir_interpolated)
    print(f"Tapir Lip Sync correctness compared to Cherry Lip Sync: {correctness:.2f}%")

if __name__ == "__main__":
    main()
