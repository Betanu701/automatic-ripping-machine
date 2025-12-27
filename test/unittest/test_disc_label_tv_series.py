#!/usr/bin/env python3
"""
Test for the USE_DISC_LABEL_FOR_TV_SERIES functionality
"""
import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add the ARM module path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from arm.ripper.utils import fix_job_title


class TestDiscLabelForTvSeries(unittest.TestCase):
    """Test USE_DISC_LABEL_FOR_TV_SERIES functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.job = Mock()
        self.job.title = "Test TV Series"
        self.job.title_manual = None
        self.job.year = "2023"
        self.job.label = "TV_SERIES_S01_D1"
        self.job.video_type = "series"

    @patch('arm.ripper.utils.cfg')
    @patch('arm.ripper.utils.logging')
    def test_fix_job_title_tv_series_with_disc_label_enabled(self, mock_logging, mock_cfg):
        """Test that disc label is used for TV series when USE_DISC_LABEL_FOR_TV_SERIES is True"""
        # Configure the mock to return True for USE_DISC_LABEL_FOR_TV_SERIES
        mock_cfg.arm_config.get.return_value = True
        
        result = fix_job_title(self.job)
        
        # Should return cleaned disc label for TV series
        self.assertIn("TV-SERIES", result)  # Part of the cleaned label
        mock_cfg.arm_config.get.assert_called_with("USE_DISC_LABEL_FOR_TV_SERIES", False)
        # Should log the use of disc label
        mock_logging.info.assert_called()

    @patch('arm.ripper.utils.cfg')
    def test_fix_job_title_tv_series_with_disc_label_disabled(self, mock_cfg):
        """Test that series title is used when USE_DISC_LABEL_FOR_TV_SERIES is False"""
        # Configure the mock to return False for USE_DISC_LABEL_FOR_TV_SERIES
        mock_cfg.arm_config.get.return_value = False
        
        result = fix_job_title(self.job)
        
        # Should return TV series title with year
        self.assertEqual(result, "Test TV Series (2023)")
        mock_cfg.arm_config.get.assert_called_with("USE_DISC_LABEL_FOR_TV_SERIES", False)

    @patch('arm.ripper.utils.cfg')
    def test_fix_job_title_movie_not_affected(self, mock_cfg):
        """Test that movies are not affected by USE_DISC_LABEL_FOR_TV_SERIES setting"""
        # Configure the mock to return True but job is a movie
        mock_cfg.arm_config.get.return_value = True
        self.job.video_type = "movie"
        self.job.title = "Test Movie"
        
        result = fix_job_title(self.job)
        
        # Should return movie title with year, not disc label
        self.assertEqual(result, "Test Movie (2023)")

    @patch('arm.ripper.utils.cfg')
    def test_fix_job_title_tv_series_with_no_label(self, mock_cfg):
        """Test behavior when TV series has no disc label"""
        # Configure the mock to return True but job has no label
        mock_cfg.arm_config.get.return_value = True
        self.job.label = None
        
        result = fix_job_title(self.job)
        
        # Should fall back to series title since label is None
        self.assertEqual(result, "Test TV Series (2023)")

    @patch('arm.ripper.utils.cfg')
    def test_fix_job_title_tv_series_manual_title(self, mock_cfg):
        """Test that manual title takes precedence when not using disc label"""
        # Configure the mock to return False for USE_DISC_LABEL_FOR_TV_SERIES
        mock_cfg.arm_config.get.return_value = False
        self.job.title_manual = "Manual Series Override"
        
        result = fix_job_title(self.job)
        
        # Should return manual title with year
        self.assertEqual(result, "Manual Series Override (2023)")


if __name__ == '__main__':
    unittest.main()