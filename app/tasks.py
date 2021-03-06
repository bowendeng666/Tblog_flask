import time 
from app import db
from app.models import Task, User, Post
from flask import render_template, current_app
from rq import get_current_job
from app import create_app
import sys
import json
from app.email import send_email

###################All tasks would be executed in redis server####################

#push a app context to access db and send_email relevant functions
app = create_app()
app.app_context().push()

#record the progress percentage
def _set_task_progress(progress):
    job = get_current_job()
    if job:
        job.meta['progress'] = progress
        job.save_meta()
        task = Task.query.get(job.get_id())
        task.user.add_notification('task_progress', {'task_id': job.get_id(),'progress': progress})
        if progress >= 100:
            task.complete = True
        db.session.commit()

def export_posts(user_id):
    try:
        # send email with data to user
        user = User.query.get(user_id)
        _set_task_progress(0)
        data = []
        i = 0
        total_posts = user.posts.count()
        for post in user.posts.order_by(Post.timestamp.asc()):
            data.append({'body': post.body,'timestamp': post.timestamp.isoformat() + 'Z'})
            time.sleep(5)
            i += 1
            _set_task_progress(100 * i // total_posts)
        send_email('[Tblog] Your blog posts',
                sender=current_app.config['DEFAULT_MAIL_ADDR'], recipients=[user.email],\
                text_body=render_template('email/export_posts.txt', user=user),\
                html_body=render_template('email/export_posts.html', user=user),\
                attachments=[('posts.json', 'application/json',\
                              json.dumps({'posts': data}, indent=4))],sync=True)
    except:
        _set_task_progress(100)
        app.logger.error('Unhandled exception', exc_info=sys.exc_info())

