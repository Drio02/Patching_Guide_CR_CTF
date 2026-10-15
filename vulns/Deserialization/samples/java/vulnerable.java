import java.io.*;
import java.util.Base64;
import org.springframework.web.bind.annotation.*;

@RestController
public class PrefsController {

    // Vuln: ObjectInputStream sobre datos del cliente
    // Con commons-collections u otras librerias en el classpath -> RCE (ysoserial)
    @PostMapping("/prefs")
    public String load(@RequestBody String b64) throws Exception {
        byte[] data = Base64.getDecoder().decode(b64);
        try (ObjectInputStream in = new ObjectInputStream(new ByteArrayInputStream(data))) {
            Prefs p = (Prefs) in.readObject();     // el cast ocurre DESPUES de deserializar
            return p.theme;
        }
    }
}

class Prefs implements Serializable {
    String theme;
}
