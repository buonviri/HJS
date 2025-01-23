@echo off

if exist C:\EdgeCortix\ (
  xcopy bmc.bat C:\EdgeCortix\bmc.bat /Y /-I
  xcopy cfg.bat C:\EdgeCortix\cfg.bat /Y /-I
  xcopy info.bat C:\EdgeCortix\info.bat /Y /-I
  xcopy stats.bat C:\EdgeCortix\stats.bat /Y /-I
  xcopy stats.bat C:\EdgeCortix\s2.bat /Y /-I
  xcopy xlog.bat C:\EdgeCortix\xlog.bat /Y /-I
) else (
  echo.
  echo.   'C:\EdgeCortix\' folder not found.
)
