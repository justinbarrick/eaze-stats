import datetime
import json
import math
import os
import pytz

from jinja2 import Template
from sanic import Sanic
from sanic.response import html

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def parse_timestamp(timestamp):
    stamp = datetime.datetime.fromtimestamp(int(timestamp) / 1000)
    return localize(stamp)

def localize(stamp):
    return pytz.utc.localize(stamp).astimezone(pytz.timezone('US/Pacific'))

def tomorrow():
    now = localize(datetime.datetime.now())
    now = now.replace(hour=0, minute=0, second=0)
    return now + datetime.timedelta(days=1)

class EazeData:
    weekdays = [
        'monday', 'tuesday', 'wednesday', 'thursday',
        'friday', 'saturday', 'sunday'
    ]

    def __init__(self, filename, now=None, tomorrow=False):
        self.filename = filename
        self.template = Template(open('report.jinja').read())
        self.__now = now

        self.tomorrow = tomorrow

    @property
    def promos(self):
        promos = []

        for promo in json.load(open(self.filename)):
            promo['timestamp'] = parse_timestamp(promo['date'])
            promos.append(promo)

        return promos

    @property
    def now(self):
        if self.tomorrow:
            return tomorrow()

        return self.__now or localize(datetime.datetime.now())

    @property
    def duration(self):
        start = min(self.promos, key=lambda promo: promo['timestamp'])
        end = max(self.promos, key=lambda promo: promo['timestamp'])

        return end['timestamp'] - start['timestamp']

    @property
    def by_day(self):
        promos = [0]*7

        for promo in self.promos:
            promos[promo['timestamp'].weekday()] += 1

        return promos

    @property
    def by_hour(self):
        promos = [0]*24

        for promo in self.promos:
            promos[promo['timestamp'].hour] += 1

        return promos

    @property
    def by_hour_and_day(self):
        promos = [ [0]*7 for _ in range(24) ]

        for promo in self.promos:
            promos[promo['timestamp'].hour][promo['timestamp'].weekday()] += 1

        return promos

    @property
    def by_day_and_hour(self):
        promos = [ [0]*24 for _ in range(7) ]

        for promo in self.promos:
            promos[promo['timestamp'].weekday()][promo['timestamp'].hour] += 1

        return promos

    @property
    def probability_by_day_and_hour(self):
        probs = self.by_day_and_hour

        for day, hours in enumerate(self.by_day_and_hour):
            weeks = self.num_weeks(day)

            for hour, count in enumerate(hours):
                probs[day][hour] = (count / weeks) * 100

        return probs

    @property
    def probability_today_by_hour(self):
        return self.probability_by_day_and_hour[self.now.weekday()]

    @property
    def probability_today(self):
        return self.probability_today_by_hour[self.now.hour:]

    @property
    def next_promo(self):
        for hour, probability in enumerate(self.probability_today):
            if probability:
                return (hour + self.now.hour, probability)

    @property
    def best_promo(self):
        best = (0, 0)

        for hour, probability in enumerate(self.probability_today):
            if probability > best[1]:
                best = (hour + self.now.hour, probability)

        return best

    @property
    def odds_today(self):
        day = self.now.weekday()
        return (self.by_day[day] / self.num_weeks(day)) * 100

    def list_to_percentages(self, lst):
        total = float(sum(lst))
        if not total:
            return []
        return map(lambda c: (c / total) * 100, lst)

    def num_weeks(self, day):
        return math.ceil(self.duration.days / 7)

    def plot(self, func, msg, name):
        fig = plt.figure()
        eaze = fig.add_subplot('111')
        func(eaze)
        plt.title(msg)

        if not os.path.exists('static'):
            os.mkdir('static')

        fig.savefig('static/eaze_{}.png'.format(name))

    def plot_by_hour(self):
        self.plot(lambda e: e.plot(self.by_hour), 'Eaze promos by hour.', 'by_hour')

    def plot_by_day(self):
        self.plot(lambda e: e.plot(self.by_day), 'Eaze promos by day (Monday == 0).', 'by_day')

    def plot_by_hour_and_day(self):
        data = self.by_hour_and_day
        self.plot(lambda e: e.imshow(data, cmap='hot', interpolation='nearest'), 'Eaze promos by day and hour.', 'by_hour_and_day')

    def render(self):
        return self.template.render(eaze=self, enumerate=enumerate)

    def report(self):
        self.plot_by_hour_and_day()
        self.plot_by_day()
        self.plot_by_hour()

        return self.render()

if __name__ == '__main__':
    app = Sanic()

    app.static('/static', './static')

    @app.route('/')
    async def index(request):
        eaze = EazeData('eaze_dataset.json')
        return html(eaze.report())

    @app.route('/tomorrow')
    async def report_tomorrow(request):
        eaze = EazeData('eaze_dataset.json', tomorrow=True)
        return html(eaze.report())

    app.run(host='0.0.0.0', port=8888)
