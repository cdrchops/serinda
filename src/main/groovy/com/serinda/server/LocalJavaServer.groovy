import com.madgaze.smartglass.otg.sensor.USBSerial2

def usbs2 = new USBSerial2()
usbs2.onStart();

// crap I closed the browser tabs before I could get which page this came from
 server = new ServerSocket(5000)
 while(true) {
     server.accept() { socket ->
         socket.withStreams { input, output ->
             // ignore input and just serve dummy content
             output.withWriter { writer ->
                 writer << "HTTP/1.1 200 OK\n"
                 writer << "Content-Type: text/html\n\n"
                 writer << "<html><body>Hello World! It's ${new Date()}</body></html>\n"
             }
         }
     }
 }

// https://glaforge.appspot.com/article/the-jdk-built-in-web-server-with-apache-groovy
/*
import com.sun.net.httpserver.HttpServer

HttpServer.create(new InetSocketAddress(8080), 0).with {
  createContext("/hello") { http ->
    http.responseHeaders.add("Content-type", "text/plain")
    http.sendResponseHeaders(200, 0)
    http.responseBody.withWriter { out ->
      out << "Hello ${http.remoteAddress.hostName}!"
    }
  }
  start()
}
*/