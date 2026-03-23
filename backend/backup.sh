#!/bin/bash
# Backup database and media files

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="backups"

mkdir -p $BACKUP_DIR

# Backup SQLite database
if [ -f "db.sqlite3" ]; then
    cp db.sqlite3 "$BACKUP_DIR/db_backup_$TIMESTAMP.sqlite3"
    echo "✓ Database backup created: $BACKUP_DIR/db_backup_$TIMESTAMP.sqlite3"
fi

# Backup media files
if [ -d "media" ]; then
    tar -czf "$BACKUP_DIR/media_backup_$TIMESTAMP.tar.gz" media/
    echo "✓ Media backup created: $BACKUP_DIR/media_backup_$TIMESTAMP.tar.gz"
fi

# Keep only last 10 backups
find $BACKUP_DIR -type f -name "db_backup_*.sqlite3" | sort -r | tail -n +11 | xargs rm -f
find $BACKUP_DIR -type f -name "media_backup_*.tar.gz" | sort -r | tail -n +11 | xargs rm -f

echo "Backup complete!"
