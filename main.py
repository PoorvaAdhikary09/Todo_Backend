from fastapi import FastAPI, HTTPException
from model import Task, UpdateTask
from crud import (
    add_task, retrieve_tasks, retrieve_task_by_slno,
    update_task_by_slno, delete_task_by_slno
)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to the To-Do API with MongoDB"}

@app.post("/tasks")
async def create_task(task: Task):
    try:
        return await add_task(task)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/tasks")
async def get_all_tasks():
    return await retrieve_tasks()

@app.get("/tasks/{slno}")
async def get_task(slno: int):
    task = await retrieve_task_by_slno(slno)
    if task:
        return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{slno}")
async def update_task(slno: int, data: UpdateTask):
    updated = await update_task_by_slno(slno, data)
    if updated:
        return {"message": "Task updated successfully"}
    raise HTTPException(status_code=404, detail="Task not found or no fields to update")

@app.delete("/tasks/{slno}")
async def delete_task(slno: int):
    deleted = await delete_task_by_slno(slno)
    if deleted:
        return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")
