import gevent
import gipc

def writelet(w):
    # This function runs as a greenlet in the parent process.
    # Put a Python object into the write end of the pipe.
    w.put(0)


def readchild(r):
    # This function runs in a child process.
    # Read object from the read end of the pipe and confirm that it is the
    # expected one.
    assert r.get() == 0


def main():
    with gipc.pipe() as (readend, writeend):
        # Start 'writer' greenlet. Provide it with the pipe write end.
        g = gevent.spawn(writelet, writeend)
        # Start 'reader' child process. Provide it with the pipe read end.
        p = gipc.start_process(target=readchild, args=(readend,))
        # Wait for both to finish.
        g.join()
        p.join()


# Protect entry point from being executed upon import (this matters
# on Windows).
if __name__ == "__main__":
    main()