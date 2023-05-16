-module(worker).
-export([start/0]).

start() ->
    Pid = spawn_link(fun() -> loop() end),
    register(worker, Pid).

loop() ->
    receive
        {check, N} ->
            Res = is_prime(N),
            sender ! {result, N, Res},
            loop()
    end.

is_prime(2) ->
    true;
is_prime(3) ->
    true;
is_prime(N) when N > 3 ->
    check_prime(N, 40).

check_prime(N, 0) ->
    false;
check_prime(N, K) ->
    A = rand:uniform(N-2) + 2,
    case fermat_test(A, N) of
        true ->
            check_prime(N, K-1);
        false ->
            false
    end.

fermat_test(A, N) ->
    case exp_mod(A, N-1, N) of
        1 ->
            true;
        _ ->
            false
    end.

exp_mod(_, 0, N) ->
    1;
exp_mod(Base, Exp, N) when Exp rem 2 =:= 0 ->
    Temp = exp_mod(Base, Exp div 2, N),
    (Temp * Temp) rem N;
exp_mod(Base, Exp, N) ->
    (Base * exp_mod(Base, Exp-1, N)) rem N.
