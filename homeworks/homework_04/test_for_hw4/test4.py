import os
print("Test4")
os.system(f"Taskkill /PID {os.getpid()} /F")
