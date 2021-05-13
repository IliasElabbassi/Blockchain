## Simple blockchain implementation in python:

- can hash in simple sha256
- can hash with a merkle tree hashing using sha256

### Lib used :

- <a href="https://docs.python.org/3/library/json.html">json</a>
- <a href="https://docs.python.org/3/library/hashlib.html">hashlib</a>
- <a href="https://docs.python.org/3/library/time.html">time</a>
- <a href="https://docs.python-requests.org/en/master/index.html">requests</a>
- <a href="https://flask.palletsprojects.com/en/2.0.x/">Flask</a>
- <a href="https://docs.python.org/3/library/uuid.html">uuid</a>

## Diagrams

### <u>Implementation diagram</u>:

<b>Block</b> :    represents the data <br/>
<b>Blockchain </b>:   link the blocks together thanks to cryptographic function <br/>
<b>Interface</b> :    API interface whick interacts with the blockchain ( creating transaction etc ) <br/>
<p align="center">
  <img src="https://github.com/IliasElabbassi/Blockchain/blob/master/images/diagram_simple.jpg?raw=true" width="500" height="500" />
</p>

### <u>Basic execution diagram on run</u>:
<p align="center">
  <img src="https://github.com/IliasElabbassi/Blockchain/blob/master/images/run_exection_diagram.jpg?raw=true" height="250" />
</p>

## API Execution Diagrams

[POST] : /transaction/new <br>
take 3 arguments:
- add1 : Adresse of the sender
- add2 : Adresse of the receiver 
- amt : the amount to transfer

<p align="center">
  <img src="https://github.com/IliasElabbassi/Blockchain/blob/master/images/api_call_make_transac.jpg?raw=true" height="250" />
</p>


## License
[MIT](https://choosealicense.com/licenses/mit/)
