@ECHO OFF
SETLOCAL EnableDelayedExpansion
REM textenture launcher
REM Make sure MySQL is in %PATH%.
:select
    REM Equivalent to bash/ksh "select."
    SET count=1
    FOR /F %%option IN ('echo %*') DO (
        ECHO %count%) %%option
        SET /A count+=1
    )
    SET /P choice="Enter Choice: "
EXIT /B %choice%
:menu1
    SET options=Login Help Quit
    CALL :select %options%
    SET chosen=%ERRORLEVEL%
    IF %chosen%==1 (
        CALL :login
    ) ELSE IF %chosen%==2 (
        CALL :help
    ) ELSE IF %chosen%==3 (
        EXIT
    ) ELSE (
        ECHO Before you can use the launcher, you must know that there is no such option.
        CALL :menu1
    )
EXIT /B 0
