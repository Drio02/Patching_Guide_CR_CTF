import java.io.IOException;
import java.nio.file.*;
import org.springframework.web.bind.annotation.*;

@RestController
public class FileController {
    private static final String BASE = "/srv/notes";

    // Vuln 1: concatenacion
    @GetMapping("/download")
    public byte[] download(@RequestParam String file) throws IOException {
        return Files.readAllBytes(Paths.get(BASE + "/" + file));   // ?file=../../etc/passwd
    }

    // Vuln 2: verificacion de String sobre la ruta sin normalizar
    @GetMapping("/view")
    public byte[] view(@RequestParam String file) throws IOException {
        Path p = Paths.get(BASE, file);
        if (!p.toString().startsWith(BASE)) throw new SecurityException();  // "/srv/notes/../../etc/passwd" pasa
        return Files.readAllBytes(p);
    }
}
