valueOfX(5).

!printValueAndIncrement.

+!printValueAndIncrement <-
!printValue;
!increment;
!printValue.

+!printValue: valueOfX(X) <-
.print(X).

+!increment: valueOfX(X) & X<10 <-
Y=X+1;
+valueOfX(Y);
-valueOfX(X).
