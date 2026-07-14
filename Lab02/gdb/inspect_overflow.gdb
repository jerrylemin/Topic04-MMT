set pagination off
set confirm off
set print pretty on
file build/vulnerable_debug
set args AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
break process_name
run
frame
info locals
p sizeof(name)
p &name
x/64bx &name
list
continue
backtrace
info registers
quit
