# Demostración rápida de la API (ejecutar con el servidor encendido)
$h = @{ Authorization = "Bearer demo-token" }
$base = "http://127.0.0.1:8000"

Write-Host "`n1) Health check" -ForegroundColor Cyan
Invoke-RestMethod "$base/salud"

Write-Host "`n2) Sin token -> 401" -ForegroundColor Cyan
try { Invoke-RestMethod "$base/v1/tareas" } catch { "Estado: $($_.Exception.Response.StatusCode.value__)" }

Write-Host "`n3) Crear tarea -> 201" -ForegroundColor Cyan
$t = Invoke-RestMethod -Method Post "$base/v1/tareas" -Headers $h -ContentType "application/json" `
     -Body (@{ titulo = "Preparar exposición" } | ConvertTo-Json)
$t

Write-Host "`n4) Título inválido -> 422" -ForegroundColor Cyan
try { Invoke-RestMethod -Method Post "$base/v1/tareas" -Headers $h -ContentType "application/json" -Body '{"titulo":"a"}' }
catch { "Estado: $($_.Exception.Response.StatusCode.value__)" }

Write-Host "`n5) Completar tarea $($t.id)" -ForegroundColor Cyan
Invoke-RestMethod -Method Patch "$base/v1/tareas/$($t.id)/completar" -Headers $h

Write-Host "`n6) Listar tareas" -ForegroundColor Cyan
Invoke-RestMethod "$base/v1/tareas" -Headers $h
