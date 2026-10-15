import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.*;
import java.util.Base64;
import org.springframework.web.bind.annotation.*;

@RestController
public class PrefsController {
    private static final ObjectMapper JSON = new ObjectMapper();   // sin enableDefaultTyping

    // Patch 1 (preferido): JSON a un DTO concreto
    @PostMapping("/prefs")
    public String load(@RequestBody String json) throws IOException {
        Prefs p = JSON.readValue(json, Prefs.class);
        return p.theme;
    }

    // Patch 2: si hay que mantener Java serialization, allowlist con ObjectInputFilter (Java 9+)
    static Prefs legacyLoad(String b64) throws Exception {
        byte[] data = Base64.getDecoder().decode(b64);
        try (ObjectInputStream in = new ObjectInputStream(new ByteArrayInputStream(data))) {
            in.setObjectInputFilter(ObjectInputFilter.Config.createFilter(
                    "Prefs;java.lang.String;!*"));            // todo lo demas se rechaza
            return (Prefs) in.readObject();
        }
    }
}

class Prefs implements Serializable {
    public String theme;
}
