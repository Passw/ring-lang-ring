rem Building Ring Compiler/VM using Zig
rem Tested using zig-x86_64-windows-0.16.0-dev.178+b1189ab03
rem Add Zig to your path, then run this batch file to build ring.exe

cd ..\src 

zig cc -Ofast ring.c general.c state.c ext.c hashlib.c rhtable.c vmgc.c os_e.c rstring.c rlist.c ritem.c ritems.c scanner.c parser.c stmt.c expr.c codegen.c vm.c vmerror.c vmeval.c vmthread.c vmexpr.c vmvars.c vmlists.c vmfuncs.c ringapi.c vmoop.c  vmtry.c vmstr.c vmjump.c vmrange.c list_e.c meta_e.c vminfo_e.c vmperf.c vmexit.c vmstack.c vmstate.c genlib_e.c math_e.c file_e.c dll_e.c objfile.c -I ../include -o ring.exe -lm 
copy ring.exe ..\..\bin\ring.exe


cd ..\build 
