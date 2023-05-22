-module(prime_worker).
-export([start/0]).

start() ->
    spawn(fun() -> init() end).

init() ->
    io:format("Worker started.~n"),
    receive
        {prime_to_verify, Prime, Server} ->
            IsPrime = is_prime(Prime),
            Server ! {is_prime, self(), IsPrime}
    end.

is_prime(N) ->
    %% Code to verify if N is prime goes here.
    %% You can use any algorithm of your choice.
    %% For simplicity, we'll return a result based on a small prime number in this example.
    case N of
        17 -> "is"
        _ -> "is not"
    end.
