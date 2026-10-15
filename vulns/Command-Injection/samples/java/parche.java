import java.io.IOException;
import java.net.InetAddress;
import java.net.URI;
import java.net.http.*;
import java.util.concurrent.TimeUnit;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

@RestController
public class ToolsController {

    // Patch 1: ProcessBuilder con lista de argumentos (sin shell) + validacion + timeout
    @PostMapping("/ping")
    public String ping(@RequestParam String host) throws Exception {
        if (!host.matches("^[0-9.]{7,15}$") && !host.matches("^[0-9a-fA-F:]{2,39}$"))
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST);
        Process p = new ProcessBuilder("ping", "-c", "1", host).start();
        if (!p.waitFor(5, TimeUnit.SECONDS)) p.destroyForcibly();
        return new String(p.getInputStream().readAllBytes());
    }

    // Patch 2: HttpClient en vez de curl
    private static final HttpClient HTTP = HttpClient.newBuilder()
            .followRedirects(HttpClient.Redirect.NEVER).build();

    @GetMapping("/fetch")
    public String fetch(@RequestParam String url) throws IOException, InterruptedException {
        URI uri = URI.create(url);
        if (!"http".equals(uri.getScheme()) && !"https".equals(uri.getScheme()))
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST);
        return HTTP.send(HttpRequest.newBuilder(uri).build(), HttpResponse.BodyHandlers.ofString()).body();
    }
}
