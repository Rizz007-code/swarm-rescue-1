from solutions.my_drone_random import MyDroneRandom


class MyDroneEval(MyDroneRandom):
    
    def __init__(self):
        super().__init__()
        self.target = None  # Current target for the drone (wounded person)
        self.state = "search"  # Possible states: search, rescue, return

    def define_message_for_all(self):
        return {"state": self.state, "target": self.target}

    def control(self):
        if self.state == "search":
            self.target = self.find_closest_wounded()
            if self.target:
                self.state = "rescue"

        elif self.state == "rescue":
            if self.at_target(self.target):
                self.pick_up_wounded()
                self.state = "return"
            else:
                self.navigate_to(self.target)

        elif self.state == "return":
            if self.at_rescue_center():
                self.drop_wounded()
                self.state = "search"
            else:
                self.navigate_to_rescue_center()

    def find_closest_wounded(self):
        """Find the closest wounded person while avoiding obstacles."""
        return self.explored_map.find_nearest_wounded(self.position)

    def navigate_to(self, target):
        """Navigate to the target while avoiding obstacles and zones."""
        path = self.compute_safe_path(target)
        self.follow_path(path)

    def at_target(self, target):
        """Check if the drone is at the target location."""
        return self.distance_to(target) < self.position_tolerance

    def pick_up_wounded(self):
        """Pick up the wounded person."""
        self.carry_wounded = True

    def at_rescue_center(self):
        """Check if the drone has reached the rescue center."""
        return self.position_in_area(self.rescue_center)

    def drop_wounded(self):
        """Drop the wounded person at the rescue center."""
        self.carry_wounded = False

    def compute_safe_path(self, target):
        """Compute the shortest path to the target avoiding zones."""
        return self.explored_map.shortest_path(self.position, target, avoid_zones=["Kill Zone"])
    pass
