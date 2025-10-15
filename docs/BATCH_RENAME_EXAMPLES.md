# Batch Rename Feature Usage Examples

This document provides examples of how to use the Batch Rename TV Series feature.

## Example Scenario

You have ripped multiple discs from the Breaking Bad TV series and ARM has created folders like:
- `Breaking Bad (2008)`
- `Breaking Bad (2008)_1704735891`
- `Breaking Bad (2008)_1704735923`
- `Breaking Bad (2008)_1704735967`

The disc labels were:
- `BREAKING_BAD_S01_D1`
- `BREAKING_BAD_S01_D2` 
- `BREAKING_BAD_S02_D1`
- `BREAKING_BAD_S02_D2`

## Using Batch Rename

### Step 1: Navigate to Batch Rename
Click "Batch Rename" in the main navigation menu.

### Step 2: Select Jobs
Check the boxes for all the Breaking Bad jobs you want to rename.

### Step 3: Analyze Selection
Click "Analyze Selection". The system will:
- Detect the common series name: "Breaking Bad"
- Show no conflicts since all jobs are from the same series
- Display the suggested series name in the input field

### Step 4: Choose Naming Option

**Option A: Use Detected Name**
- Keep "Breaking Bad" in the series name field
- Leave "Use Custom Name Instead" unchecked

**Option B: Use Custom Name**
- Check "Use Custom Name Instead"
- Enter your preferred name, e.g., "Breaking-Bad" or "BB"

### Step 5: Preview Changes
Click "Preview Changes" to see:
```
Current → New
Breaking Bad (2008) → Breaking-Bad_BREAKING-BAD-S01-D1
Breaking Bad (2008)_1704735891 → Breaking-Bad_BREAKING-BAD-S01-D2
Breaking Bad (2008)_1704735923 → Breaking-Bad_BREAKING-BAD-S02-D1
Breaking Bad (2008)_1704735967 → Breaking-Bad_BREAKING-BAD-S02-D2
```

### Step 6: Execute Rename
Click "Execute Rename" to perform the actual folder renaming.

## Result

Your folders are now consistently named:
- `Breaking-Bad_BREAKING-BAD-S01-D1`
- `Breaking-Bad_BREAKING-BAD-S01-D2`
- `Breaking-Bad_BREAKING-BAD-S02-D1`
- `Breaking-Bad_BREAKING-BAD-S02-D2`

This makes it much easier to:
1. Identify which disc contains which episodes
2. Use external tools for batch episode renaming
3. Organize your media library

## Conflict Resolution Example

If you accidentally select jobs from different series:
- Breaking Bad discs
- Game of Thrones discs

The system will:
1. Show a warning about multiple series names detected
2. List all detected series: "Breaking Bad, Game of Thrones"
3. Allow you to choose the correct series name or use a custom name

You can then either:
- Deselect jobs from one series and proceed
- Use a custom name like "Mixed-Series" if you really want to group them

## Advanced Use Cases

### Custom Naming for Season Organization
If you want to organize by season, you could:
1. Select all Season 1 discs
2. Use custom name: "Breaking-Bad-Season-01"
3. Result: `Breaking-Bad-Season-01_BREAKING-BAD-S01-D1`, etc.

### Fixing Inconsistent Labels
If disc labels are inconsistent or missing:
1. The system falls back to using job IDs
2. Result: `Breaking-Bad_123`, `Breaking-Bad_124`, etc.
3. You can then manually rename these as needed

## Error Handling

The system handles various error conditions:

### Target Already Exists
```
Error: Target path already exists: /media/tv/Breaking-Bad_BREAKING-BAD-S01-D1
```

### Permission Issues
```
Error: Permission denied when renaming /media/tv/Breaking Bad (2008)
```

### Missing Paths
```
Error: Path does not exist: /media/tv/Breaking Bad (2008)
```

Each error is reported individually, allowing successful renames to proceed while flagging problems.