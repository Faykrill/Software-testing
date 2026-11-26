import uuid

from locust import HttpUser, SequentialTaskSet, between, task


class PublishAndReadFlow(SequentialTaskSet):
    """Бизнес-поток: создать пост -> извлечь id -> прочитать свой пост."""

    @task
    def create_post(self):
        payload = {
            "title": f"Post by {self.user.username}",
            "author": self.user.username,
            "content": "Load testing with Locust",
        }
        with self.client.post(
            "/posts", json=payload, name="POST /posts", catch_response=True
        ) as response:
            if response.status_code == 201:
                self.post_id = response.json()["id"]  # извлекаем id из JSON-ответа
                response.success()
            else:
                response.failure(f"Expected 201, got {response.status_code}")
                self.post_id = None
        if self.post_id is None:
            self.interrupt()  # пост не создан -> дальше читать нечего

    @task
    def read_own_post(self):
        with self.client.get(
            f"/posts/{self.post_id}",
            name="GET /posts/[id]",  # общее имя: статистика не дробится по каждому id
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(f"Expected 200, got {response.status_code}")
        self.interrupt()  # поток завершён -> возврат к выбору задач по весам


class BlogUser(HttpUser):
    host = "http://localhost:5000"
    wait_time = between(1, 2)  # think time: пауза 1–2 с между задачами

    def on_start(self):
        # "авторизация": один раз на пользователя генерируем уникальное имя
        self.username = f"user_{uuid.uuid4()}"

    @task(5)
    def read_all_posts(self):
        self.client.get("/posts", name="GET /posts")

    @task(3)
    def read_first_post(self):
        self.client.get("/posts/1", name="GET /posts/1")

    tasks = {PublishAndReadFlow: 1}  # весь бизнес-поток — одна задача с весом 1