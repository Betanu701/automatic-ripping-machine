"""
ARM route blueprint for batch rename functionality
Covers:
- batch_rename [GET/POST] - Main batch rename page
- api endpoints for batch operations
"""

import os
import json
import logging
from flask import render_template, request, Blueprint, flash, redirect, url_for, jsonify, session
from flask_login import login_required
from sqlalchemy import and_

import arm.ui.utils as ui_utils
from arm.ui import app, db
from arm.models.job import Job, JobState
from arm.ripper import utils as ripper_utils
import arm.config.config as cfg
from arm.ui.forms import BatchRenameForm

route_batch_rename = Blueprint('route_batch_rename', __name__,
                             template_folder='templates',
                             static_folder='../static')


@route_batch_rename.route('/batch_rename')
@login_required
def batch_rename():
    """
    Main batch rename page showing completed TV series jobs
    """
    # Set page title for navigation
    session["page_title"] = "Batch Rename"
    
    # Get all successful TV series jobs that have completed paths
    tv_jobs = Job.query.filter(
        and_(
            Job.status == 'success',
            Job.video_type == 'series',
            Job.path.isnot(None),
            Job.path != ''
        )
    ).order_by(Job.start_time.desc()).all()
    
    form = BatchRenameForm()
    
    return render_template('batch_rename.html', jobs=tv_jobs, form=form)


@route_batch_rename.route('/get_series_info', methods=['POST'])
@login_required
def get_series_info():
    """
    API endpoint to get series information for selected jobs
    Returns the detected series name and any conflicts
    """
    job_ids = request.json.get('job_ids', [])
    
    if not job_ids:
        return jsonify({'error': 'No jobs selected'}), 400
    
    jobs = Job.query.filter(Job.job_id.in_(job_ids)).all()
    
    # Analyze selected jobs for series names
    series_names = set()
    job_details = []
    
    for job in jobs:
        # Get the series name from title (remove year if present)
        series_name = job.title_manual if job.title_manual else job.title
        if series_name and job.year:
            series_name = series_name.replace(f"({job.year})", "").strip()
        
        series_names.add(series_name)
        job_details.append({
            'job_id': job.job_id,
            'title': job.title,
            'title_manual': job.title_manual,
            'year': job.year,
            'label': job.label,
            'path': job.path,
            'detected_series': series_name
        })
    
    # Check for conflicts (multiple different series names)
    has_conflicts = len(series_names) > 1
    suggested_name = list(series_names)[0] if len(series_names) == 1 else ""
    
    return jsonify({
        'success': True,
        'job_details': job_details,
        'suggested_series_name': suggested_name,
        'has_conflicts': has_conflicts,
        'series_names_found': list(series_names)
    })


@route_batch_rename.route('/preview_rename', methods=['POST'])
@login_required
def preview_rename():
    """
    Preview what the new folder names would be
    """
    job_ids = request.json.get('job_ids', [])
    series_name = request.json.get('series_name', '')
    use_custom_name = request.json.get('use_custom_name', False)
    custom_name = request.json.get('custom_name', '')
    
    if not job_ids:
        return jsonify({'error': 'No jobs selected'}), 400
        
    if not series_name and not (use_custom_name and custom_name):
        return jsonify({'error': 'No series name or custom name provided'}), 400
    
    jobs = Job.query.filter(Job.job_id.in_(job_ids)).all()
    
    preview_results = []
    base_name = custom_name if use_custom_name else series_name
    
    for job in jobs:
        current_path = job.path
        
        # Generate new folder name: SeriesName_DiscLabel
        if job.label:
            # Clean the label for use in filename
            clean_label = ripper_utils.clean_for_filename(job.label)
            new_folder_name = f"{ripper_utils.clean_for_filename(base_name)}_{clean_label}"
        else:
            # Fallback if no label
            new_folder_name = f"{ripper_utils.clean_for_filename(base_name)}_{job.job_id}"
        
        # Construct new path
        if current_path:
            path_parts = current_path.split(os.sep)
            path_parts[-1] = new_folder_name  # Replace last part (folder name)
            new_path = os.sep.join(path_parts)
        else:
            new_path = new_folder_name
            
        preview_results.append({
            'job_id': job.job_id,
            'current_title': job.title_manual if job.title_manual else job.title,
            'current_path': current_path,
            'new_folder_name': new_folder_name,
            'new_path': new_path,
            'label': job.label
        })
    
    return jsonify({
        'success': True,
        'preview': preview_results
    })


@route_batch_rename.route('/execute_rename', methods=['POST'])
@login_required
def execute_rename():
    """
    Execute the batch rename operation
    """
    job_ids = request.json.get('job_ids', [])
    series_name = request.json.get('series_name', '')
    use_custom_name = request.json.get('use_custom_name', False)
    custom_name = request.json.get('custom_name', '')
    
    if not job_ids:
        return jsonify({'error': 'No jobs selected'}), 400
        
    if not series_name and not (use_custom_name and custom_name):
        return jsonify({'error': 'No series name or custom name provided'}), 400
    
    jobs = Job.query.filter(Job.job_id.in_(job_ids)).all()
    
    results = []
    base_name = custom_name if use_custom_name else series_name
    
    for job in jobs:
        try:
            current_path = job.path
            
            if not current_path or not os.path.exists(current_path):
                results.append({
                    'job_id': job.job_id,
                    'success': False,
                    'error': f'Path does not exist: {current_path}'
                })
                continue
            
            # Generate new folder name: SeriesName_DiscLabel
            if job.label:
                clean_label = ripper_utils.clean_for_filename(job.label)
                new_folder_name = f"{ripper_utils.clean_for_filename(base_name)}_{clean_label}"
            else:
                new_folder_name = f"{ripper_utils.clean_for_filename(base_name)}_{job.job_id}"
            
            # Construct new path
            path_parts = current_path.split(os.sep)
            path_parts[-1] = new_folder_name
            new_path = os.sep.join(path_parts)
            
            # Check if target already exists
            if os.path.exists(new_path) and new_path != current_path:
                results.append({
                    'job_id': job.job_id,
                    'success': False,
                    'error': f'Target path already exists: {new_path}'
                })
                continue
            
            # Perform the rename
            if new_path != current_path:
                os.rename(current_path, new_path)
                
                # Update the job record
                job.path = new_path
                
                # Also update the title if using custom name
                if use_custom_name and custom_name:
                    job.title_manual = f"{custom_name} ({job.year})" if job.year else custom_name
                
                db.session.commit()
                
                app.logger.info(f"Renamed job {job.job_id} from {current_path} to {new_path}")
            
            results.append({
                'job_id': job.job_id,
                'success': True,
                'old_path': current_path,
                'new_path': new_path
            })
            
        except Exception as e:
            app.logger.error(f"Failed to rename job {job.job_id}: {str(e)}", exc_info=True)
            results.append({
                'job_id': job.job_id,
                'success': False,
                'error': str(e)
            })
    
    successful_renames = sum(1 for r in results if r['success'])
    
    return jsonify({
        'success': True,
        'results': results,
        'total_processed': len(results),
        'successful_renames': successful_renames
    })