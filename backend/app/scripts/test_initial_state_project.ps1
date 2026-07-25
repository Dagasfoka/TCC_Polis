$ErrorActionPreference = "Stop"

$commands = @(
    "backend.app.scripts.create_db",
    "backend.app.scripts.seed_parties",
    "backend.app.scripts.seed_missions",
    "backend.app.scripts.seed_territories",
    "backend.app.scripts.create_demo_match"
)

foreach ($module in $commands) {
    Write-Host ""
    Write-Host "Executando: $module"

    docker compose exec -T api python -m $module

    if ($LASTEXITCODE -ne 0) {
        Write-Error "Erro ao executar: $module"
        exit $LASTEXITCODE
    }
}

Write-Host ""
Write-Host "Banco e partida de demonstração preparados com sucesso."