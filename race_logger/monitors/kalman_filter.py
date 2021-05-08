import logging
from statistics import mean

from awebus import Bus
import numpy as np
from filterpy.kalman import KalmanFilter
from filterpy.common.kinematic import kinematic_kf
from filterpy.common.discretization import Q_discrete_white_noise

_event_bus: Bus = None
_kalman_filter: KalmanFilter = kinematic_kf(dim=2, order=2, dt=0.2, dim_z=1, order_by_dim=False)
_kalman_filter.P *= 1e-4
_kalman_filter.R *= 1e-4
_has_init_estimate = False
_init_gps_data = []
_init_timestamp_data = []
_last_timestamp = None


async def kalman_filter(event_bus: Bus):
    global _event_bus
    _event_bus = event_bus
    event_bus.on("gps_data", _handle_gps_data)


async def _handle_gps_data(timestamp, gps_coordinate, _speed, _climb, _heading):
    global _kalman_filter, _has_init_estimate, _last_timestamp
    if len(_init_gps_data) < 3:
        _init_gps_data.append(gps_coordinate[:2])
        _init_timestamp_data.append(timestamp)
        return
    if not _has_init_estimate:
        lat_vel_1 = (_init_gps_data[1][0] - _init_gps_data[0][0]) / (_init_timestamp_data[1] - _init_timestamp_data[0])
        lon_vel_1 = (_init_gps_data[1][1] - _init_gps_data[0][1]) / (_init_timestamp_data[1] - _init_timestamp_data[0])
        lat_vel_2 = (_init_gps_data[2][0] - _init_gps_data[1][0]) / (_init_timestamp_data[2] - _init_timestamp_data[1])
        lon_vel_2 = (_init_gps_data[2][1] - _init_gps_data[1][1]) / (_init_timestamp_data[2] - _init_timestamp_data[1])
        accel_dt = (mean((_init_timestamp_data[1], _init_timestamp_data[2])) -
                    mean((_init_timestamp_data[0], _init_timestamp_data[1])))
        lat_accel = (lat_vel_2 - lat_vel_1) / accel_dt
        lon_accel = (lon_vel_2 - lon_vel_1) / accel_dt
        _kalman_filter.x = np.array(gps_coordinate[:2] + (lat_vel_2, lon_vel_2, lat_accel, lon_accel))
        _last_timestamp = timestamp
        _has_init_estimate = True
        return
    dt = timestamp - _last_timestamp
    _kalman_filter.F = _get_f(dt)
    _kalman_filter.Q = Q_discrete_white_noise(dim=3, dt=dt, var=1e-4, block_size=2, order_by_dim=False)
    _last_timestamp = timestamp
    _kalman_filter.predict()
    _kalman_filter.update(gps_coordinate[:2])
    logging.info("Kalman Estimate: {}".format(_kalman_filter.x))
    logging.debug("Kalman P: {}".format(_kalman_filter.P))
    await _event_bus.emitAsync("kalman_gps_data", timestamp, tuple(_kalman_filter.x[:2]))


def _get_f(dt):
    return np.array([
        [1., 0., dt, 0., 0.5*dt**2, 0.],
        [0., 1., 0., dt, 0., 0.5*dt**2],
        [0., 0., 1., 0., dt, 0.],
        [0., 0., 0., 1., 0., dt],
        [0., 0., 0., 0., 1., 0.],
        [0., 0., 0., 0., 0., 1.]
    ])
