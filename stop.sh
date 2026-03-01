#!/bin/bash

echo "🛑 Galéria Alkalmazás Leállítása..."
echo ""

# Stop and remove containers
docker compose down

echo ""
echo "✅ Alkalmazás sikeresen leállítva!"
echo ""
echo "💡 Tipp: Az adatok megmaradtak a volumes-ban"
echo "🗑️  Adatok törlése is: docker-compose down -v"
