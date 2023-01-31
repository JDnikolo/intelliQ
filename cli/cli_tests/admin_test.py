import subprocess

class Usermod:
    
    #Test 1
    def test_right_output(self):
        process = subprocess.run(["python", "login", "--username", "andreane82", "--passw", "e00f8e21a864de304a6c"])
        process = subprocess.Popen(["python", "admin", "--usermod","--username", "user55", "--passw", "12345"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert output == b"User Registered/password updated Successfully!\n"
        
    #Test 2
    def test_admin_change(self):
        process = subprocess.Popen(["python", "admin", "--usermod","--username", "andreane82", "--passw", "e00f8e21a864de304a6c"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert output == b"User andreane82 has the Admin role and their credentials cannot be modified using this endpoint."
       
    #Test 3
    def test_no_credentials_given(self):
        process = subprocess.Popen(["python", "admin", "--usermod","--username", "", "--passw", ""],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert output == b"Username and/or password are required but are not included in the request."
        
    #Test 4
    def test_long_credentials(self):
        process = subprocess.Popen(["python", "admin", "--usermod","--username", "superduperuser", "--passw", "querty"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert output == b"Username and/or password are too long."
     
    #Test 5
    def test_unauthorized(self):
            process = subprocess.run(["python", "logout"])
            process = subprocess.Popen(["python", "admin", "--usermod","--username", "user55", "--passw", "12345"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, errors = process.communicate()
            print(errors)
            assert output == b"You are unauthorized to perform this action!"
            
class Users:
    
    #Test 1
    def test_right_output(self):
        process = subprocess.run(["python", "login", "--username", "andreane82", "--passw", "e00f8e21a864de304a6c"])
        process = subprocess.Popen(["python", "admin", "--users","--username", "user55", "--format", "json"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert b"User data :/n" in output
        
    #Test 2
    def test_csv(self):
        process = subprocess.run(["python", "login", "--username", "andreane82", "--passw", "e00f8e21a864de304a6c"])
        process = subprocess.Popen(["python", "admin", "--usermod","--username", "user55", "--passw", "12345"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process = subprocess.Popen(["python", "admin", "--users","--username", "user55", "--format", "csv"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert output == b"[user55 info saved at csv_files directory successfully!"
        
    #Test 3
    def test_no_credentials_given(self):
        process = subprocess.Popen(["python", "admin", "--users","--username", "", "--format", "json"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert output == b"Username is required but is not included in the request."
        
    #Test 4
    def test_no_user_found(self):
        process = subprocess.Popen(["python", "admin", "--users","--username", "user66", "--format", "json"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert output == b"User user66 was not found."
        
    #Test 5
    def test_admin(self):
        process = subprocess.Popen(["python", "admin", "--users","--username", "andreane82", "--format", "json"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert output == b"User andreane82 has the Admin role and their credentials cannot be retrieved using this endpoint."
        
    #Test 6
    def test_unauthorized(self):
            process = subprocess.run(["python", "logout"])
            process = subprocess.Popen(["python", "admin", "--users","--username", "user55", "--format", "json"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, errors = process.communicate()
            print(errors)
            assert output == b"You are not authorized to use this endpoint."