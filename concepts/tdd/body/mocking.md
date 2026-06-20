# When to mock

Mock at **system boundaries** only:
- External APIs (payment, email, etc.)
- Databases (sometimes — prefer a test DB)
- Time / randomness
- File system (sometimes)

**Don't mock:**
- Your own classes/modules
- Internal collaborators
- Anything you control

## Designing for mockability

At system boundaries, design interfaces that are easy to mock.

**1. Use dependency injection** — pass external dependencies in rather than creating them internally:

```typescript
// Easy to mock
function processPayment(order, paymentClient) {
  return paymentClient.charge(order.total);
}

// Hard to mock
function processPayment(order) {
  const client = new StripeClient(process.env.STRIPE_KEY);
  return client.charge(order.total);
}
```

**2. Prefer SDK-style interfaces over generic fetchers** — one specific function per external operation, not one generic function with conditional logic:

```typescript
// GOOD: each function is independently mockable
const api = {
  getUser: (id) => fetch(`/users/${id}`),
  getOrders: (userId) => fetch(`/users/${userId}/orders`),
  createOrder: (data) => fetch("/orders", { method: "POST", body: data }),
};

// BAD: mocking requires conditional logic inside the mock
const api = {
  fetch: (endpoint, options) => fetch(endpoint, options),
};
```

The SDK approach means each mock returns one specific shape, no conditional logic in test setup, and it's easy to see which endpoints a test exercises.
