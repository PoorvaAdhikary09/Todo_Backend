from database import task_collection
from model import Task, UpdateTask
from datetime import datetime, date

def task_helper(task) -> dict:
    return {
        "slno": task["slno"],
        "title": task["title"],
        "due_date": task["due_date"].strftime("%Y-%m-%d") if task["due_date"] else None,
        "completed": task["completed"]
    }

# Create
async def add_task(task_data: Task) -> dict:
    task_dict = task_data.dict()
    task_dict["due_date"] = datetime.combine(task_dict["due_date"], datetime.min.time())

    # Check if slno already exists
    existing = await task_collection.find_one({"slno": task_dict["slno"]})
    if existing:
        raise ValueError("Serial number already exists.")
    
    await task_collection.insert_one(task_dict)
    return task_helper(task_dict)

# Read all
async def retrieve_tasks():
    tasks = []
    async for task in task_collection.find():
        tasks.append(task_helper(task))
    return tasks

# Read one
async def retrieve_task_by_slno(slno: int):
    task = await task_collection.find_one({"slno": slno})
    if task:
        return task_helper(task)

# Update
async def update_task_by_slno(slno: int, data: UpdateTask):
    data = {k: v for k, v in data.dict().items() if v is not None}
    if "due_date" in data and isinstance(data["due_date"], date):
        data["due_date"] = datetime.combine(data["due_date"], datetime.min.time())
    
    if not data:
        return False
    
    updated = await task_collection.update_one({"slno": slno}, {"$set": data})
    return updated.modified_count > 0

# Delete
async def delete_task_by_slno(slno: int):
    deleted = await task_collection.delete_one({"slno": slno})
    return deleted.deleted_count > 0
