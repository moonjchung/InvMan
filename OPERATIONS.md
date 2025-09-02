# Operations

## Database Disaster Recovery

### Backups

The production database is hosted on Neon. To ensure data safety, Point-in-Time Recovery (PITR) must be enabled in the Neon project settings. This provides continuous backups and the ability to restore the database to any point within the retention period (e.g., 7 or 14 days). This is a manual setup step to be performed by the project administrator in the Neon console.
