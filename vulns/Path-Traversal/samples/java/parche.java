import java.io.IOException;
import java.nio.file.*;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

@RestController
public class FileController {
    private static final Path BASE;
    static {
        try { BASE = Paths.get("/srv/notes").toRealPath(); }
        catch (IOException e) { throw new ExceptionInInitializerError(e); }
    }

    private static Path safePath(String name) throws IOException {
        Path target = BASE.resolve(name).normalize();
        // Path.startsWith compara por componentes: /srv/notes_x NO empieza con /srv/notes
        if (!target.startsWith(BASE)) throw new ResponseStatusException(HttpStatus.FORBIDDEN);
        // toRealPath sigue symlinks; volver a verificar
        Path real = target.toRealPath();
        if (!real.startsWith(BASE)) throw new ResponseStatusException(HttpStatus.FORBIDDEN);
        return real;
    }

    // Patch 1
    @GetMapping("/download")
    public byte[] download(@RequestParam String file) throws IOException {
        return Files.readAllBytes(safePath(file));
    }

    // Patch 2: normalizar ANTES de verificar
    @GetMapping("/view")
    public byte[] view(@RequestParam String file) throws IOException {
        return Files.readAllBytes(safePath(file));
    }
}
