valueOfX(0).

!printAndIncrement.

+!printAndIncrement: valueOfX(X) & X<10 <-
!printValue;
!increment;
!printAndIncrement.

+!printAndIncrement: valueOfX(X) & X>=10 <-
!printValue.

+!printValue: valueOfX(X) <-
.print(X).

+!increment: valueOfX(X) <-
Y=X+1;
+valueOfX(Y);
-valueOfX(X).
