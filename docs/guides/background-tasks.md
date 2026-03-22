# Background Tasks

## In-Process Tasks (FastAPI)

```python
from fastapi import BackgroundTasks
from api_toolkit.tasks import task_manager

@app.post("/orders")
async def create_order(order: OrderCreate, background: BackgroundTasks):
    result = await db.create_order(order)
    background.add_task(send_confirmation_email, result.id, order.email)
    background.add_task(update_inventory, result.items)
    return result
```

## Celery Integration

```python
from api_toolkit.tasks import CeleryTaskRouter

router = CeleryTaskRouter(broker="redis://localhost:6379")

@router.task(queue="emails", retry=3, backoff="exponential")
async def send_email(to: str, subject: str, body: str):
    await smtp.send(to, subject, body)

# Dispatch from endpoint
@app.post("/notify")
async def notify(payload: NotificationPayload):
    await send_email.dispatch(payload.email, payload.subject, payload.body)
    return {"queued": True}
```

## Task Monitoring

```python
# Track task status
@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    return await router.get_status(task_id)
```
