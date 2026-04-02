
# import os
# import random  # Added for random duration
# import time

# from azure.storage.queue import QueueClient


# def cpu_intensive_task(duration_seconds):
#     """
#     Runs a busy-wait loop to consume CPU for a given duration.
#     """
#     end_time = time.time() + duration_seconds
#     while time.time() < end_time:
#         # Perform a meaningless calculation to keep the CPU busy
#         _ = 12345 * 54321

# def process_message(message):
#     """
#     Processes a message by running a CPU-intensive task for a random time.
#     """
#     # Pick a random number between 1.0 and 3.0
#     duration = random.uniform(1, 3)
    
#     print(f"Processing message: {message} (Duration: {duration:.2f}s)")
    
#     # Burn CPU for that specific duration
#     cpu_intensive_task(duration)
    
#     print(f"Finished processing message: {message}")

# def main():
#     queue_name = "hieuduc231"
#     connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
#     queue_client = QueueClient.from_connection_string(connection_string, queue_name)
    
#     print("Worker started. Listening for messages...")
    
#     while True:
#         # Pull up to 5 messages at once
#         messages = queue_client.receive_messages(messages_per_page=5, visibility_timeout=30)
        
#         for msg in messages:
#             if msg:
#                 process_message(msg.content)
#                 queue_client.delete_message(msg)
        
#         # Short sleep to prevent hammering the API when empty
#         time.sleep(1)

# if __name__ == "__main__":
#     main()
# import os
# import random
# import sys
# import time

# from azure.storage.queue import QueueClient


# def cpu_intensive_task(duration_seconds):
#     """
#     Runs a busy-wait loop to consume CPU for a given duration.
#     """
#     end_time = time.time() + duration_seconds
#     while time.time() < end_time:
#         # Perform a meaningless calculation to keep the CPU busy
#         _ = 12345 * 54321

# def process_message(message):
#     """
#     Processes a message by running a CPU-intensive task for a random time.
#     """
#     # Pick a random number between 1.0 and 3.0
#     duration = random.uniform(1, 3)
    
#     # FIX: Added flush=True to force logs to appear immediately
#     print(f"Processing message: {message} (Duration: {duration:.2f}s)", flush=True)
    
#     # Burn CPU for that specific duration
#     cpu_intensive_task(duration)
    
#     # FIX: Added flush=True here as well
#     print(f"Finished processing message: {message}", flush=True)

# def main():
#     queue_name = "hieuduc231"
#     connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    
#     if not connection_string:
#         print("Error: AZURE_STORAGE_CONNECTION_STRING is not set.", flush=True)
#         return

#     queue_client = QueueClient.from_connection_string(connection_string, queue_name)
    
    
#     print("Worker started. Listening for messages...", flush=True)
    
#     while True:
#         # Pull up to 5 messages at once
#         messages = queue_client.receive_messages(messages_per_page=5, visibility_timeout=30)
        
#         for msg in messages:
#             if msg:
#                 process_message(msg.content)
#                 queue_client.delete_message(msg)
        
#         # Short sleep to prevent hammering the API when empty
#         time.sleep(1)

# if __name__ == "__main__":
#     main()
# import os
# import time

# from azure.storage.queue import QueueClient

# def cpu_intensive_task(duration_seconds):
#     """
#     Runs a busy-wait loop to consume CPU for a given duration.
#     """
#     end_time = time.time() + duration_seconds
#     while time.time() < end_time:
#         # Perform a meaningless calculation to keep the CPU busy
#         _ = 12345 * 54321

# def process_message(message):
#     """
#     Processes a message by running a CPU-intensive task.
#     """
#     print(f"Processing message: {message}")
#     # Instead of sleeping, we now burn CPU for ~2 seconds.
#     cpu_intensive_task(2)
#     print(f"Finished processing message: {message}")

# def main():
#     queue_name = "hieuduc231"
#     connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
#     queue_client = QueueClient.from_connection_string(connection_string, queue_name)
    
#     while True:
#         messages = queue_client.receive_messages(messages_per_page=5, visibility_timeout=30)
#         for msg in messages:
#             if msg:
#                 process_message(msg.content)
#                 queue_client.delete_message(msg)
#         # We can poll more frequently now that work takes time
#         time.sleep(1)

# if __name__ == "__main__":
#     main()
    
    
# import os
# import time

# from azure.storage.queue import QueueClient


# def process_message(message):
#     print(f"Processing message: {message}")
#     time.sleep(2)  # Simulating work

# def main():
#     queue_name = "hieuduc231"
#     connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
#     queue_client = QueueClient.from_connection_string(connection_string, queue_name)
    
#     while True:
#         messages = queue_client.receive_messages()
#         for msg in messages:
#             process_message(msg.content)
#             queue_client.delete_message(msg)
#         time.sleep(5)

# if __name__ == "__main__":
#     main()
import os
import random
import time
from concurrent.futures import ThreadPoolExecutor

from azure.storage.queue import QueueClient


def dynamic_workload_task(duration_seconds, math_iterations, sleep_time):
    """
    Dynamically balances CPU burn and I/O wait based on the message type.
    """
    end_time = time.time() + duration_seconds
    while time.time() < end_time:
        # Simulate CPU work
        for _ in range(math_iterations):
            _ = 12345 * 54321
            
        # Simulate I/O wait
        time.sleep(sleep_time)

def process_message(message):
    duration = random.uniform(1, 3)
    
    # Determine the "weight" of the message based on its duration
    if duration < 2.0:
        # LIGHT MESSAGE (1 to 2 seconds): Low CPU, High I/O wait
        math_iterations = 5000     # Very little math
        sleep_time = 0.1           # Long sleep
        print(f"[LIGHT] Processing message: {message} (Duration: {duration:.2f}s)", flush=True)
    else:
        # HEAVY MESSAGE (2 to 3 seconds): High CPU, Low I/O wait
        math_iterations = 150000   # Heavy math crunching
        sleep_time = 0.01          # Almost no sleep
        print(f"[HEAVY] Processing message: {message} (Duration: {duration:.2f}s)", flush=True)
        
    # Run the workload with the calculated intensity
    dynamic_workload_task(duration, math_iterations, sleep_time)
    
    print(f"Finished processing message: {message}", flush=True)

def main():
    queue_name = "hieuduc231"
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    
    if not connection_string:
        print("Error: AZURE_STORAGE_CONNECTION_STRING is not set.", flush=True)
        return

    queue_client = QueueClient.from_connection_string(connection_string, queue_name)
    print("Worker started. Listening for messages...", flush=True)
    
    executor = ThreadPoolExecutor(max_workers=5)
    
    while True:
        messages = queue_client.receive_messages(messages_per_page=5, visibility_timeout=30)
        
        futures = []
        for msg in messages:
            if msg:
                futures.append(executor.submit(process_message, msg.content))
                queue_client.delete_message(msg)
        
        for future in futures:
            future.result()
        
        time.sleep(1)

if __name__ == "__main__":
    main()