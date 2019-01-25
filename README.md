<h1>PyPass</h1>
<hr>
<p>PyPass is a project I started in January 2019. It attempts
        to provide a service similar to those offered by other password storing sites. The user sets up their connection to a MySQL server and copies the key that they
        generate which will be used to encrypt and decrypt passwords.</p>
        <p>The System imploys the use of the package, Fernet (<a href="https://cryptography.io/en/latest/fernet/">found here</a>). This is used
        for the encryption and decryption of passwords. Users are required to generate a key
        before the system will function. this can be done with the lines:</p>
        
        >>> from cryptography.fernet import Fernet 
        >>> key = Fernet.generate_key()
        >>> print (str(key))
<p>Then copying the key and placing it in the <i>key.txt</i> file. <br/>
        To create the database copy and paste the code below: </p>

        
        CREATE TABLE IF NOT EXISTS &lt;Your Database&gt; (
          site varchar(50) NOT NULL,
          username varchar(50),
          password varchar(1000),
          PRIMARY KEY (site)
          )
<p>Finally inside the file <i>connection.py</i> the four variables should be changed:</p>
 
         def connection(): <br>
              connect = mysql.connector.connect(<br>
              host="&lt;Your Host&gt;", <br>
              user="&lt;Your Username&gt;", <br>
              passwd="&lt;Your Password&gt;", <br>
              database="&lt;Your Database&gt;" <br>
          )
          
 <a href="https://ellisdeveloping.co.uk">https://ellisdeveloping.co.uk</a>
