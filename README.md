# Note:
- Coordinate vector is a string written in an array of numbers, depending on which base we use.
- The standard base is "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-_=+[]{};:,.<>/?|\'\"~", which is 92 characters long.
- In our database, there are 100,001 different base, where each will give a different coordinate vector for the same string.
# How does the encrypting algorithm work?
## Encryption
- First, from the client input, we have a "key" and a "password", let Key:="key" and Password:="password".
- Key is then turned into a coordinate vector using the standard base.
- Depending on Key, we go into our database and get another base which is different from the standard base, we call it Base. Each Key should give a different base.
- Then we write Password in its coordinate vector form using Base. After that, we hash each entry of the coordinate vector using hash seed calculated based on Key. Then, we salt the hash by injecting random numbers (from 0 - 91) into the coordinate vector. Ofcourse, we have to remember the order of injection so that we can decrypt it afterward.
- Finally, the coordinate vector after hash and salt, is converted back into the string representation and return to the client.
## Decryption
- Similar to Encryption, but in opposite order.
- First, we still get Key and Password from the client. Key is then turned into a coordinate vector and we get Base. Note that if Key is the same, we get the same Base and that makes our encryption/decryption work.
- Then, to turn the encrypted string back into its original one, we remove the salt, then hash it in the backward direction (opposite to in Encryption). But it is a pain to do so because we have to work with negative numbers. So we reverse Base, then apply hash in forward direction like in Encryption, and there we go our original password. We have successfully decrypt it!!!
