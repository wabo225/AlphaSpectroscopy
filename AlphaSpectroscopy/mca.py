import numpy as np

def extract_data(filename: str) -> dict:
    with open(filename) as f:
        f.readline()
        f.readline()
        for i in range(5):
            f.readline()
        date = f.readline()
        f.readline()
        meas_time, meas_live = f.readline().split()
        f.readline()
        shape = f.readline().split()
        data = [int(f.readline()) for i in range(int(shape[1]))]
        data[0:8] = [0,0,0,0,0,0,0,0]
    
    return {
        'date': date,
        'meas_time': int(meas_time),
        'meas_live': int(meas_live),
        'data': np.array(data)
    }

if __name__ == "__main__":
    filename = 'spectrum7.Spe'
    data = extract_data(filename)
    
    
