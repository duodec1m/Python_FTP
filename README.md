# cpsc471_project_ftp

## Group Members

1. Huy Ho - hho114@csu.fullerton.edu

2. Brannon Ha - brannonha@csu.fullerton.edu

3. Chandler Ebrahimi - csebra@csu.fullerton.edu

## Language

Python

## How To Execute Program

Open two terminals and go to project directory. Client and Server will run on different terminal.

### Start the Server

```terminal
python3 server.py <port>
ex: python3 server.py 1234
```

### Start the Client

```terminal
python3 client.py <hostname> <port>
ex: python3 client.py 127.0.0.1 1234
```

### How to use commands on the client

#### ls

Lists the files present in the `servFiles` directory on the server.
Example:

```terminal
ftp> ls
```

#### put

Sends a file from the client to the server. The file will be placed in the server's `files` directory.
Example:

```terminal
ftp> put <filename>
```

#### get

Gets a file from the server and downloads it to the client.
Example:

```terminal
ftp> get <filename>
```

#### quit

Provides a method for cleanly closing the control connection between the client and server.
Example

```terminal
ftp> quit
```

## Notes

Requires Python 3.7 or greater

Client manage files from clientFiles directory
Server manage files from serverFiles directory
