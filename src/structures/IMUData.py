class IMUData:

    """
    accel data, gyro data
    """

    def __init__(self, accel_x: float = None, accel_y: float = None, accel_z: float = None,
                 gyro_x: float = None, gyro_y: float = None, gyro_z: float = None,
                 roll: float = None, pitch: float = None, yaw: float = None):

        self.accel_x = accel_x
        self.accel_y = accel_y
        self.accel_z = accel_z
        self.gyro_x = gyro_x
        self.gyro_y = gyro_y
        self.gyro_z = gyro_z
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw
