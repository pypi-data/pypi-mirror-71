# Supertype Implement

Implement is the backbone of Supertype. This library enables the easy, secure, and efficient end-to-end encrypted production and consumption of data between connected devices.

## Functions:

### produce(data, attribute, nuid)
- data: the data to be encrypted and produced
- attribute: the Supertype consumer attriubute you wish to produce to Supertype (see <TODO: add vendor dashboard link>)
- supertype_id: the Supertype ID of the currently logged-in Supertype user

### consume(supertype_id, attribute, date)
- supertype_id: the Supertype ID of the currently logged-in Supertype user
- attribute: the Supertype consumer attriubute you wish to consume (see <TODO: add vendor dashboard link>)
- date: the date you want to receive data from