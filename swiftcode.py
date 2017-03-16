#Reference - https://www.ibm.com/developerworks/community/blogs/1b48459f-4091-43cb-bca4-37863606d989/entry/Use_Python_to_access_your_Bluemix_Object_Storage_Service_with_Keystone_v3?lang=en
#Name: Jeetendra Patil
#Assigment number - 1
#Course CSE 6331   Cloud Computing.
#First you'll need to import the swiftclient, and your Bluemix credentials to establish a swift connection  
import swiftclient
import gnupg
# Keystone v3 authentication url for IBM Public Cloud
auth_url = 'https://identity.open.softlayer.com/v3'
# Uniquely identifies an OpenStack project
project_id = ''
# Uniquely identifies an OpenStack user
user_id = ''
# Swift region
region_name = 'dallas'
# Password for authentication
password = ''
# Get a Swift client connection object
conn = swiftclient.Connection(
        key=password,
        authurl=auth_url,
        auth_version='3',
        os_options={"project_id": project_id,
                             "user_id": user_id,
                             "region_name": region_name})

# Container name for testing
container_name = 'new-container'
# File names
file_name_upload = 'upload.txt'
file_name_download='download.txt'
encrypted_file='my-encrypted.txt'
decrypted_file='my-decrypted.txt'
# Create a new container
conn.put_container(container_name)
print "\nContainer %s created successfully." % container_name

# List your containers
print ("\nContainer List:")
for container in conn.get_account()[1]:
    print container['name']
#Python-gnupg code
gpg = gnupg.GPG(gnupghome='/home/jeet/Cloud/gpghome')
input_data = gpg.gen_key_input(key_type="RSA", key_length=1024,passphrase='my passphrase')
#Generate a key
key = gpg.gen_key(input_data)
print key
#Encrypt a file 
with open(file_name_upload, 'rb') as f:
    status = gpg.encrypt_file(f,None,passphrase='my passphrase',symmetric='AES256',output=encrypted_file)
print 'ok: ', status.ok
print 'status: ', status.status
print 'stderr: ', status.stderr
print 'data: ', status.data
# Upload a file
with open(encrypted_file, 'r') as example_file:
    conn.put_object(container_name,
    encrypted_file,
    contents= example_file.read(),
    content_type='text/plain')
# List objects in a container, and prints out each object name, the file size, and last modified date
print ("\nObject List:")
for container in conn.get_account()[1]:
    for data in conn.get_container(container['name'])[1]:
        print 'object: {0}\t size: {1}\t date: {2}'.format(data['name'], data['bytes'], data['last_modified'])
# Download an object and save it to ./download.txt
obj = conn.get_object(container_name, encrypted_file)
with open(file_name_download, 'w') as my_example:
       my_example.write(obj[1])
       print "\nObject %s downloaded successfully." % file_name_download
#Decrypt a file
with open(file_name_download, 'rb') as f:
    status = gpg.decrypt_file(f, passphrase='my passphrase', output=decrypted_file)	
print 'ok: ', status.ok
print 'status: ', status.status
print 'stderr: ', status.stderr
print 'data: ', status.data
# Delete an object
conn.delete_object(container_name, encrypted_file)
print "\nObject %s deleted successfully." % encrypted_file
# To delete a container. Note: The container must be empty!
conn.delete_container(container_name)
print "\nContainer %s deleted successfully.\n" % container_name
