from locust import HttpUser, LoadTestShape, task, between, TaskSet


class StepLoadShape(LoadTestShape):
    """
    A step load shape that adds users at a fixed interval.
    起始用户数量为20，每小时增加10个用户，持续5个小时
    """

    step_time = 3600  # Time between steps (in seconds)
    step_load = 10  # Users to add at each step
    spawn_rate = 10  # Users to spawn per second
    time_limit = 18000  # Total test duration (in seconds)

    def tick(self):
        run_time = self.get_run_time()

        if run_time > self.time_limit:
            return None

        current_step = run_time // self.step_time
        return (20 + current_step * self.step_load, self.spawn_rate)


# Add this shape to your Locust test
class UserBehavior(TaskSet):
    @task
    def pay_order(self):
        # ...existing code...
        pass


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)
    load_shape = StepLoadShape
