import os
from os.path import isfile, join

import boto3
from dotenv import find_dotenv, load_dotenv

env_file = find_dotenv(filename=f'.env.{os.getenv("FLASK_ENV")}')
load_dotenv(env_file)


def upload_backup_file_to_S3():
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("S3_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("S3_SECRET_KEY"),
        region_name=os.getenv("S3_REGION"),
    )

    only_files = [f for f in os.listdir("./backups") if isfile(join("./backups", f))]

    try:
        for filename in only_files:
            if "sql.gz" in filename:
                s3.upload_file(
                    f"./backups/{filename}",
                    os.getenv("S3_BUCKET_NAME"),
                    f"backups/{filename}",
                )
                os.remove(f"./backups/{filename}")

    except Exception as e:
        print(f"Error when upload file to S3. error = {e}")


upload_backup_file_to_S3()
