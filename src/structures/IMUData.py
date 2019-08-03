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

    @staticmethod
    def get_csv_header():
        return "Accelerometer X, Accelerometer Y, Accelerometer Z, Gyro X, Gyro Y, Gyro Z, Roll, Pitch, Yaw"

    def get_imu_as_csv(self):
        return "{}, {}, {}, {}, {}, {}, {}, {}, {}". format(
            self.accel_x, self.accel_y, self.accel_z,
            self.gyro_x, self.gyro_y, self.gyro_z,
            self.roll, self.pitch, self.yaw
        )
