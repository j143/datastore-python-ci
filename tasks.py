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
