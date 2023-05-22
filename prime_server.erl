-module(prime_server).
-export([start/0, generate_prime/0]).

start() ->
    spawn(fun() -> init() end).

init() ->
    io:format("Server started.~n"),
    Worker1 = spawn(fun() -> worker() end),
    Worker2 = spawn(fun() -> worker() end),
    receive
        {generate_prime, Worker1, Worker2} ->
            Prime = generate_prime(),
            io:format("Generated prime number: ~p~n", [Prime]),
            Worker1 ! {prime_to_verify, Prime, self()},
            Worker2 ! {prime_to_verify, Prime, self()},
            wait_for_results(Prime, 0)
    end.

worker() ->
    io:format("Worker started.~n"),
    receive
        {prime_to_verify, Prime, Server} ->
            IsPrime = is_prime(Prime),
            Server ! {is_prime, self(), IsPrime}
    end.

wait_for_results(Prime, NumResults) ->
    wait_for_results(Prime, [], NumResults).

wait_for_results(Prime, Results, NumResults) when NumResults < 2 ->
    receive
        {is_prime, Worker, Result} ->
            io:format("Worker ~p says the number is ~s prime.~n", [Worker, Result]),
            wait_for_results(Prime, [Result | Results], NumResults + 1)
    end;
wait_for_results(Prime, Results, 2) ->
    io:format("All workers have responded.~n"),
    io:format("Final result: ~p is ~s prime.~n", [Prime, Result]),
    %% Additional logic based on the results can be added here.
    exit(normal).

generate_prime() ->
    %% Code to generate a large prime number goes here.
    %% You can use any algorithm of your choice.
    %% For simplicity, we'll return a small prime number in this example.
    17.

is_prime(N) ->
    %% Code to verify if N is prime goes here.
    %% You can use any algorithm of your choice.
    %% For simplicity, we'll return a result based on a small prime number in this example.
    case N of
        17 -> "is"
        _ -> "is not"
    end.
