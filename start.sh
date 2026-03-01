#!/bin/bash

echo "🚀 Galéria Alkalmazás Indítása..."
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker nincs telepítve. Kérlek telepítsd a Docker-t!"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker compose &> /dev/null; then
    echo "❌ Docker Compose nincs telepítve. Kérlek telepítsd a Docker Compose-t!"
    exit 1
fi

echo "✅ Docker és Docker Compose telepítve"
echo ""

# Stop existing containers
echo "🛑 Meglévő konténerek leállítása..."
docker compose down

# Build and start containers
echo "🔨 Konténerek építése és indítása..."
docker compose up --build -d

echo ""
echo "⏳ Várakozás az alkalmazás indulására..."
sleep 10

# Check if containers are running
if docker compose ps | grep -q "Up"; then
    echo ""
    echo "✅ Alkalmazás sikeresen elindult!"
    echo ""
    echo "📱 Alkalmazás elérhetőségek:"
    echo "   Frontend:  http://localhost:5173"
    echo "   Backend:   http://localhost:5000"
    echo "   Database:  localhost:5432"
    echo ""
    echo "📋 Logok megtekintése: docker-compose logs -f"
    echo "🛑 Leállítás: docker-compose down"
    echo ""
    echo "🌐 Nyisd meg a böngészőt: http://localhost:5173"
else
    echo ""
    echo "❌ Hiba történt az indítás során!"
    echo "📋 Nézd meg a logokat: docker-compose logs"
fi
