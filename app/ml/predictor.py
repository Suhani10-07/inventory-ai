import numpy as np

def moving_average_prediction(sales_history, window=3):
    if len(sales_history) < window:
        return sum(sales_history) / len(sales_history)

    return np.mean(sales_history[-window:])