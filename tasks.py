from google.cloud import datastore

# Authorized service object
# For help authenticating your client, visit
# https://cloud.google.com/docs/authentication/getting-started
def create_client(project_id):
    return datastore.Client(project_id)


# Storing data

def add_task(client: datastore.Client, description: str):
    # Create an incomplete key for entity kind "Task".
    # So that an id will be generated automatically.
    key = client.key("Task")

    # Create an Entity object
    task = datastore.Entity(key, exclude_from_indexes=["description"])

    # Apply new field values and save the Task entity to Datastore
    task.update(
        {
            "created": datetime.datetime.utcnow(),
            "description": description,
            "done": False,
        }
    )
    client.put(task)

    return task.key

# A Method to update `done` property, to indicate the task is complete.

def mark_done(client: datastore.Client, task_id: Union[str, int]):
    with client.transaction():
        # Create a key for an entity of kind "Task", this is an immutable
        # representation
        key = client.key("Task", task_id)
        # Load entity with the key
        task = client.get(key)

        if not task:
            raise ValueError(f"Task {task_id} does not exist.")
        
        # Work done
        task["done"] = True

        # Persist the change back to Datastore
        client.put(task)


# Now delete `Task` entity, using the `Task` entity's key

def delete_task(client: datastore.Client, task_id: Union[str, int]):
    key = client.key("Task", task_id)
    # use the above key to delete associated document, if it exists
    client.delete(key)

# The query can also be done with 
# https://cloud.google.com/datastore/docs/reference/gql_reference
def list_tasks(client: datastore.Client):
    query = client.query(kind="Task")
    query.order = ["created"]

    return list(query.fetch())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--project-id", help="Google Cloud Project ID")

    args = parser.parse_args()

    client = create_client(args.project_id)
    args.func(client, args)
