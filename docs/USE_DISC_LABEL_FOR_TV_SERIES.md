# Using DVD Label for TV Series Output Folder Names

By default, ARM uses the series title looked up from online databases as the output folder name for TV series. When ARM encounters a TV series disc that already has a folder, it creates a new folder with a timestamp suffix (e.g., `Series Name_123456789`). This can make batch episode renaming difficult.

This feature allows ARM to use the DVD/Blu-ray label (disc volume name) as the output folder name specifically for TV series, making it easier to organize and batch rename episodes using external tools.

## Configuration

To enable this feature, set the following option in your `arm.yaml` configuration file:

```yaml
USE_DISC_LABEL_FOR_TV_SERIES: true
```

## Behavior

- **When enabled (`true`)**: For TV series only, the DVD label (disc volume name) will be used as the output folder name. The label will be cleaned to remove invalid filename characters.
- **When disabled (`false`, default)**: The series title from database lookup will be used as the output folder name, and duplicate folders will get timestamp suffixes.
- **Movies are not affected**: This setting only applies to content identified as TV series (`video_type: "series"`).

## Examples

### Default behavior (USE_DISC_LABEL_FOR_TV_SERIES: false):
- DVD label: "BREAKING_BAD_S01_D1"
- Series title lookup: "Breaking Bad"
- Year: "2008"
- First disc output folder: `Breaking Bad (2008)`
- Second disc output folder: `Breaking Bad (2008)_123456789` *(timestamp suffix)*

### With disc label enabled for TV series (USE_DISC_LABEL_FOR_TV_SERIES: true):
- DVD label: "BREAKING_BAD_S01_D1"
- Output folder: `BREAKING-BAD-S01-D1`
- DVD label: "BREAKING_BAD_S01_D2" 
- Output folder: `BREAKING-BAD-S01-D2`

This creates unique, descriptive folder names for each disc that can be easily batch processed with episode renaming tools.

## Use Cases

This feature is particularly useful when:
- Ripping TV series with multiple discs per season
- Episodes on the disc are not properly labeled or identified
- You want to use external tools to match and rename episodes after ripping
- You need to avoid timestamp-based duplicate folder names
- The disc labels contain useful information (season/disc numbers, etc.)

## Notes

- Only applies to content identified as TV series (`video_type: "series"`)
- Movies continue to use the standard title-based naming
- The disc label is automatically cleaned to remove special characters and replace them with filename-safe alternatives
- If the disc has no label or the label is empty, ARM will fall back to the default behavior (series title)
- This setting affects both the transcode path and the final completed path
- The feature works for both DVDs and Blu-rays

## Configuration via Web UI

You can also change this setting through the ARM web interface:
1. Navigate to Settings
2. Go to the "Ripper Settings" tab
3. Find "USE_DISC_LABEL_FOR_TV_SERIES" and set it to your desired value
4. Click Submit to save the changes