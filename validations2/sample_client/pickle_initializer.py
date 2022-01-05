import pickle


def initial_pickle():
    l = [0, 0, 0, 0, 0]
    with open('gems.txt', 'wb') as fp:
        pickle.dump(l, fp)
