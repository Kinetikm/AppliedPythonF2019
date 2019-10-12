from multiprocessing import Process, Queue

queue = Queue()

queue.put("132/")
queue.put("345")

print(queue.get())
print(queue.get())
