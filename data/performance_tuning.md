# Performance Tuning and Best Practices

To maximize performance:
- Use pagination for all API list requests (e.g., limit=50, offset=0).
- Only request the fields you need using the `fields` query parameter.
- Cache static responses on your end to reduce API calls.
- Use the bulk API endpoints when creating or updating multiple records simultaneously.