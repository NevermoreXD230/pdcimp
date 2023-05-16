-module(prime_distributed).
-export([start/1, stop/0, process/2]).

start(Workers) ->
    spawn(fun() -> loop(Workers) end).

stop() ->
    self() ! stop.

process(N, Client) ->
    self() ! {process, N, Client},
    receive
        {result, P} ->
            Client ! {result, P}
    end.

loop(Workers) ->
    receive
        {process, N, Client} ->
            spawn(fun() -> handle(N, Client, Workers) end),
            loop(Workers);
        stop ->
            ok
    end.

handle(N, Client, [Worker | Rest]) ->
    case rpc:call(Worker, fermat, process, [N]) of
        {ok, P} ->
            Client ! {result, P},
            Worker ! {free, self()},
            loop([Worker | Rest]);
        _ ->
            handle(N, Client, Rest)
    end;
handle(_, _, []) ->
    ok.

