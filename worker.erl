-module(worker).
-export([start/1]).

start(Server) ->
    register(worker, spawn(fun() -> loop(Server) end)).

loop(Server) ->
    receive
        {work, N} ->
            Result = is_prime(N),
            Server ! {result, self(), Result},
            loop(Server);
        stop ->
            ok
    end.

is_prime(N) ->
    R = rand:uniform(N-1) + 1,
    fermat(N, R).

fermat(N, A) ->
    case mod_exp(A, N-1, N) of
        1 ->
            true;
        _ ->
            false
    end.

mod_exp(_, 0, Mod) ->
    1;
mod_exp(Base, Exp, Mod) ->
    case Exp rem 2 of
        0 ->
            Temp = mod_exp(Base, Exp div 2, Mod),
            (Temp * Temp) rem Mod;
        1 ->
            (Base * mod_exp(Base, Exp - 1, Mod)) rem Mod
    end.
