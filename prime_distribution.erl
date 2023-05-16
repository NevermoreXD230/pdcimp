-module(prime_distribution).
-export([calculate_primes/1]).

calculate_primes(UpperLimit) ->
    Workers = [worker1@myserver, worker2@myserver], % Replace with the actual worker node names
    Workloads = divide_workload(UpperLimit, Workers),
    Primes = calculate_primes_on_workers(Workloads, Workers),
    lists:flatten(Primes).

divide_workload(UpperLimit, Workers) ->
    RangeSize = UpperLimit div length(Workers),
    lists:zipwith(
        fun(Worker, Index) -> 
            {Worker, RangeSize * (Index - 1) + 1, RangeSize * Index} 
        end,
        Workers,
        lists:seq(1, length(Workers))
    ).

calculate_primes_on_workers(Workloads, Workers) ->
    lists:map(
        fun({Worker, Start, End}) ->
            Pid = spawn(Worker, worker:calculate_primes, [Start, End]),
            {Pid, Worker}
        end,
        Workloads
    ),
    receive_all(length(Workers)).

receive_all(0) ->
    [];
receive_all(N) ->
    receive
        {Pid, Primes} ->
            [Primes | receive_all(N - 1)]
    end.

