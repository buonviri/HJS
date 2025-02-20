@echo off

if exist C:\EdgeCortix\ (
  xcopy bmc.bat C:\EdgeCortix\bmc.bat /Y
  xcopy cfg.bat C:\EdgeCortix\cfg.bat /Y
  xcopy info.bat C:\EdgeCortix\info.bat /Y
  xcopy stats.bat C:\EdgeCortix\stats.bat /Y
  xcopy stats.bat C:\EdgeCortix\s2.bat /Y
  xcopy xlog.bat C:\EdgeCortix\xlog.bat /Y
  xcopy 47.bat C:\EdgeCortix\47.bat /Y
  xcopy 55.bat C:\EdgeCortix\55.bat /Y
  xcopy 100.bat C:\EdgeCortix\100.bat /Y
  xcopy 110.bat C:\EdgeCortix\110.bat /Y
  xcopy 115.bat C:\EdgeCortix\115.bat /Y
  xcopy hex.bat C:\EdgeCortix\hex.bat /Y
) else (
  echo.
  echo.   'C:\EdgeCortix\' folder not found.
)
