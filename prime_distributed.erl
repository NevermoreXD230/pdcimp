-module(prime_distributed).
-export([main/2, worker/1]).

main(N, P) ->
    {StartTime, _} = erlang:statistics(wall_clock),
    Res = master(N, P),
    {EndTime, _} = erlang:statistics(wall_clock),
    Time = EndTime - StartTime,
    io:format("Total time taken: ~p ms.~n", [Time]),
    Res.

master(N, P) ->
    Workers = spawn_workers(P),
    ChunkSize = N div P,
    Extra = N rem P,
    Jobs = build_jobs(Workers, ChunkSize, Extra),
    [W ! {self(), Job} || {W, Job} <- Jobs],
    Results = collect_results(P, []),
    lists:foldl(fun(Acc, X) -> Acc + X end, 0, Results).

spawn_workers(P) ->
    lists:map(fun(_) -> spawn(?MODULE, worker, []) end, lists:seq(1, P)).

build_jobs(Workers, ChunkSize, Extra) ->
    Jobs = lists:duplicate(ChunkSize, 0),
    case Extra of
        0 ->
            fill_jobs(Jobs, Workers);
        _ ->
            fill_jobs(Jobs ++ [0], Workers) ++ [fill_jobs([0], Workers)]
    end.

fill_jobs(Jobs, Workers) ->
    lists:zip(Workers, lists:map(fun(List) -> [fermet:is_prime(N) || N <- List] end, split_list(Jobs))).

split_list(List) ->
    case lists:split(length(List) div 2, List) of
        {Left, []} ->
            [Left];
        {Left, Right} ->
            [Left | split_list(Right)]
    end.

collect_results(0, Acc) ->
    lists:reverse(Acc);
collect_results(P, Acc) ->
    receive
        {_, Result} ->
            collect_results(P-1, [Result|Acc])
    end.

worker() ->
    receive
        {Master, [P1, P2|Ps]} ->
            Master ! {self(), [fermet:is_prime(P1), fermet:is_prime(P2)]},
            worker();
        {Master, [P]} ->
            Master ! {self(), [fermet:is_prime(P)]},
            worker();
        stop ->
            ok
    end.
