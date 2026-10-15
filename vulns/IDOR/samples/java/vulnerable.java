import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/notes")
public class NoteController {
    private final NoteRepository repo;
    public NoteController(NoteRepository repo) { this.repo = repo; }

    // Vuln: Spring Security exige login, pero no se verifica el dueño
    @GetMapping("/{id}")
    public Note get(@PathVariable Long id) {
        return repo.findById(id).orElseThrow();     // /api/notes/1, /api/notes/2, ...
    }

    // Vuln: endpoint de "debug" que devuelve todo y quedo sin auth en SecurityConfig
    @GetMapping("/debug/all")
    public Iterable<Note> all() {
        return repo.findAll();
    }
}
