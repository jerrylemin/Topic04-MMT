set pagination off
set confirm off
set print pretty on
file build/vulnerable_debug
set args "Le Minh"
break process_name
run
frame
info locals
p sizeof(name)
p &name
x/64bx &name
list
disassemble process_name
backtrace
continue
quit
