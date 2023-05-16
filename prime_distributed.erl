% prime_distributed.erl

-module(prime_distributed).

-export([start/1, start_worker/0, is_prime/1, primes/2]).

start_worker() ->
    register(worker, spawn(fun() -> worker() end)).

worker() ->
    receive
        {From, {is_prime, N}} ->
            Res = is_prime(N),
            From ! {self(), {is_prime, Res}}
    end,
    worker().

start(N) ->
    start_worker(),
    {_, Workers} = lists:foldl(
        fun(_, {Id, Workers}) ->
            {Id+1, [spawn(worker, worker, []) | Workers]}
        end,
        {1, []},
        lists:seq(1, N)
    ),
    lists:foreach(
        fun(Worker) ->
            Worker ! {self(), {is_prime, 2}}
        end,
        Workers
    ),
    primes(Workers, 3).

primes([], _) ->
    ok;
primes(Workers, N) ->
    receive
        {Worker, {is_prime, Res}} ->
            case Res of
                true ->
                    io:format("~p is prime~n", [N]);
                false ->
                    ok
            end,
            Worker ! {self(), {is_prime, N+2}},
            primes(Workers, N+2)
    end.
