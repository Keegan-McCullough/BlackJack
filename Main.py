from BlackJack_Rule_Set import games
import random

# Testing betting strategies

keys = []
values = []
results_dict = {}
bank_size = 800
for bet_size in range(5,100,5):
    for s in range(20, 40):
        stop = s*bank_size/10
        r_win_rate, h_win_rate = games(100,bank_size,bet_size,stop)
        r_total = 0
        h_total = 0
        r_wins = 0
        h_wins = 0
        for value in r_win_rate:
            r_total = r_total + (int(value) - bank_size)
            if int(value) > 0:
                r_wins+=1
        for value in h_win_rate:
            h_total = h_total + (int(value) - bank_size)
            if int(value) > 0:
                h_wins+=1
        keys.append('Bet:' + str(bet_size)+ ', Bank:' + str(bank_size)+ ', Stop:' + str(stop))
        values.append((r_wins/1, h_wins/1, h_total, r_total))

for i, key in enumerate(keys):
    results_dict[key] = values[i]

print("Most Amount of wins combo real then hypothetical")
max_key1 = max(results_dict, key=lambda k: results_dict[k])
r_maximum_wins = results_dict[max_key1]
print(str(max_key1) + ' with ' + str(r_maximum_wins[0]) + '% wins')
max_key1 = max(results_dict, key=lambda k: results_dict[k][1])
h_maximum_wins = results_dict[max_key1]
print(str(max_key1) + ' with ' + str(h_maximum_wins[0]) + '% wins')

print('')
print("Most amount of hypothetical gain")
max_key2 = max(results_dict, key=lambda k: results_dict[k][2])
print(max_key2)
print("Most amount of real gain")
max_key3 = max(results_dict, key=lambda k: results_dict[k][3])
print(max_key3)
