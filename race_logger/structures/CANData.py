class CANData:

    """
    engine speed, throttle position, coolant temp, oil temp, intake air temp,
    MAP sensor (Manifold air pressure after throttle), battery voltage, fuel pressure, oil pressure
    """

    def __init__(self, engine_speed: float = None, throttle_position: float = None, coolant_temp: float = None,
                 oil_temp: float = None, intake_air_temp: float = None, map_sensor: float = None,
                 battery_voltage: float = None, fuel_pressure: float = None, oil_pressure: float = None):

        self.engine_speed: float = engine_speed
        self.throttle_position: float = throttle_position
        self.coolant_temp: float = coolant_temp
        self.oil_temp: float = oil_temp
        self.intake_air_temp: float = intake_air_temp
        self.map_sensor: float = map_sensor
        self.battery_voltage: float = battery_voltage
        self.fuel_pressure: float = fuel_pressure
        self.oil_pressure: float = oil_pressure

    @staticmethod
    def get_csv_header():
        return "Engine Speed, Throttle Position, Coolant Temp, Oil Temp, Intake Air Temp, " \
               "MAP Sensor, Battery Voltage, Fuel Pressure, Oil Pressure"

    def get_can_as_csv(self):
        return "{}, {}, {}, {}, {}, {}, {}, {}, {}".format(
            self.engine_speed,
            self.throttle_position,
            self.coolant_temp,
            self.oil_temp,
            self.intake_air_temp,
            self.map_sensor,
            self.battery_voltage,
            self.fuel_pressure,
            self.oil_pressure
        )
