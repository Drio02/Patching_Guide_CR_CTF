import java.security.Principal;
import java.util.Optional;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

// En el repositorio:
// interface NoteRepository extends CrudRepository<Note, Long> {
//     Optional<Note> findByIdAndOwner(Long id, String owner);
// }

@RestController
@RequestMapping("/api/notes")
public class NoteController {
    private final NoteRepository repo;
    public NoteController(NoteRepository repo) { this.repo = repo; }

    // Patch: el dueño viene del Principal autenticado y forma parte de la consulta
    @GetMapping("/{id}")
    public Note get(@PathVariable Long id, Principal principal) {
        return repo.findByIdAndOwner(id, principal.getName())
                   .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND));
    }

    // Patch: el endpoint de debug se elimina (no hay razon para que exista en el juego)
}
