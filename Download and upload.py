def copy(n):
    fname = "%03i.zip" % n

    # get the remove file length
    url = 'http://digitalcorpora.org/corp/files/govdocs1/zipfiles/'+fname u = urllib2.urlopen(url)
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])

    # get the key in the bucket
    key = bucket.lookup('zipfiles/'+fname)
    if key and key.exists and key.size==file_size:
        print("{} exists and is correct size ({:,}B)".format(fname,file_size))
        return (fname,0,0) if not key:
        key = bucket.new_key('zipfiles/'+fname)

    # Download the file if we don't have it
   if os.path.exists(fname)==False or os.path.getsize(fname)!=file_size: 
   print("Downloading {}".format(url))
   block_sz = 65536
   with open(fname,"wb") as f:
       while True:
           buffer = u.read(block_sz) if not buffer:
               break
           f.write(buffer)

    # Upload the file
    print("Uploading s3://{}/{}".format(bucket_name,fname)) key.set_contents_from_filename(fname) key.set_acl('public-read')
    print("Uploaded {} {:,}B in {}s".format(fname,file_size,t1-t0))

    # Finally remove the uploaded file
    os.unlink(fname)
    return (fname,total_time, file_size)