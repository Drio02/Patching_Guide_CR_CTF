import java.util.regex.Pattern;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

@RestController
public class ShopController {

    // Patch 1: DTO de entrada solo con los campos permitidos (record, Java 16+)
    public record RegisterRequest(String username, String password) {}

    @PostMapping("/register")
    public User register(@RequestBody RegisterRequest req) {
        if (req.username() == null || !req.username().matches("[a-z0-9_]{3,32}")
                || req.password() == null || req.password().length() > 128)
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST);
        User u = new User();
        u.setUsername(req.username());
        u.setPassword(req.password());                 // admin queda en false por defecto
        return userRepo.save(u);
    }

    // Patch 2: rango + multiplyExact (lanza ArithmeticException si desborda)
    @PostMapping("/buy")
    public String buy(@RequestParam int qty, @RequestParam String item, @SessionAttribute String user) {
        Integer price = PRICES.get(item);
        if (price == null || qty < 1 || qty > 100)
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST);
        int total = Math.multiplyExact(qty, price);
        // UPDATE account SET credits = credits - :total WHERE owner = :user AND credits >= :total
        if (accountRepo.debitIfEnough(user, total) != 1) return "not enough credits";
        return "flag".equals(item) ? FLAG : "ok";
    }

    // Patch 3: matches() exige que TODO el string cumpla el patron
    private static final Pattern ID = Pattern.compile("[a-f0-9]{16}");
    @GetMapping("/note")
    public Note note(@RequestParam String id) {
        if (!ID.matcher(id).matches()) throw new ResponseStatusException(HttpStatus.BAD_REQUEST);
        return noteRepo.findByPublicId(id);
    }
}
