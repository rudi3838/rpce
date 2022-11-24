Der folgende Algorithmus schreibt die Elemente von f1 f2- Mal in f3.

Über dem Start des Algorithmus können beliebig viele Zeilen geschrieben werden.

algorithm Extract ( \i f1 \i  f2 \i l \o f3 \i l3)
param char f1[1…l];
             int f2[1…l];
             int l;
             int f3[1…l3];
             int l3;
local int counter = 0;
         int curpos = 1;
         int counter2 = 0;
         int endpos = 0;
         char value = ‘‘;

   for counter = 1 to l do
      endpos = curpos + f2[counter];
      value = f1[counter];
      for counter2 = curpos to endpos do
            f3[counter2] = value;
            curpos = curpos + 1;
      end
   end
end
