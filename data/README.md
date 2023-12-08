# Data Folder

## Overview

This `data` folder is a central location for managing and organizing point cloud data and related processing logs in our project. It is crucial for maintaining a structured and efficient workflow.

## Data Storage

### Point Cloud Data

- All point cloud data files should be placed directly in this `data` folder.
- Supported data file formats include `.pcd`, `.ply`, `.las`, etc.
- Ensure that the data files are named appropriately to reflect their content or source.

### Log Files

- Log files generated during point cloud processing are automatically saved in this folder.
- Each log file is associated with a specific data file and processing session.
- Logs are stored in subfolders named according to the convention `{filename}_{timestamp}`.

## Folder Structure
```
data/
│
├── your_data_file_1.pcd
├── your_data_file_2.las
│
├── your_data_file_1_20210101_120000/
│ ├── noise_filter_log.txt
│ ├── ground_filter_log.txt
│ └── ...
│
├── your_data_file_2_20210102_123000/
├── noise_filter_log.txt
├── ground_filter_log.txt
└── ...
```

## Guidelines

1. **Placing Data**: When adding new point cloud data files, place them directly in the `data` folder without creating additional subfolders for individual data files.

2. **Running Processes**: When executing point cloud processing scripts, ensure they are configured to access and save data in this `data` folder.

3. **Reviewing Logs**: After processing, check the respective `{filename}_{timestamp}` subfolder for logs to review the processing results, parameters used, and any potential issues.

4. **Archiving Data**: For long-term storage or backup, consider archiving the entire `data` folder, including both point cloud data and associated log subfolders.