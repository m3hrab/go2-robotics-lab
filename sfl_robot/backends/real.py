class RealBackend:
    """Real-robot backend — implemented in Milestone 2 against the Unitree SDK."""

    def __init__(self):
        raise NotImplementedError("Real backend not yet implemented (Milestone 2)")

    def walk_to(self, x, y):
        raise NotImplementedError

    def turn(self, deg):
        raise NotImplementedError

    def stand(self):
        raise NotImplementedError

    def sit(self):
        raise NotImplementedError

    def get_camera_image(self):
        raise NotImplementedError

    def get_obstacle_distance(self):
        raise NotImplementedError