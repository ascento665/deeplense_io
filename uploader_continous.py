import boto3
from time import sleep


# Create an S3 client
s3 = boto3.client('s3')
bucket_name = 'temp-photo'
i = 0

while(True):
        # upload frame-by-frame
        filename = "pictures/movement.jpg"
        filename_dest = 'uploads/' + "movement.jpg"

        # Uploads the given file using a managed uploader, which will split up large
        # files automatically and upload parts in parallel.
        s3.upload_file(filename, bucket_name, filename_dest)
        i = (i+1)
        print "uploaded a picture to s3", i
        print filename
        sleep(0.5)

print "finished upload"
