import pickle

with open("test_hw_01_winversion.ini.pkl", 'rb') as f:
    data = pickle.load(f)

for line in data:
    print(line)
