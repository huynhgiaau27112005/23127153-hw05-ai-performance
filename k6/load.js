import http from 'k6/http';
import { check, sleep } from 'k6';
import { SharedArray } from 'k6/data';

const users = new SharedArray('users', () => {
  const raw = open('../data/users.csv');
  return raw
    .split('\n')
    .slice(1)
    .filter((l) => l.trim())
    .map((line) => {
      const [email, password, search_keyword, product_id, quantity, shipping_address] = line.split(',');
      return { email, password, search_keyword, product_id, quantity, shipping_address };
    });
});

const BASE = __ENV.API_URL || 'http://127.0.0.1:3010';
const STUDENT_ID = '23127153';

export const options = {
  scenarios: {
    load: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '30s', target: 15 },
        { duration: '2m', target: 15 },
        { duration: '10s', target: 0 },
      ],
      exec: 'e2e',
      tags: { scenario: 'load' },
    },
  },
};

export function e2e() {
  const u = users[(__VU - 1) % users.length];
  const headers = { 'Content-Type': 'application/json', 'X-Student-Id': STUDENT_ID };

  const login = http.post(`${BASE}/api/login`, JSON.stringify({ email: u.email, password: u.password }), { headers });
  check(login, { 'login 200': (r) => r.status === 200 });
  if (login.status !== 200) return;
  const token = login.json('token');
  const auth = { ...headers, Authorization: `Bearer ${token}` };

  const products = http.get(`${BASE}/api/products?search=${u.search_keyword}`, { headers });
  check(products, { 'products 200': (r) => r.status === 200 });
  const list = products.json();
  const pid = Array.isArray(list) && list.length ? list[0].id : Number(u.product_id);

  http.get(`${BASE}/api/products/${pid}`, { headers });
  http.post(`${BASE}/api/cart`, JSON.stringify({ id: pid, name: 'Perf', price: 100000, quantity: Number(u.quantity) }), { headers: auth });
  const checkout = http.post(`${BASE}/api/checkout`, JSON.stringify({ total_amount: 100000, shipping_address: u.shipping_address }), { headers: auth });
  check(checkout, { 'checkout 200': (r) => r.status === 200 });
  sleep(2);
}
