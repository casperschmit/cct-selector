from locust import HttpUser, task, between
import csv
import pandas as pd

USER_CREDENTIALS = None


class User(HttpUser):
    wait_time = between(10, 15)
    email = "NOT_FOUND"
    password = "NOT_FOUND"
    username = "NOT_FOUND"
    confirm_password = "NOT_FOUND"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        global USER_CREDENTIALS
        if USER_CREDENTIALS is None:
            df = pd.read_excel('registration.xlsx', sheet_name='registration')
            USER_CREDENTIALS = df.values.tolist()

    def on_start(self):
        if USER_CREDENTIALS:
            self.username, self.email, self.password, self.confirm_password = USER_CREDENTIALS.pop()
        # self.client.post("/register", json={"username": self.username, "email": self.email,
        #                                     "password": self.password, "confirm_password": self.confirm_password})

        self.client.post("/login", json={"email": self.email, "password": self.password})

        # self.client.post("/system", json={"scenario": "('cho_1', 'Connecting two defined blockchain systems')"})
        #
        # self.client.post("/system/step/1", json={"source": "Bitcoin", "target": "Ethereum", "source_permissions":
        #     "Public permissionless", "target_permissions": "Public permissionless",
        #                                          "decentralization": "yes", "scalability": "yes", "development": "yes",
        #                                          "efficiency": "yes", "tokens": "yes", "crypto": "yes", "oracle": "yes",
        #                                          "smart_contract": "yes", "transfer": "yes"})
        #
        # self.client.post("/system/step/2", json={"team_size": "4", "team_experience": "(0, 'Inexperienced')"})
        #
        # self.client.post("/system/step/3", json={"project_description": "stress test"})
        #
        # self.client.post("/system/step/4", json={"cost_weight": 1, "compatibility_weight": 1, "relevancy_weight": 1,
        #                                          "complexity_weight": 1, "security_weight": 1, "devsupport_weight": 1})

    def on_stop(self):
        self.client.post("/remove_tests")
        self.client.get("/logout")

    # @task
    # def index(self):
    #     self.client.get("/")

    @task
    def system(self):
        self.client.post("/system", json={"scenario": "('cho_1', 'Connecting two defined blockchain systems')"})

        self.client.post("/system/step/1", json={"source": "Bitcoin", "target": "Ethereum", "source_permissions":
            "Public permissionless", "target_permissions": "Public permissionless",
                                                 "decentralization": "yes", "scalability": "yes", "development": "yes",
                                                 "efficiency": "yes", "tokens": "yes", "crypto": "yes", "oracle": "yes",
                                                 "smart_contract": "yes", "transfer": "yes"})

        self.client.post("/system/step/2", json={"team_size": "4", "team_experience": "(0, 'Inexperienced')"})

        self.client.post("/system/step/3", json={"project_description": "stress test"})
        self.client.post("/system/step/4", json={"cost_weight": 1, "compatibility_weight": 1, "relevancy_weight": 1,
                                                 "complexity_weight": 1, "security_weight": 1, "devsupport_weight": 1})

    # @task
    # def write(self):
    #     self.client.post("/centralized_write")
    #
    # @task
    # def read(self):
    #     self.client.post("/centralized_read")

    # @task
    # def render_only(self):
    #     self.client.post("/render_only")

    # @task
    # def decentralized_write(self):
    #     self.client.post("/decentralized_write")
    #
    # @task
    # def decentralized_read(self):
    #     self.client.post("/decentralized_read")

