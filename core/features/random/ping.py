import time

def Ping(voice):
    """Sends a 'Pong' voice message and measures response time."""
    start = time.perf_counter()
    voice.say("Pong!")
    end = time.perf_counter()
    elapsed_ms = round((end - start) * 1000, 2)
    return elapsed_ms
