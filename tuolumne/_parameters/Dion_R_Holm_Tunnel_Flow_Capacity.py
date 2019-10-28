from parameters import WaterLPParameter

from utilities.converter import convert

class Dion_R_Holm_Tunnel_Flow_Capacity(WaterLPParameter):
    """"""

    def _value(self, timestep, scenario_index):
        kwargs = dict(timestep=timestep, scenario_index=scenario_index)
        return 1000*self.get("cfs2cms", **kwargs)
        
    def value(self, timestep, scenario_index):
        try:
            return convert(self._value(timestep, scenario_index), "m^3 s^-1", "m^3 day^-1", scale_in=1, scale_out=1000000.0)
        except Exception as err:
            print('ERROR for parameter {}'.format(self.name))
            print('File where error occurred: {}'.format(__file__))
            print(err)
            raise

    @classmethod
    def load(cls, model, data):
        return cls(model, **data)
        
Dion_R_Holm_Tunnel_Flow_Capacity.register()
print(" [*] Dion_R_Holm_Tunnel_Flow_Capacity successfully registered")
