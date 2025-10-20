# Batch Rename TV Series Feature

This feature allows users to select multiple completed TV series discs and rename their output folders to use a consistent naming scheme that includes the series name and disc label.

## Purpose

When ARM rips multiple discs from a TV series, it often creates folders with timestamp suffixes (e.g., `Series Name_123456789`) when the same series name is detected. This makes it difficult to batch rename episodes later using external tools.

The batch rename feature solves this by allowing you to:
1. Select multiple completed TV series jobs
2. Use a common series name for all selected jobs
3. Append the disc label to create unique folder names (e.g., `Breaking_Bad_S01_D01`)

## How It Works

### Access
Navigate to **Batch Rename** from the main navigation menu.

### Workflow
1. **Select Jobs**: Check the boxes for the TV series jobs you want to rename
2. **Analyze Selection**: Click "Analyze Selection" to detect the series name and check for conflicts
3. **Choose Series Name**: 
   - Use the detected series name, or
   - Check "Use Custom Name Instead" to specify your own series name
4. **Preview Changes**: Click "Preview Changes" to see what the new folder names will be
5. **Execute Rename**: Click "Execute Rename" to perform the actual folder renaming

### Naming Pattern
The new folder names follow this pattern:
```
[SeriesName]_[DiscLabel]
```

For example:
- Original: `Breaking Bad (2008)` → New: `Breaking-Bad_BREAKING_BAD_S01_D1`
- Original: `Game of Thrones (2011)_123456789` → New: `Game-of-Thrones_GOT_S01_DISC1`

## Features

### Conflict Detection
If you select jobs with different series names, the system will warn you and allow you to choose the correct series name.

### Custom Naming
You can override the detected series name with a custom name of your choice.

### Preview Mode
See exactly what the changes will be before executing them.

### Safety Checks
- Validates that target folders don't already exist
- Shows detailed results for each rename operation
- Handles errors gracefully (e.g., missing paths, permission issues)

## Requirements

- Only completed TV series jobs (status: 'success', video_type: 'series') are shown
- Jobs must have valid output paths
- Disc labels are used for generating unique folder names

## API Endpoints

The feature provides several API endpoints for the frontend:

- `GET /batch_rename` - Main batch rename page
- `POST /get_series_info` - Analyze selected jobs for series information
- `POST /preview_rename` - Preview what the new names will be
- `POST /execute_rename` - Execute the batch rename operation

## Technical Implementation

The feature is implemented as a Flask blueprint in `arm/ui/batch_rename/` with:
- `batch_rename.py` - Main route handlers and API logic
- `templates/batch_rename.html` - Frontend interface
- Integration with existing ARM models and utilities

## Database Changes

The feature updates the following fields in renamed jobs:
- `job.path` - Updated to the new folder path
- `job.title_manual` - Updated when using custom series names

## Error Handling

The system provides detailed error reporting for:
- Missing or invalid paths
- Permission issues
- Target folders that already exist
- Database update failures

Each operation shows success/failure status with specific error messages when needed.