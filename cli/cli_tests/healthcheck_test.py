import subprocess

class TestHealthCheck:
    #Test 1
    def test_right_output(self):
        process = subprocess.run(["python", "login.py", "--username", "andreane82", "--passw", "e00f8e21a864de304a6c"])
        process = subprocess.Popen(["python", "healthcheck.py", "--format", "json"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert output == b"200\r\n{'status': 'OK', 'dbconnection': 'intelliq'}\r\n"
    #Test 2
    def test_csv_format(self):
            process = subprocess.Popen(["python", "healthcheck.py", "--format", "csv"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, errors = process.communicate()
            print(errors)
            assert b"OK" in output
            assert  b"csv file healthcheck.csv saved at csv_files directory successfully" in output
            assert b"intelliq" in output 
    #Test 3
    def test_unauthorized(self):
            process = subprocess.run(["python", "logout.py"])
            process = subprocess.Popen(["python", "healthcheck.py", "--format", "json"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, errors = process.communicate()
            print(errors)
            assert output == b"{'type': '/errors/authentication-error', 'title': 'Unauthorized User', 'status': '401', 'detail': 'User is unauthorized', 'instance': '/admin/healthcheck'}\r\n"
    

    
    