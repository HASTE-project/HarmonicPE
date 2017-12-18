@staticmethod
def g2(result):
    # import features as f
    import time as t
    import numpy as np
    import scipy

    def burstiness(y):
        """
        % DN_Burstiness
        %
        % Returns the 'burstiness' statistic from:
        %
        % Goh and Barabasi, 'Burstiness and memory in complex systems' Europhys. Lett.
        % 81, 48002 (2008)
        %
        % INPUTS:
        % y, the input time series """

        return (np.std(y) - np.mean(y)) / (np.std(y) + np.mean(y))

    def skewness(y):
        """
        % Estimates custom skewness measures, the Pearson skewnesses.
        %
        % INPUTS:
        % y, the input time series """

        return (3 * np.mean(y) - np.median(y)) / np.std(y)

    def CV(x, k=1):
        """
        % Calculates the coefficient of variation, sigma^k / mu^k, of order k
        %
        % INPUTS:
        %
        % x, the input time series
        %
        % k, the order of coefficient of variation (k = 1 is usual) """

        return (np.std(x)) ** k / (np.mean(x)) ** k

    def autocorrelations(y, k=10):
        """
        % Computes the autocorrelation of an input time series, y, at a time-lag up to k
        %
        % INPUTS:
        % y, a scalar time series column vector
        %
        % Output is the autocorrelation for every time lag as an array """

        N = len(y)
        return [np.sum(
            (y[0:N - i] - np.mean(y[0:N - i])) * (y[i:N] - np.mean(y[i:N])) / N / np.std(y[0:N - i]) / np.std(
                y[i:N])) for i in range(1, k)]

    def check_if_zero(v):
        if np.count_nonzero(v) == 0:
            return True
        else:
            return False

    def check_arrays(data):
        a_len = data.shape[1]
        t_data = []
        for i, a in enumerate(data):
            if np.count_nonzero(a) == 0:
                idx = np.random.randint(0, a_len)
                a[idx] = 1
                data[i] = a
        return data

    def fft_norm(x):
        # remove dc bias
        x -= np.mean(x)
        return np.linalg.norm(abs(np.fft.fft(x)))

    t0 = t.time()

    mapped = {}

    parameters = result.model.get_all_parameters()
    mapped['parameters'] = zip(parameters.keys(), (v.expression for v in parameters.values()))
    mapped['D'] = result.model.get_species('mRNA').diffusion_constant
    # mapped['tspan'] = result.model.tspan

    result_species = []
    for species in result.model.get_all_species():
        if species == 'protein' or species == 'mRNA':
            # get result
            matrix = result.get_species(species)

            # Check for zero vectors and replace one random element to 1
            matrix = check_arrays(matrix)

            # Transpose the result, should make this matrix.T
            matrixT = np.asarray([list(matrix[:, i]) for i in range(matrix.shape[1])])

            matrixT = check_arrays(matrixT)

            result_species.append((matrix, matrixT))

    # Sums all CP in each snapshot(m) and per voxel(mT)
    total_sum = []
    for m, mT in result_species:
        m_sum = [np.sum(v) for v in m]
        mt_sum = [np.sum(v) for v in mT]
        # total_sum.append((scipy.signal.savgol_filter(m_sum, 51, 3), scipy.signal.savgol_filter(m_sum, 51, 3)))
        total_sum.append((m_sum, mt_sum))
    # feature vector
    f_vector = []

    # Total CP
    for c, (Sm, SmT) in enumerate(total_sum):
        f_vector.append(np.mean(Sm))
        f_vector.append(burstiness(Sm))
        f_vector.append(burstiness(SmT))
        f_vector.append(skewness(Sm))
        # f_vector.append(skewness(SmT)) remove
        f_vector.append(CV(Sm, 1))
        f_vector.append(CV(SmT, 1))
        f_vector.append(np.linalg.norm(autocorrelations(Sm, len(Sm) / 2)))
        # f_vector.append(np.linalg.norm(autocorrelations(SmT,len(SmT)/2))) remove
        f_vector.append(fft_norm(Sm))
        f_vector.append(fft_norm(SmT))
        if c < len(total_sum) - 1:  ### CHECK IF IT'S CORRECT! 03/18
            for i in range(1, len(total_sum) - c):
                # Correlations of total CP in volume
                f_vector.append(np.corrcoef(Sm, total_sum[c + i][0])[0][1])
                # f_vector.append(np.corrcoef(SmT,total_sum[c+i][1])[0][1]) remove

    for c, (m, mT) in enumerate(result_species):
        bm, bmT, sm, smT, CVm, CVmT, ACm, ACmT = [], [], [], [], [], [], [], []
        for v in m:
            bm.append(burstiness(v))
            sm.append(skewness(v))
            CVm.append(CV(v, 1))
            # ACm.append(numpy.linalg.norm(f.autocorrelations(v, len(v)/2)))
        for v in mT:
            bmT.append(burstiness(v))
            smT.append(skewness(v))
            CVmT.append(CV(v, 1))
            # ACmT.append(numpy.linalg.norm(f.autocorrelations(v, len(v)/2)))
        if c < len(result_species):
            for i in range(1, len(result_species) - c):
                nm, nmT = result_species[c + i]
                corr1 = [np.corrcoef(v, nm[e])[0][1] for e, v in enumerate(m)]
                corr2 = [np.corrcoef(v, nmT[e])[0][1] for e, v in enumerate(mT)]
                f_vector.append(np.linalg.norm(corr1))
                f_vector.append(np.linalg.norm(corr2))
                f_vector.append(np.var(corr1))
                f_vector.append(np.var(corr2))

        for var in [bm, bmT, sm, smT, CVm, CVmT]:
            f_vector.append(np.linalg.norm(var))
            f_vector.append(np.mean(var))
            f_vector.append(np.var(var))

    mapped['features'] = f_vector

    mapped['time for mapper (s)'] = t.time() - t0

    return mapped

