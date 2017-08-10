from nose.tools import *
from freezegun import freeze_time
import datetime
import eaze

def test_eaze_duration():
    e = eaze.EazeData('./tests/test_data/eaze_dataset.json')
    assert_equal(e.duration.days, 65)
    assert_equal(e.num_weeks(2), 10)

def test_eaze_by_day():
    e = eaze.EazeData('./tests/test_data/eaze_dataset.json')
    assert_equal(e.by_day, [6,9,5,7,7,6,8])

def test_eaze_by_hour():
    e = eaze.EazeData('./tests/test_data/eaze_dataset.json')
    assert_equal(e.by_hour, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 5, 2, 6, 3, 1, 1, 8, 9, 4, 7, 1, 0, 0])

def test_eaze_by_hour_and_day():
    e = eaze.EazeData('./tests/test_data/eaze_dataset.json')
    assert_equal(e.by_hour_and_day, [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0],
        [2, 1, 0, 0, 0, 0, 2],
        [0, 1, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 1, 1, 3],
        [1, 1, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [1, 1, 1, 1, 3, 1, 0],
        [1, 4, 1, 1, 0, 1, 1],
        [0, 0, 2, 0, 1, 1, 0],
        [1, 0, 1, 4, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]
    ])

def test_eaze_by_day_and_hour():
    e = eaze.EazeData('./tests/test_data/eaze_dataset.json')
    assert_equal(e.by_day_and_hour, [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 4, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 4, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 3, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 3, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0]
    ])

def test_eaze_probability_by_day_and_hour():
    e = eaze.EazeData('./tests/test_data/eaze_dataset.json')
    assert_equal(e.probability_by_day_and_hour, [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 20, 0.0, 0.0, 10, 0.0, 0.0, 10, 10, 0.0, 10, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 10, 10, 10, 10, 0.0, 0.0, 10, 40, 0.0, 0.0, 0.0, 0.0, 0.0], 
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 10, 10, 20, 10, 0.0, 0.0, 0.0], 
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 10, 10, 10, 0.0, 40, 0.0, 0.0, 0.0], 
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 10, 10, 0.0, 0.0, 0.0, 30, 0.0, 10, 10, 0.0, 0.0, 0.0], 
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 10, 0.0, 0.0, 10, 0.0, 10, 0.0, 10, 10, 10, 0.0, 0.0, 0.0, 0.0], 
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 20, 0.0, 30, 10, 0.0, 0.0, 0.0, 10, 0.0, 0.0, 10, 0.0, 0.0]
    ])

def test_eaze_probability_today_by_hour():
    now = datetime.datetime(2017, 8, 9, 10, 0, 0)
    e = eaze.EazeData('./tests/test_data/eaze_dataset.json', now=now)
    assert_equal(e.probability_today_by_hour, [
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 10, 10, 20, 10, 0.0, 0.0, 0.0
    ])

def test_eaze_probability_today():
    now = datetime.datetime(2017, 8, 9, 10, 0, 0)
    e = eaze.EazeData('./tests/test_data/eaze_dataset.json', now=now)
    assert_equal(e.probability_today, [
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        10, 10, 20, 10, 0.0, 0.0, 0.0
    ])

def test_eaze_promo_predictions():
    now = datetime.datetime(2017, 8, 9, 10, 0, 0)
    e = eaze.EazeData('./tests/test_data/eaze_dataset.json', now=now)
    assert_equal(e.next_promo, (17, 10))
    assert_equal(e.best_promo, (19, 20))
    assert_equal(e.odds_today, 50)

@freeze_time(eaze.localize(datetime.datetime(2017, 8, 10, 6, 30, 0)))
def test_tomorrow():
    assert_equal(eaze.tomorrow(), eaze.localize(datetime.datetime(2017, 8, 10, 7, 0, 0)))

@freeze_time(eaze.localize(datetime.datetime(2017, 8, 9, 10, 0, 0)))
def test_eaze_today():
    e = eaze.EazeData('./tests/test_data/eaze_dataset.json')
    assert_equal(e.now, eaze.localize(datetime.datetime(2017, 8, 9, 10, 0, 0)))
    assert_equal(e.next_promo, (17, 10))
    assert_in('Statistics for today:', e.report())

@freeze_time(eaze.localize(datetime.datetime(2017, 8, 9, 10, 0, 0)))
def test_eaze_tomorrow():
    e = eaze.EazeData('./tests/test_data/eaze_dataset.json', tomorrow=True)
    assert_equal(e.now, eaze.tomorrow())
    assert_equal(e.next_promo, (16, 10))
    assert_in('Statistics for tomorrow:', e.report())

def test_localize():
    now = eaze.localize(datetime.datetime(2017, 8, 6, 10, 0, 0))
    assert_equal(now.weekday(), 6)
    assert_equal(now.hour, 3)

    now = eaze.localize(datetime.datetime(2017, 8, 6, 3, 0, 0))
    assert_equal(now.weekday(), 5)
    assert_equal(now.hour, 20)
