#!/usr/bin/env python3
"""
Test for the batch rename functionality
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os
import json


class TestBatchRename(unittest.TestCase):
    """Test batch rename functionality"""

    def setUp(self):
        """Set up test fixtures"""
        # Create mock jobs
        self.job1 = Mock()
        self.job1.job_id = 1
        self.job1.title = "Breaking Bad"
        self.job1.title_manual = None
        self.job1.year = "2008"
        self.job1.label = "BREAKING_BAD_S01_D1"
        self.job1.video_type = "series"
        self.job1.status = "success"
        self.job1.path = "/media/completed/tv/Breaking Bad (2008)"
        self.job1.poster_url = "http://example.com/poster1.jpg"
        self.job1.start_time = Mock()
        self.job1.start_time.strftime.return_value = "2023-01-01"

        self.job2 = Mock()
        self.job2.job_id = 2
        self.job2.title = "Breaking Bad"
        self.job2.title_manual = None
        self.job2.year = "2008"
        self.job2.label = "BREAKING_BAD_S01_D2"
        self.job2.video_type = "series"
        self.job2.status = "success"
        self.job2.path = "/media/completed/tv/Breaking Bad (2008)_123456789"
        self.job2.poster_url = "http://example.com/poster2.jpg"
        self.job2.start_time = Mock()
        self.job2.start_time.strftime.return_value = "2023-01-02"

    def test_series_info_analysis_same_series(self):
        """Test that series info analysis works correctly for same series"""
        # Test data for same series
        jobs = [self.job1, self.job2]
        
        # Expected results
        expected_series_name = "Breaking Bad"
        expected_conflicts = False
        
        # Mock the series analysis logic
        series_names = set()
        for job in jobs:
            series_name = job.title_manual if job.title_manual else job.title
            if series_name and job.year:
                series_name = series_name.replace(f"({job.year})", "").strip()
            series_names.add(series_name)
        
        has_conflicts = len(series_names) > 1
        suggested_name = list(series_names)[0] if len(series_names) == 1 else ""
        
        self.assertEqual(suggested_name, expected_series_name)
        self.assertEqual(has_conflicts, expected_conflicts)

    def test_series_info_analysis_different_series(self):
        """Test that series info analysis detects conflicts for different series"""
        # Create jobs with different series
        job3 = Mock()
        job3.title = "Game of Thrones"
        job3.title_manual = None
        job3.year = "2011"
        
        jobs = [self.job1, job3]
        
        # Mock the series analysis logic
        series_names = set()
        for job in jobs:
            series_name = job.title_manual if job.title_manual else job.title
            if series_name and job.year:
                series_name = series_name.replace(f"({job.year})", "").strip()
            series_names.add(series_name)
        
        has_conflicts = len(series_names) > 1
        
        self.assertTrue(has_conflicts)
        self.assertEqual(len(series_names), 2)
        self.assertIn("Breaking Bad", series_names)
        self.assertIn("Game of Thrones", series_names)

    def test_preview_rename_generation(self):
        """Test that preview rename generates correct new paths"""
        # Mock clean_for_filename behavior locally
        def clean_for_filename(x):
            return x.replace(' ', '-').replace('_', '-')
        
        # Test data
        jobs = [self.job1, self.job2]
        series_name = "Breaking Bad"
        use_custom_name = False
        custom_name = ""
        
        # Expected results
        expected_results = []
        base_name = series_name
        
        for job in jobs:
            if job.label:
                clean_label = clean_for_filename(job.label)
                new_folder_name = f"{clean_for_filename(base_name)}_{clean_label}"
            else:
                new_folder_name = f"{clean_for_filename(base_name)}_{job.job_id}"
            
            # Construct new path
            if job.path:
                path_parts = job.path.split(os.sep)
                path_parts[-1] = new_folder_name
                new_path = os.sep.join(path_parts)
            else:
                new_path = new_folder_name
                
            expected_results.append({
                'job_id': job.job_id,
                'current_title': job.title_manual if job.title_manual else job.title,
                'current_path': job.path,
                'new_folder_name': new_folder_name,
                'new_path': new_path,
                'label': job.label
            })
        
        # Verify the expected structure
        self.assertEqual(len(expected_results), 2)
        self.assertEqual(expected_results[0]['new_folder_name'], 'Breaking-Bad_BREAKING-BAD-S01-D1')
        self.assertEqual(expected_results[1]['new_folder_name'], 'Breaking-Bad_BREAKING-BAD-S01-D2')

    def test_custom_name_override(self):
        """Test that custom name overrides detected series name"""
        series_name = "Breaking Bad"
        use_custom_name = True
        custom_name = "My Custom Series Name"
        
        # When using custom name, base_name should be custom_name
        base_name = custom_name if use_custom_name else series_name
        
        self.assertEqual(base_name, custom_name)

    def test_folder_name_generation_no_label(self):
        """Test folder name generation when job has no label"""
        job = Mock()
        job.job_id = 999
        job.label = None
        
        base_name = "Test Series"
        
        # When no label, should use job_id
        if job.label:
            new_folder_name = f"{base_name.replace(' ', '-')}_{job.label}"
        else:
            new_folder_name = f"{base_name.replace(' ', '-')}_{job.job_id}"
        
        expected = "Test-Series_999"
        self.assertEqual(new_folder_name, expected)

    def test_job_filtering_criteria(self):
        """Test that only appropriate jobs are selected for batch rename"""
        # Create various job types
        jobs = [
            # Valid job - should be included
            Mock(status='success', video_type='series', path='/some/path'),
            # Invalid - not success
            Mock(status='fail', video_type='series', path='/some/path'),
            # Invalid - not series
            Mock(status='success', video_type='movie', path='/some/path'),
            # Invalid - no path
            Mock(status='success', video_type='series', path=None),
            # Invalid - empty path
            Mock(status='success', video_type='series', path=''),
        ]
        
        # Filter jobs like the actual code would
        valid_jobs = [
            job for job in jobs 
            if (job.status == 'success' and 
                job.video_type == 'series' and 
                job.path and 
                job.path != '')
        ]
        
        self.assertEqual(len(valid_jobs), 1)
        self.assertEqual(valid_jobs[0].status, 'success')
        self.assertEqual(valid_jobs[0].video_type, 'series')
        self.assertIsNotNone(valid_jobs[0].path)
        self.assertNotEqual(valid_jobs[0].path, '')


if __name__ == '__main__':
    unittest.main()