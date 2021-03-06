import numpy as np
import matplotlib.pylab as plt
import pandas as pd
class Metrics():
    def __init__(self, y=None, ypred=None):
        self.y = y
        self.ypred = ypred


    def accuracy(self, y, ypred):
        """
        Measures the number of correctly
        classified classes
        param: y: correct labels
        type: y: ndarray
        param: y_pred: predicted labels
        type: y_pred: ndarray
        return: accuracy
        """
        cls_pred = np.argmax(ypred, axis=1)
        acc = 100.0/y.shape[0]*np.sum(cls_pred == y)
        self.acc = acc
        return acc


    def gain_chart(self, threshold = 0.5, plot = True):
        """
        Creates a gains chart for the predicted y-values
        when classifying a binary variable. Predicted y-values
        are given as a percent confidence of which class it
        belongs to. The percent over the given threshold is
        predicted as class 1 and everything under is given
        as class 2.

        param: y: correct label
        type: y: ndarray
        param: ypred: Predicted labels given in percent confidence
        type: ypred: ndarray
        param: threshold: number [0,1] desciding the threshold
        between the classes
        type: threshold: float
        return: None
        """
        y = self.y
        ypred = self.ypred

        num1 = np.sum(y)
        frac1 = num1/y.shape[0]
        sort = np.argsort(ypred[:, -1])
        lab_sort = y[sort[::-1]]

        fracs = np.arange(0, 1.01, 0.01)
        gains = np.zeros(len(fracs))

        for i in range(len(fracs)):
            lab_frac = lab_sort[:int(fracs[i]*y.shape[0])]
            gains[i] = np.sum(lab_frac)/num1

        def best(x):
            if x < frac1:
                return x/frac1
            else:
                return 1
        besty = np.zeros_like(fracs)
        for i in range(len(besty)):
            besty[i] = best(fracs[i])

        area_best = np.trapz(besty - fracs, fracs)
        area_model = np.trapz(gains - fracs, fracs)
        ratio = area_model/area_best
        self.gain_params = [fracs, gains, besty]
        self.gain_dict = {'fracs': fracs, 'gains':gains, 'besty':besty, 'ratio':ratio}
        self.ratio = ratio
        if plot:
            self.plot_gains(*self.gain_params)
        return ratio

    def plot_gains(self, fracs, gains, besty, ratio):
        plt.plot(fracs, gains, label='Lift Curve')
        plt.plot(fracs, fracs, '--', label='Baseline')
        plt.plot(fracs, besty, '--', label='Best Curve')
        plt.plot([], [], ' ', label='Area ratio: %.4f' % ratio)
        plt.xlabel('Fraction of total data', fontsize=14)
        plt.ylabel('Cumulative number of target data', fontsize=14)
        plt.grid(True)
        plt.legend()
        plt.show()

    def prob_acc(self, n = 50, plot = True):
        y = self.y
        ypred = self.ypred

        sort = np.argsort(ypred[:, -1])
        pred_sort = ypred[sort[::-1]]
        lab_sort = y[sort[::-1]]

        P = np.zeros((y.shape[0] - 2*n))

        for i in range(len(P)):
            P[i] = np.sum(lab_sort[n + i: 3*n + i +1])/(2*n +1)

        pred_plt = pred_sort[n:-n, -1]

        ## DO LINREG
        from sklearn.linear_model import LinearRegression
        reg = LinearRegression().fit(pred_plt.reshape(-1, 1),P)
        b = reg.intercept_
        a = reg.coef_[0]
        R2 = reg.score(pred_plt.reshape(-1,1), P)
        self.prob_params = [pred_plt, P, b, a]
        self.prob_dict = {'pred_plt':pred_plt, 'P':P, 'b': b, 'a':a, 'R2':R2}
        self.R2 = R2
        if plot:
            self.plot_acc(*self.prob_params)
        return R2

    def plot_acc(self, pred_plt, P, b, a, R2):
        plt.plot(pred_plt, P, 'o', markersize=0.8)
        plt.plot(pred_plt, b + pred_plt*a, label="y = %.3fx + %.3f\n R2 = %.4f" %(a, b,R2))
        plt.xlim([0, 1])
        plt.ylim([0, 1])
        plt.xlabel("Predicted probability", fontsize=14)
        plt.ylabel("Actual probability", fontsize=14)
        plt.grid(True)
        plt.legend()
        plt.show()

    def save_metrics(self, path_to_dir: str, filename: str):
        file_dict = {**self.gain_dict, **self.prob_dict}
        df_gain = pd.DataFrame(data=self.gain_dict)
        df_prob = pd.DataFrame(data=self.prob_dict)
         
        df_gain.to_csv(path_to_dir+filename+'gain.csv')
        df_prob.to_csv(path_to_dir+filename+'prob.csv')
