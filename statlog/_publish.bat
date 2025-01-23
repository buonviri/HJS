@echo off

if exist C:\EdgeCortix\ (
  xcopy bmc.bat C:\EdgeCortix\bmc.bat /Y
  xcopy cfg.bat C:\EdgeCortix\cfg.bat /Y
  xcopy info.bat C:\EdgeCortix\info.bat /Y
  xcopy stats.bat C:\EdgeCortix\stats.bat /Y
  xcopy stats.bat C:\EdgeCortix\s2.bat /Y
  xcopy xlog.bat C:\EdgeCortix\xlog.bat /Y
) else (
  echo.
  echo.   'C:\EdgeCortix\' folder not found.
)
