import datetime
import calendar
from parameters import WaterLPParameter

from utilities.converter import convert


class IFR_bl_Hunter_Reservoir_Requirement(WaterLPParameter):
    """"""

    def _value(self, timestep, scenario_index):
        if 5 <= self.datetime.month <= 10:  # May-Oct
            ifr_val = 1.6 / 35.31  # cfs to cms
        else:
            ifr_val = 0.6 / 35.31  # cfs to cms

        if self.mode == 'planning':
            ifr_val *= self.days_in_month
        return ifr_val

    def value(self, *args, **kwargs):
        try:
            ifr = self.get_ifr(*args, **kwargs)
            if ifr is not None:
                return ifr
            else:
                ifr = self._value(*args, **kwargs)
                return convert(ifr, "m^3 s^-1", "m^3 day^-1", scale_in=1, scale_out=1000000.0)
        except Exception as err:
            print('\nERROR for parameter {}'.format(self.name))
            print('File where error occurred: {}'.format(__file__))
            print(err)

    @classmethod
    def load(cls, model, data):
        return cls(model, **data)


IFR_bl_Hunter_Reservoir_Requirement.register()
print(" [*] IFR_bl_Hunter_Reservoir_Requirement successfully registered")
