from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from src.app.core.config import client
from src.app.schemas.task import Task, TaskCreate, TaskUpdate

router = APIRouter()

db = client["apirest"]
collection = db["tasks"]

# Helper para converter ObjectId
def task_helper(task) -> dict:
    task["_id"] = str(task["_id"])
    return task

@router.post("/", response_model=Task, summary="Criar uma nova tarefa")
async def create_task(task: TaskCreate):
    result = await collection.insert_one(task.dict())
    new_task = await collection.find_one({"_id": result.inserted_id})
    return task_helper(new_task)

@router.get("/", response_model=list[Task], summary="Listar todas as tarefas")
async def list_tasks():
    tasks = []
    cursor = collection.find()
    async for task in cursor:
        tasks.append(task_helper(task))
    return tasks

@router.get("/{task_id}", response_model=Task, summary="Buscar uma tarefa pelo ID")
async def get_task(task_id: str):
    task = await collection.find_one({"_id": ObjectId(task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return task_helper(task)

@router.put("/{task_id}", response_model=Task, summary="Atualizar uma tarefa")
async def update_task(task_id: str, task_data: TaskUpdate):
    result = await collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": task_data.dict(exclude_unset=True)}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    task = await collection.find_one({"_id": ObjectId(task_id)})
    return task_helper(task)

@router.delete("/{task_id}", status_code=204, summary="Deletar uma tarefa")
async def delete_task(task_id: str):
    result = await collection.delete_one({"_id": ObjectId(task_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return None
