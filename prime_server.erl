-module(prime_server).
-export([start/0, generate_prime/0]).

start() ->
    spawn(fun() -> init() end).

init() ->
    io:format("Server started.~n"),
    receive
        {generate_prime, Worker1, Worker2} ->
            Prime = generate_prime(),
            io:format("Generated prime number: ~p~n", [Prime]),
            Worker1 ! {prime_to_verify, Prime, self()},
            Worker2 ! {prime_to_verify, Prime, self()},
            wait_for_results(Prime)
    end.

wait_for_results(Prime) ->
    wait_for_results(Prime, [], 0).

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
