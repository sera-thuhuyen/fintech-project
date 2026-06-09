# Config Notes

Place your Google Cloud service account JSON key in this folder, for example:

```text
config/service-account.json
```

Do not commit real credential files. The project `.gitignore` excludes common service account and credential filename patterns.

For local upload, run:

```powershell
python scripts/ingestion/upload_processed_to_gcs.py --credentials-file config/service-account.json
```

The service account needs permission to upload objects to the bucket, such as `Storage Object Admin` on `sera-fintech-bucket`.
