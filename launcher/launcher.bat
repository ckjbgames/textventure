@ECHO OFF
SETLOCAL
rem textenture launcher
:select
    SET count=1
    rem Equivalent to bash/ksh "select."
    FOR /F %%option in ('echo %*') DO (
        ECHO %count%) %%option
        SET /A count+=1
    )
