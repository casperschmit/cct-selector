from locust import HttpUser, task, between
import csv
import pandas as pd

USER_CREDENTIALS = None


class User(HttpUser):
    wait_time = between(1, 5)
    email = "NOT_FOUND"
    password = "NOT_FOUND"
    username = "NOT_FOUND"
    confirm_password = "NOT_FOUND"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        global USER_CREDENTIALS
        if USER_CREDENTIALS is None:
            # with open('registration.csv', 'rb') as f:
            #     reader = csv.reader(f)
            #     USER_CREDENTIALS = list(reader)
            df = pd.read_excel('registration.xlsx', sheet_name='registration')
            USER_CREDENTIALS = df.values.tolist()

    def on_start(self):
        if USER_CREDENTIALS:
            self.username, self.email, self.password, self.confirm_password = USER_CREDENTIALS.pop()
        # self.client.post("/register", json={"username": self.username, "email": self.email,
        #                                     "password": self.password, "confirm_password": self.confirm_password})
        # self.client.post("/register", json={"username": "salanto", "email": "hellotest1@gmail.com",
        #                                     "password": "hello12", "confirm_password": "hello12"})
        self.client.post("/login", json={"email": self.email, "password": self.password})

    def on_stop(self):
        self.client.get("/logout")

    @task
    def index(self):
        self.client.get("/")

    @task
    def system(self):
        self.client.get("/system")

    @task
    def login(self):
        self.client.post("/login", json={"email": "hellotest@gmail.com", "password": "hello1"})
