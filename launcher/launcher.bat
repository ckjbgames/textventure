@ECHO OFF
SETLOCAL EnableDelayedExpansion
REM textenture launcher
:select
    REM Equivalent to bash/ksh "select."
    SET count=1
    FOR /F %%option in ('echo %*') DO (
        ECHO %count%) %%option
        SET /A count+=1
    )
    SET /P choice="Enter Choice: "
EXIT /B %choice%
:menu1
    SET options=Login Help Quit
    SET chosen=%ERRORLEVEL
