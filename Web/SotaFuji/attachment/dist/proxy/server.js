import { createServer, Socket } from "net";

const sererHost = process.env.WEB_HOST || "localhost";
const serverPort = process.env.WEB_PORT || 4001;

const hackerResponse = `HTTP/1.1 200 OK
Content-Type: text/plain
Connection: close

Hacker!`.replaceAll("\n", "\r\n");

function isAllAscii(buffer) {
  for (let i = 0; i < buffer.length; i++) {
    if (buffer[i] > 127) {
      return false;
    }
  }
  return true;
}

function validateAndGetContentLength(buffer, isRequest) {
  if (!isAllAscii(buffer)) {
    throw Error("Bad header");
  }
  const bufferStr = buffer.toString();
  const headerLines = bufferStr.split("\r\n");
  const firstLineSplitted = headerLines[0].split(" ");
  if (isRequest && firstLineSplitted[1] !== "/") {
    throw Error("Bad header");
  }
  if (!isRequest && headerLines[0] !== "HTTP/1.1 200 OK") {
    throw Error("Bad header");
  }
  const headers = new Map();
  for (let headerLine of headerLines.slice(1)) {
    const index = headerLine.indexOf(":");
    if (index === -1) {
      throw Error("Bad header");
    }
    const k = headerLine.slice(0, index);
    const v = headerLine.slice(index + 1);
    headers.set(k.trim().toLowerCase(), v.trim());
  }
  if (headers.has("transfer-encoding")) {
    throw Error("Bad header");
  }
  return parseInt(headers.get("content-length") ?? "0");
}

const server = createServer((clientSocket) => {
  const serverSocket = new Socket();
  serverSocket.connect(serverPort, sererHost);

  let clientChunks = Buffer.alloc(0);
  let isClientSendingBody = false;
  let clientBodyToSend;

  clientSocket.on("data", (data) => {
    try {
      clientChunks = Buffer.concat([clientChunks, data]);
      if (!isClientSendingBody) {
        const bodyIndex = clientChunks.indexOf("\r\n\r\n");
        if (bodyIndex === -1) return;
        const headerPart = clientChunks.subarray(0, bodyIndex);
        clientChunks = clientChunks.subarray(bodyIndex + 4);
        clientBodyToSend = validateAndGetContentLength(headerPart, true);
        isClientSendingBody = true;
        serverSocket.write(
          Buffer.concat([headerPart, Buffer.from("\r\n\r\n")])
        );
      }
      const toSend = clientChunks.subarray(0, clientBodyToSend);
      serverSocket.write(toSend);
      clientBodyToSend -= toSend.length;
    } catch (e) {
      console.error(e);
      clientSocket.write(hackerResponse);
      clientSocket.end();
      serverSocket.end();
    }
  });
  clientSocket.on("close", () => {
    serverSocket.end();
  });
  serverSocket.on("close", () => {
    clientSocket.end();
  });
  clientSocket.on("error", () => {
    clientSocket.write(hackerResponse);
    clientSocket.end();
    serverSocket.end();
  });
  serverSocket.on("error", () => {
    clientSocket.write(hackerResponse);
    clientSocket.end();
    serverSocket.end();
  });

  let serverChunks = Buffer.alloc(0);
  let isServerSendingBody = false;
  let serverBodyToSend;

  serverSocket.on("data", (data) => {
    try {
      serverChunks = Buffer.concat([serverChunks, data]);
      if (!isServerSendingBody) {
        const bodyIndex = serverChunks.indexOf("\r\n\r\n");
        if (bodyIndex === -1) return;
        const headerPart = serverChunks.subarray(0, bodyIndex);
        serverChunks = serverChunks.subarray(bodyIndex + 4);
        serverBodyToSend = validateAndGetContentLength(headerPart, false);
        isServerSendingBody = true;
        clientSocket.write(
          Buffer.concat([headerPart, Buffer.from("\r\n\r\n")])
        );
      }
      const toSend = serverChunks.subarray(0, serverBodyToSend);
      clientSocket.write(toSend);
      serverBodyToSend -= toSend.length;
      if (serverBodyToSend <= 0) {
        clientSocket.end();
        serverSocket.end();
      }
    } catch (e) {
      console.error(e);
      clientSocket.write(hackerResponse);
      clientSocket.end();
      serverSocket.end();
    }
  });
});

server.listen(4000, () => {
  console.log("Proxy server is running on port 4000");
});
