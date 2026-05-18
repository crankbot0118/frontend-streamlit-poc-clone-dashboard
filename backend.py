from fastapi import fastAPI

from db import (
    init_db_pool,
    get_connection,
    release_connection
)

app = FastAPI()

@app.on_event("startup")
async def startup():

    init_db_pool()

@app.get("/")
async def root():

    return {
        "status": "backend running"
    }

@app.post("/submit_job")
async def submit_job(payload: dict):
    connection = get_connection()

    cursor = connection.cursor()

    insert_query = """
        INSERT INTO job_list (
            job_name,
            target_instance,
            status
        )
        VALUES (
            %s,
            %s,
            %s
        )
    """
    cursor.execute(
        insert_query,
        (
            payload["job_name"],
            payload["target_instance"],
            "PENDING"
        )
    )  
    connection.commit()

    cursor.close()

    release_connection(connection)

    return {
        "message": "Job Submitted Successfully"
    }