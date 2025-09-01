process_flag(FileName) :-
    open(FileName, read, Stream),           
    read_string(Stream, _, Content),        
    close(Stream),                          
    string_codes(Content, Codes),           
    transform_codes(Codes, 1, Transformed),
    string_codes(NewString, Transformed),   
    writeln(NewString).                     


transform_codes([], _, []).
transform_codes([H|T], Index, [NewH|NewT]) :-
    NewH is H + Index,                      
    NextIndex is Index + 1,                  
    transform_codes(T, NextIndex, NewT).     


%EXECUTE
%?- process_flag('flag.txt').