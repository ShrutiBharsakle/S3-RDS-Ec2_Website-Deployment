from flask import Flask, render_template, request, redirect, url_for
import pymysql
import boto3
from werkzeug.utils import secure_filename
import os
import config

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp/'

# Initialize S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=config.customuser,  # Note: In production, use proper AWS credentials
    aws_secret_access_key=config.custompass,
    region_name=config.customregion
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_employee', methods=['POST'])
def add_employee():
    # Get form data
    employee_id = request.form['employee_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    location = request.form['location']
    image_file = request.files['image_file']
    
    # Upload image to S3
    if image_file:
        filename = secure_filename(f"{employee_id}_{image_file.filename}")
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(temp_path)
        
        # Upload to S3
        s3_filename = f"employee_images/{filename}"
        s3.upload_file(
            temp_path, 
            config.custombucket, 
            s3_filename,
            ExtraArgs={'ACL': 'public-read'}
        )
        
        # Generate S3 URL
        image_url = f"https://{config.custombucket}.s3.{config.customregion}.amazonaws.com/{s3_filename}"
        
        # Clean up temporary file
        os.remove(temp_path)
    else:
        image_url = None
    
    # Save to database
    connection = pymysql.connect(
        host=config.customhost,
        user=config.customuser,
        password=config.custompass,
        database=config.customdb
    )
    
    try:
        cursor = connection.cursor()
        sql = "INSERT INTO employees (employee_id, first_name, last_name, location, image_url) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (employee_id, first_name, last_name, location, image_url))
        connection.commit()
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        connection.close()
    
    return redirect(url_for('success'))

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0', port=80)

