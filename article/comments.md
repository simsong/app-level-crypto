Cavan:
First, this is an innovative and useful use of new technology as I understand it was broadly released just recently. It is good for the Census Bureau to be known for developing and paying special attention for keeping data private. I have interviewed several corporate leaders that do not appear to know that there is a difference between government agencies that regulate and statistical agencies that by law cannot use the data for regulatory purposes or disclose it in any way.

For that reason, I think that this project should be continued if the cost isn’t prohibitive.

If I understand it correctly, you are using the Web Crypto library to generate an AES symmetric Key from the Java script webpage using a public key sent over as part of the initial payload separate from the TLS used to communicate between the server and the customer facing webpage. The AES key will be sent back to the server with the data payload that is encrypted. I assume that the AES key is encrypted with the public key, the data is encrypted with AES.

First, if I understand this process correctly it appears to protect the AES encrypted key that is generated not on the server but on the client. Even if the public key that is sent to the client via a public key encryption JSON object could be extracted, it still won’t generate the symmetric AES key and the hardware that might be able to break the TLS encryption will only get a public key that can write, but not read the encrypted AES key. The AES key used to encrypt the respondent data will only be able readable by the private key on the server. If I understand this correctly, I don’t see an exposed attack vector.

If I understand this correctly, I do think the process is complicated. I think that a simple diagram of the various encryption processes should be displayed showing the weaknesses of public/private key data, the strength and weakness of symmetric AES key encryption. It should also show the stages of encryption and why it is done in that sequence.

I would also address issues of deployment, does it create a significant latency when returning data? Should all the data in a session be collected before sending it back, if so should the data be AES encrypted before it stored locally in the client cache? Would this code still be usable if it were available and vetted as open source? Will the number of AES keys and public/private keys needed create issues. I like the use of a database to organize both the data and the keys.

I did not address the example where only a public/private key was used. If I understand the examples correctly the AES seems more secure.
