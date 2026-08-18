set pagination off
set confirm off
set print pretty on
file build/secure_hardened
set args AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
break process_name
run
frame
info locals
p sizeof(name)
p &name
x/64bx &name
disassemble process_name
continue
backtrace
quit
