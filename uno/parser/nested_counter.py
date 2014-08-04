# -*- coding: utf-8 -*-

class NestedCounter(object):

    def __init__(self):
        self.count = 0
        self.chart = [0]
        self.total = 0
        self.serial_events = ['init']

    @property
    def g_id(self):
        return str(self.total)

    @property
    def position(self):
        self.print_chart
        y = [str(x) for x in self.chart]
        return '_'.join(y)

    @property
    def up_total(self):
        self.total += 1

    @property
    def print_chart(self):
        print 'chart:', str(self.chart)

    @property
    def pos(self):
        if len(self.pos) > 0:
            self.pos = str(self.chart[-1])
        return self._pos
    @pos.setter
    def pos(self, value):
        self._pos = value

    @property
    def new_level(self):
        self.count = 0
        self.chart.append(0)
        self.print_chart
        self.up_total
        ser_string = 'new level: {}'
        ser_string.format(str(len(self.chart)))
        self.serial_events.append(ser_string)

    @property
    def end_level(self):
        self.chart.pop(-1)
        try:
            self.counter = self.chart[-1]
        except:
            self.counter = 0
            print 'counter reset to 0 when len of chart was:', str(len(self.chart))
        self.print_chart
        ser_string = 'end level: {}, current item: {}'
        ser_string.format(str(len(self.chart) + 1), str(self.counter))
        self.serial_events.append(ser_string)

    @property
    def next(self):
        self.count += 1
        try:
            self.chart[-1] = self.count
        except:
            len_chart = len(self.chart)
            self.chart = [0]
            print 'chart was reinitialized with 0 as first(0th) index when len of chart was:', str(len_chart)
        self.print_chart
        self.up_total
        ser_string = 'new feature on level: {}, item: {}'
        ser_string.format(str(len(self.chart)),  str(self.count))
        self.serial_events.append(ser_string)

    def __repr__(self):
        return str(self.chart)

    def uplevel(self, varname):
        self.new_level
