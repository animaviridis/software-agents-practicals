location([5,6]).

+!give_coordinates(Msg)[source(Sender)] : location(XY) <-
    .print("got a message from", Sender, "asking for garbage coordinates");
    .print("Passing garbage coordinates: ", XY);
    .send(garbage_collector, achieve, receive_coordinates(XY)).
