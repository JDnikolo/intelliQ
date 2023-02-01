import subprocess

class TestUsermod:
    
    #Test 1
    def test_right_output(self):
        subprocess.run(["python", "login", "--username", "andreane82", "--passw", "e00f8e21a864de304a6c"])
        process = subprocess.Popen(["python", "admin", "--usermod", "--username", "user55", "--passw", "12345"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert output == b"User Registered/password updated Successfully!\r\n\r\n"
        
    #Test 2
    def test_admin_change(self):
        process = subprocess.Popen(["python", "admin", "--usermod","--username", "andreane82", "--passw", "e00f8e21a864de304a6c"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert output == b"User andreane82 has the Admin role and their credentials cannot be modified using this endpoint.\r\n"
        
    #Test 3
    def test_long_credentials(self):
        process = subprocess.Popen(["python", "admin", "--usermod","--username", "superduperuser", "--passw", "querty"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert output == b"Username and/or password are too long.\r\n"
     
    #Test 4
    def test_unauthorized(self):
            subprocess.run(["python", "logout"])
            process = subprocess.Popen(["python", "admin", "--usermod","--username", "user55", "--passw", "12345"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, errors = process.communicate()
            print(errors)
            assert b"You are unauthorized to perform this action!" in output
            
class TestUsers:
    
    #Test 1
    def test_right_output(self):
        subprocess.run(["python", "login", "--username", "andreane82", "--passw", "e00f8e21a864de304a6c"])
        process = subprocess.Popen(["python", "admin", "--users","--username", "user55", "--format", "json"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert b"User data :" in output
        
    #Test 2
    def test_csv(self):
        process = subprocess.Popen(["python", "admin", "--users","--username", "user55", "--format", "csv"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert b"user55 info saved at csv_files directory successfully!" in output
        
    #Test 3
    def test_no_user_found(self):
        process = subprocess.Popen(["python", "admin", "--users","--username", "user66", "--format", "json"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert output == b"User user66 was not found.\r\n"
        
    #Test 4
    def test_admin(self):
        process = subprocess.Popen(["python", "admin", "--users","--username", "andreane82", "--format", "json"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert output == b"User andreane82 has the Admin role and their credentials cannot be retrieved using this endpoint.\r\n"
        
    #Test 5
    def test_unauthorized(self):
            subprocess.run(["python", "logout"])
            process = subprocess.Popen(["python", "admin", "--users","--username", "user55", "--format", "json"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, errors = process.communicate()
            print(errors)
            assert b"You are not authorized to use this endpoint." in output