import Pyro4

@Pyro4.expose
class PrimeWorker:
    def __init__(self):
        pass
    
    def find_primes(self, start, end):
        primes = []
        for i in range(start, end+1):
            for j in range(2, int(i**0.5)+1):
                if (i % j) == 0:
                    break
            else:
                primes.append(i)
        return primes

def main():
    worker = PrimeWorker()
    daemon = Pyro4.Daemon(host="192.168.83.46")
    uri = daemon.register(worker)
    ns = Pyro4.locateNS(host="192.168.83.205")
    ns.register("prime.worker1", uri)

    print("Prime worker 1 ready.")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
