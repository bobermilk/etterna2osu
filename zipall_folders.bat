@echo off
for /d %%i in (*) do (
 "C:\Program Files\7-Zip\7z.exe" a "%%i.zip" "%%i"
)
