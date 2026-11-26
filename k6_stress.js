import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '1m', target: 50 },   // stage 1: разгон до 50 VU
    { duration: '1m', target: 50 },   // stage 2: удержание 50 VU
    { duration: '30s', target: 0 },   // stage 3: спад до 0
  ],
  thresholds: {
    // требование: доля проваленных checks < 1%.
    // В k6 метрика checks хранит долю УСПЕШНЫХ проверок, поэтому это rate > 0.99
    checks: ['rate>0.99'],
    'http_req_duration{name:GET /posts}': ['p(95)<500'],
    'http_req_duration{name:POST /posts}': ['p(95)<2000'],
  },
};

const BASE_URL = 'http://127.0.0.1:5000'

export default function () {
  if (Math.random() < 0.9) {
    // 90% итераций — чтение списка
    const res = http.get(`${BASE_URL}/posts`, { tags: { name: 'GET /posts' } });
    check(res, { 'GET /posts -> 200': (r) => r.status === 200 });
  } else {
    // 10% итераций — создание поста
    const payload = JSON.stringify({
      title: `Stress post VU${__VU} iter${__ITER}`,
      author: `k6_vu_${__VU}`,
      content: 'k6 stress test',
    });
    const res = http.post(`${BASE_URL}/posts`, payload, {
      headers: { 'Content-Type': 'application/json' },
      tags: { name: 'POST /posts' },
    });
    check(res, { 'POST /posts -> 201': (r) => r.status === 201 });
  }
  sleep(1); // think time: без него 50 VU утопят dev-сервер, а растущий список постов раздует p95 чтения
}