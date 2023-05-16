-module(prime_distributed).

-export([start/2, master/4, worker/1, is_prime/1]).

start(N, NumOfWorkers) ->
    spawn(prime_distributed, master, [N, NumOfWorkers, self(), []]).

master(N, NumOfWorkers, Parent, PrimeList) ->
    K = trunc(math:sqrt(N))+1,
    Lists = lists:foldl(
        fun(K_, Lists_) ->
            Start = (K_-1)*K + 1,
            End = K_*K,
            [ {Start_, End_} || Start_ <- lists:seq(Start, N, K_), End_ <- lists:seq(Start_, min(End, N)), Start_ =< End_ ] ++ Lists_
        end,
        [], lists:seq(1,K)),
    Workers = [ spawn(prime_distributed, worker, []) || _ <- lists:seq(1,NumOfWorkers)],
    spawn_link(prime_distributed, collector, [Parent, length(Lists), PrimeList]),
    lists:foreach(
        fun(List_) ->
            {Worker, WorkersRest} = lists:split(1, Workers),
            Worker ! {self(), List_},
            Workers = WorkersRest
        end,
        Lists),
    ok.

worker() ->
    receive
        {Parent, {Start, End}} ->
            Parent ! {self(), [ N || N <- lists:seq(Start,End), is_prime(N) =:= true ]}
    end,
    worker().

collector(Parent, NumOfWorkers, PrimeList) ->
    receive
        {From, List} ->
            collector(Parent, NumOfWorkers, PrimeList ++ List);
        {'EXIT', _, _} ->
            {_, WorkersRest} = lists:split(1, lists:droplast(NumOfWorkers, [spawn(prime_distributed, worker, []) || _ <- lists:seq(1,NumOfWorkers) ])),
            lists:foreach(
                fun(Worker_) -> Worker_ ! stop end,
                WorkersRest),
            exit(killed)
    after
        5000 ->
            {_, WorkersRest} = lists:split(1, lists:droplast(NumOfWorkers, [spawn(prime_distributed, worker, []) || _ <- lists:seq(1,NumOfWorkers) ])),
            lists:foreach(
                fun(Worker_) -> Worker_ ! stop end,
                WorkersRest),
            exit(timeout)
    end,
    Parent ! {primes, PrimeList},
    exit(normal).

is_prime(N) when N > 1 ->
    is_prime(N, 2, trunc(math:sqrt(N))+1).

is_prime(N, K, Max) when K < Max ->
    case N rem K of
        0 -> false;
        _ -> is_prime(N, K+1, Max)
    end;
is_prime(_, _, _) ->
    true.
