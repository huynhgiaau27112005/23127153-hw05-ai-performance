$ErrorActionPreference = "Stop"
$Base = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$JMeter = "e:\DISK D\NOTES FOR CLASS\NAM 3\HOC KY III\TESTING\HOMEWORKS\tools\apache-jmeter-5.6.3\bin\jmeter.bat"
$SutBackend = "e:\DISK D\NOTES FOR CLASS\NAM 3\HOC KY III\TESTING\HOMEWORKS\eshop-sut\backend"
$Date = "20260830"
$Sid = "23127153"

Set-Location $Base

$ApiPort = "3010"
& "e:\DISK D\NOTES FOR CLASS\NAM 3\HOC KY III\TESTING\HOMEWORKS\scripts\reset-eshop-api.ps1" -Port ([int]$ApiPort)

python "$Base\scripts\generate_jmx.py"

python "$Base\scripts\seed_users.py"

$scenarios = @(
  @{ Name = "Load"; Jtl = "results\load\${Sid}_Load_${Date}.jtl"; Html = "results\load\html-report"; Plan = "test-plans\${Sid}_Load_${Date}.jmx" },
  @{ Name = "Stress"; Jtl = "results\stress\${Sid}_Stress_${Date}.jtl"; Html = "results\stress\html-report"; Plan = "test-plans\${Sid}_Stress_${Date}.jmx" },
  @{ Name = "Spike"; Jtl = "results\spike\${Sid}_Spike_${Date}.jtl"; Html = "results\spike\html-report"; Plan = "test-plans\${Sid}_Spike_${Date}.jmx" },
  @{ Name = "Endurance"; Jtl = "results\endurance\${Sid}_Endurance_${Date}.jtl"; Html = "results\endurance\html-report"; Plan = "test-plans\${Sid}_Endurance_${Date}.jmx" }
)

foreach ($s in $scenarios) {
  New-Item -ItemType Directory -Force -Path (Split-Path $s.Jtl) | Out-Null
  if (Test-Path $s.Html) { Remove-Item -Recurse -Force $s.Html }
  Write-Host "Running $($s.Name)..."
  $prevEap = $ErrorActionPreference
  $ErrorActionPreference = "Continue"
  cmd /c "`"$JMeter`" -n -t `"$Base\$($s.Plan)`" -l `"$Base\$($s.Jtl)`" -e -o `"$Base\$($s.Html)`" -Jjmeter.save.saveservice.output_format=csv 2>&1" | Out-File "$Base\results\$($s.Name.ToLower())\console.log"
  $ErrorActionPreference = $prevEap
}

Write-Host "Done all JMeter runs."
