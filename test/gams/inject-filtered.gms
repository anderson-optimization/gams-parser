
set site(asset) /
**ao list asset "type startswith asset:land"
/;

set gen(asset) /
**ao list asset "type startswith asset:gen"
/;

set control_gen(gen) /
**ao list asset "type startswith asset:gen"
/;

set variable_gen(gen) / 
**ao list asset "type startswith asset:gen:renewable "
/;

set battery(gen) / 
**ao list asset "type startswith asset:battery "
/;