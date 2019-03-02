import pandas as pd
import scipy.signal as sp
import numpy as np
import matplotlib.pyplot as plt

col_name = 'EMG1'
column = []


def get_column():
    global column
    path = 'training_data/test/record1/emg1.csv'
    df = pd.read_csv(path)
    saved_column = df[col_name]
    column = saved_column.values


def plot1(array, title):
    t = np.arange(0, array.__len__(), 1)
    plt.figure()
    plt.title(title)
    plt.plot(t, array)


def plot2(array1, array2, name1, name2, title):
    try:
        t = np.arange(0, array1.__len__(), 1)
        plt.figure()
        plt.title(title)
        plt.plot(t, array1, label=name1)
        plt.plot(t, array2, label=name2)
        plt.legend()
    except:
        print("Error in plot2 --> "
              "'array1 = " + str(array1.__len__()) +
              "' and 'array2 = " + str(array2.__len__()) +
              "' should be same length")


def draw_decimate_fir():
    out = sp.decimate(column, 4, None, 'fir', -1, True)
    plot1(out, "Decimate FIR")
    print("decimate FIR", out.__len__())
    return out


def draw_decimate_iir():
    out = sp.decimate(column, 4, None, 'iir', -1, True)
    plot1(out, "Decimate IIR")
    print("decimate IIR ", out.__len__())
    return out


def draw_original():
    plot1(column, "Original")


def draw_original_and_decimate(o, d):
    new_decimate = []
    for i in range(0, d.__len__()):
        if i != 0:
            new_decimate = np.append(new_decimate, [0, 0, 0])
        new_decimate = np.append(new_decimate, d[i])
    # print("new decimate ", new_decimate)
    # print("new decimate", new_decimate.__len__())
    plot2(o, new_decimate, "Original signal", "Decimate signal", "Original and Decimate")


def draw_avg():
    avg = []
    sum = 0
    for i in range(0, column.__len__()):
        if i % 4 == 0 and i != 0:
            avg = np.append(avg, sum/4)
            sum = 0
            sum = sum + column[i]
        else:
            sum = sum + column[i]
    # print("original ", column)
    # print("avg ", avg)
    # print("avg", avg.__len__())
    plot1(avg, "Average")
    return avg


def draw_original_and_avg(o, a):
    avg = []
    for i in range(0, a.__len__()):
        if i != 0:
            avg = np.append(avg, [0, 0, 0])
        avg = np.append(avg, a[i])
    # print("avg ", a)
    # print("new avg ", avg)
    plot2(o, avg, "Original signal", "Decimate signal", "Original and Average")


def main():
    get_column()
    # print("original", column.__len__())
    down_sampling1 = draw_decimate_fir()
    # down_sampling2 = draw_decimate_iir()
    # plot2(down_sampling1, down_sampling2, "FIR output", "IIR output", "Decimate FIR and IIR")
    draw_original()
    # draw_original_and_decimate(column, down_sampling)
    # average = draw_avg()
    # draw_original_and_avg(column, average)
    plt.show()


if __name__ == '__main__':
    main()
