from random import choice

percent = range(100)
styles_on_banner = 2
must_have_styles = 0
minimum_styles_to_get = 1
sim_runs = 10**5

one_target = [3, [0], 1, 3, 150]
one_target_sa = [2, [0], 1, 3, 150]
one_target_plusBonus = [3, [0], 2, 3, 150]
two_targets = [3, [0, 1], 2, 3, 150]
three_targets = [3, [0, 1, 2], 3, 3, 150]
four_targets = [3, [0, 1, 2, 3], 4, 3, 150]


class StyleResult:
    def __init__(self, pulls: int, results: list):
        self.number_of_pulls = pulls
        self.result_list = results


def get_pull(smn_nbr, rank):
    n = choice(percent)
    if rank == 1:
        return n//3
    elif rank == 2:
        if smn_nbr % 10 == 0:
            return n//4
        else:
            return n//3
    elif rank == 3:
        return n


def run_sim(on_offer, must_gets, minimum_gets, rank=3, pityable=150):
    gets = []
    done = False
    num_pulls = 0
    pities = 0
    while not done:
        pull = get_pull(num_pulls, rank)
        if pull < on_offer and pull not in gets:
            gets.append(pull)
        num_pulls += 1
        if num_pulls % pityable == 0:
            pities += 1
        missing = [m for m in must_gets if m not in gets]
        if pities >= max(len(missing), minimum_gets - len(gets)):
            for p in range(pities):
                if all([m in gets for m in missing]):
                    unowned = [_ for _ in range(on_offer) if _ not in gets]
                    if unowned:
                        gets.append(min(unowned))
                else:
                    gets.append(min([m for m in missing if m not in gets]))
        if len(gets) >= minimum_gets and all([m in gets for m in must_gets]):
            done = True
    return StyleResult(num_pulls, gets)


def update_files(sim_runs):
    three_targets_file = 'data/three_targets.csv'
    two_targets_file = 'data/two_targets.csv'
    one_target_file = 'data/one_target.csv'
    one_target_sa_file = 'data/one_target_sa.csv'
    one_target_plusBonus_file = 'data/one_target_plusBonus.csv'
    update_data_file(three_targets_file, sim_runs, three_targets)
    update_data_file(two_targets_file, sim_runs, two_targets)
    update_data_file(one_target_file, sim_runs, one_target)
    update_data_file(one_target_sa_file, sim_runs, one_target_sa)
    update_data_file(one_target_plusBonus_file, sim_runs, one_target_plusBonus)


def update_data_file(filepath, num_sims, sim_pattern):
    mean, variance, sim_data = read_data_file(filepath)
    sim_data = [d[0] for d in sim_data]
    for i in range(num_sims):
        sim_value = run_sim(*sim_pattern)[-1]
        if sim_pattern == one_target_sa and sim_value < 30:
            sim_value = 30
        sim_data.append(sim_value)
    sim_data = [str(d) for d in sim_data]
    with open(filepath, 'w') as output_file:
        output_file.write('Number_of_Pulls\n')
        output_file.write('\n'.join(sim_data))


def read_data_file(filepath):
    import os
    dirname = os.path.dirname(filepath)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
    if os.path.exists(filepath):
        with open(filepath, 'r') as input_file:
            data = [line.split(',') for line in input_file.read().split('\n') if line]
        headers = data[0]
        data = data[1:]
        data = [int(d[0]) for d in data]
        if data:
            import numpy
            variance = numpy.var(data)
            mean = numpy.mean(data)
            return mean, variance, data
        else:
            return 0, 0, []
    else:
        return 0, 0, []


if __name__ == '__main__':
    if False:
        # update_files(2*10**4)
        mean, var, _ = read_data_file('data/three_targets.csv')
        print(mean)
        print(var)
    else:
        num_banners = 1
        simulations = []
        for _ in range(sim_runs):
            banner = []
            requirements = []
            for b in range(num_banners):
                banner.append(run_sim(3, [0], 2, 3, 150))
            cost = [x[-1] for x in banner]
            simulations.append(sum(cost))
        avg = sum(simulations) / len(simulations)
        print('Average Rate (with pity): {0}'.format(avg))
        simulations.sort()
        from statistics import mode, median
        mn = mode(simulations)
        mx = max(simulations)
        print('Mode: {0}'.format(mn))
        print('Median: {0}'.format(median(simulations)))
        print('Min: {0}'.format(min(simulations)))
        print('Max: {0}'.format(mx))
        for t in range(mx//10):
            threshold = (t + 1) * 10
            chance = len([_ for _ in simulations if _ <= threshold]) / len(simulations)*100
            print('% chance of getting out in {0} pulls or less: {1}'.format(threshold, chance))
        # print(cost)
