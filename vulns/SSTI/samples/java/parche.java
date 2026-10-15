import freemarker.core.TemplateClassResolver;
import freemarker.template.*;
import java.io.*;
import org.springframework.web.bind.annotation.*;

@RestController
public class GreetingController {
    private final Configuration cfg = new Configuration(Configuration.VERSION_2_3_32);

    public GreetingController() {
        // Patch 1: bloquear ?new y ?api (vectores de RCE en Freemarker)
        cfg.setNewBuiltinClassResolver(TemplateClassResolver.ALLOWS_NOTHING_RESOLVER);
        cfg.setAPIBuiltinEnabled(false);
    }

    // Patch 2 (preferido): sin plantillas del usuario, sustitucion simple
    @PostMapping("/greeting")
    public String greeting(@RequestParam String template) {
        return template.replace("{user}", "alice");
    }
}
