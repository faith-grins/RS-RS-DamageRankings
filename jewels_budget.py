import find_cost_of_ss_style as cost
import datetime
import numpy
from enum import Enum
from typing import List
from statistics import mode
from collections import OrderedDict


monthly_pack = True
granular_earnings = False
daily_average = 1900
pull_plan_file = 'data/pull_plan_2021-11-13.csv'
results_file = 'data/simulation_results.csv'
starting_jewels = 186396
cost_of_jewel_pack = 36.00
end_date = datetime.date(2022, 10, 1)


class BannerType(Enum):
    Main1 = 1
    Main1S1 = 2
    Main1Bonus1 = 3
    Main2 = 4
    Main3 = 5
    Main4 = 6


class PullPlanBanner:
    banner_name = ''
    banner_type = BannerType.Main1
    banner_date = datetime.date.today()

    def __init__(self, data_row: str):
        strings = data_row.split(',')
        self.banner_name = strings[0]
        self.banner_type = BannerType[strings[1]]
        date_ints = [int(s) for s in strings[2].split('-')]
        self.banner_date = datetime.date(date_ints[0], date_ints[1], date_ints[2])


class SimResult:
    jewels_purchased = 0
    cost_of_purchase = 0
    dollars_spent = 0.0
    number_of_pulls = 0
    number_of_acquisitions = 0
    current_date = datetime.date.today()

    def __init__(self, start_jewels: int, pull_plan: List[PullPlanBanner], jewels_cost: float):
        self.jewels_left = start_jewels
        self.pull_plan = pull_plan
        self.cost_of_purchase = jewels_cost

    def earn_jewels_to_date(self, target_date: datetime.date,
                            daily_avg: int,
                            simple_earnings_model: bool,
                            monthly_pack_active: bool):
        if target_date > self.current_date:
            duration = (target_date - self.current_date).days
            if simple_earnings_model:
                if monthly_pack_active:
                    daily_avg += 120
                self.jewels_left += daily_avg * duration
            else:
                daily = 330 if monthly_pack_active else 230
                weekly = 1200
                biweekly = 500
                event_haul = 2000
                monthly = 6890 if monthly_pack_active else 6270
                self.jewels_left += (duration * daily)\
                    + (duration // 7 * weekly)\
                    + (duration // 14 * biweekly) \
                    + (duration // 10 * event_haul)\
                    + (duration // 30) * monthly
                # leverage paid jewels
                paid_modifier = 2.5
                if monthly_pack:
                    self.jewels_left += 620 * (paid_modifier - 1) * duration // 30
            self.current_date = target_date

    def purchase_jewels(self):
        self.jewels_purchased += 15000
        self.jewels_left += 15000
        self.dollars_spent += self.cost_of_purchase

    def run_simulation(self, ending_date, daily_avg, simple_earnings, monthly_active):
        for banner in self.pull_plan:
            if banner.banner_date > ending_date:
                continue
            self.earn_jewels_to_date(banner.banner_date, daily_avg, simple_earnings, monthly_active)
            if banner.banner_type == BannerType.Main1:
                sim = cost.run_sim(*cost.one_target)
            elif banner.banner_type == BannerType.Main1S1:
                sim = cost.run_sim(*cost.one_target_sa)
            elif banner.banner_type == BannerType.Main1Bonus1:
                sim = cost.run_sim(*cost.one_target_plusBonus)
            elif banner.banner_type == BannerType.Main2:
                sim = cost.run_sim(*cost.two_targets)
            elif banner.banner_type == BannerType.Main3:
                sim = cost.run_sim(*cost.three_targets)
            else:
                sim = cost.run_sim(*cost.four_targets)
            cost_of_banner = sim.number_of_pulls * 300
            while cost_of_banner > self.jewels_left:
                self.purchase_jewels()
            self.jewels_left -= cost_of_banner
            self.number_of_pulls += sim.number_of_pulls
            self.number_of_acquisitions += len(sim.result_list)


class PercentileMarker:
    def __init__(self, pulls, jewels, dollas):
        self.pulls = pulls
        self.jewels = jewels
        self.dollars = dollas


class StringsManager:
    def __init__(self, sims_list: List[SimResult]):
        self.sims_list = sims_list
        pulls = [n.number_of_pulls for n in self.sims_list]
        self.average_styles = sum([s.number_of_acquisitions for s in self.sims_list]) // len(self.sims_list)
        self.average_pulls = sum(pulls) // len(pulls)
        self.average_jewels_left = sum([s.jewels_left for s in self.sims_list]) // len(self.sims_list)
        self.average_jewels_purchased = sum([s.jewels_purchased for s in self.sims_list]) // len(self.sims_list)
        self.average_dollars_spent = sum([s.dollars_spent for s in self.sims_list]) / len(self.sims_list)
        self.min_pulls = min(pulls)
        self.max_pulls = max(pulls)
        self.mode_pulls = mode(pulls)
        self.median_pulls = int(numpy.percentile(pulls, 50))
        pull_keys = {s.number_of_pulls: s for s in self.sims_list}
        self.percentiles = OrderedDict.fromkeys([50, 75, 90, 95, 99])
        for p in self.percentiles:
            percent = pull_keys[int(numpy.percentile(pulls, p))]
            self.percentiles[p] = PercentileMarker(percent.number_of_pulls, percent.jewels_left, percent.dollars_spent)

    def print(self):
        print('Average # of Styles acquired: {0}'.format(self.average_styles))
        print('Average # of pulls made: {0}'.format(self.average_pulls))
        print('Average # of jewels left: {0}'.format(self.average_jewels_left))
        print('Average # of jewels purchased: {0}'.format(self.average_jewels_purchased))
        print('Average $$$ spent: ${0:.2f}\n'.format(self.average_dollars_spent))
        print('Mode: {0}'.format(self.mode_pulls))
        print('Median: {0}'.format(self.median_pulls))
        print('Min: {0}'.format(self.min_pulls))
        print('Max: {0}\n'.format(self.max_pulls))
        percentile_string = '{0}th %ile --\n--pulls: {1}\n--jewels left: {2}\n--dollars spent: ${3:.2f}\n'
        for p in self.percentiles:
            print(percentile_string.format(p,
                                           self.percentiles[p].pulls,
                                           self.percentiles[p].jewels,
                                           self.percentiles[p].dollars))

    def write_to_file(self, filename, new_file=False):
        field_list = [datetime.date.today().isoformat(), self.average_styles, self.average_pulls,
                      self.average_jewels_left, self.average_jewels_purchased, self.average_dollars_spent,
                      self.mode_pulls, self.median_pulls, self.min_pulls, self.max_pulls]
        for key in self.percentiles:
            field_list.append(self.percentiles[key].pulls)
            field_list.append(self.percentiles[key].jewels)
            field_list.append(self.percentiles[key].dollars)
        file_mode = 'w' if new_file else 'a'
        with open(filename, file_mode) as output_file:
            if new_file:
                header_string = 'DateOfSim,Avg#Styles,Avg#Pulls,Avg#JewelsLeft,Avg#JewelsBought,Avg$Spent,' \
                                'ModePulls,MedianPulls,MinPulls,MaxPulls,'
                for key in self.percentiles:
                    header_string += ',{0}th%Pulls,{0}th%JewelsLeft,{0}th%$Spent'.format(key)
                output_file.write(header_string)
                output_file.write('\n')
            output_file.write(','.join([str(f) for f in field_list]))
            output_file.write('\n')


if __name__ == '__main__':
    # estimated festival giveaways not accounted for by general model
    # starting_jewels += 45000 * 1
    # starting_jewels = 270001
    simulations = []
    start_date = datetime.date.today()

    with open(pull_plan_file, 'r') as plan_file:
        plan_banners = [PullPlanBanner(s) for s in plan_file.read().split('\n')[1:]]
    for _ in range(cost.sim_runs):
        sim_run = SimResult(starting_jewels, plan_banners, cost_of_jewel_pack)
        sim_run.run_simulation(end_date, daily_average, not granular_earnings, monthly_pack)
        simulations.append(sim_run)

    text = StringsManager(simulations)
    text.print()
    text.write_to_file(results_file, False)
