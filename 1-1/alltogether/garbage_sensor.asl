locations([[5,6], [1,2], [3,3]]).

!dosomething.

+!dosomething : locations([H|T]) <-
    .print(H);
    -locations([H|T]);
    +locations(T);
    !dosomething.

+!dosomething : locations([]) <-
    .print("finished").

+!give_coordinates(Msg)[source(Sender)] : location(XY) <-
    .print("got a message from", Sender, "asking for garbage coordinates");
    .print("Passing garbage coordinates: ", XY);
    .send(garbage_collector, achieve, receive_coordinates(XY)).
