-module(prime_worker).
-export([start/1]).

start(ServerIP) ->
    spawn(fun() -> init(ServerIP) end).

init(ServerIP) ->
    io:format("Worker started.~n"),
    Server = get_server(ServerIP),
    receive
        {prime_to_verify, Prime, Server} ->
            IsPrime = is_prime(Prime),
            Server ! {is_prime, self(), IsPrime}
    end.

get_server(ServerIP) ->
    {ok, Server} = net_adm:world(),
    {ok, ServerPID} = net_kernel:connect_node(ServerIP),
    ServerPID.

is_prime(N) ->
    %% Code to verify if N is prime goes here.
    %% You can use any algorithm of your choice.
    %% For simplicity, we'll return a result based on a small prime number in this example.
    case N of
        17 -> "is"
        _ -> "is not"
    end.
