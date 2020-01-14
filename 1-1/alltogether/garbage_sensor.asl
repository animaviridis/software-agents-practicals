locations([[5,6], [1,2], [3,3]]).

+!receive_query(Msg)[source(Sender)] <-
    .print("got a message from", Sender, "asking for garbage coordinates");
    !send_coordinates.

+!send_coordinates : locations([XY|T]) <-
    .print("Passing garbage coordinates: ", XY);
    -locations([H|T]);
    +locations(T);
    .send(garbage_collector, achieve, receive_coordinates(XY)).

+!send_coordinates : locations([]) <-
    .print("No more garbage");
    .send(garbage_collector, achieve, receive_coordinates([])).
