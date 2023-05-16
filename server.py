import Pyro4

@Pyro4.expose
class PrimeServer:
    def __init__(self):
        self.workers = []
    
    def add_worker(self, worker_uri):
        self.workers.append(worker_uri)
    
    def find_primes(self, start, end):
        primes = []
        for i in range(start, end+1):
            for j in range(2, int(i**0.5)+1):
                if (i % j) == 0:
                    break
            else:
                primes.append(i)
        return primes

    def distribute_workload(self, start, end):
        workload_size = (end - start) // len(self.workers)
        start_range = start
        end_range = start_range + workload_size

        jobs = []
        for worker_uri in self.workers:
            jobs.append((worker_uri, start_range, end_range))
            start_range = end_range + 1
            end_range = start_range + workload_size

        # Handle remainder workload
        if end_range - 1 < end:
            jobs[-1] = (jobs[-1][0], jobs[-1][1], end)

        results = []
        for worker_uri, start, end in jobs:
            worker = Pyro4.Proxy(worker_uri)
            result = worker.find_primes(start, end)
            results.extend(result)
        
        return results

def main():
    server = PrimeServer()
    daemon = Pyro4.Daemon(host="192.168.83.205")
    uri = daemon.register(server)
    ns = Pyro4.locateNS(host="192.168.83.205")
    ns.register("prime.server", uri)

    print("Prime server ready.")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
